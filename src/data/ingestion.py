import logging
from datetime import date
from decimal import Decimal
from itertools import pairwise

from src.data.models import CompanyProfile, PriceBar
from src.data.service import DataService
from src.data.trading_calendar import (
    UnsupportedTradingCalendarError,
    get_expected_trading_dates,
)
from src.storage.database import get_connection

logger = logging.getLogger(__name__)
SUSPICIOUS_DAILY_PRICE_CHANGE_PERCENT = Decimal("20")


def _validate_price_bars(
    price_bars: list[PriceBar],
    start: date,
    end: date,
) -> None:
    """Reject invalid or duplicate provider bars before database persistence."""
    seen: set[tuple[date, str]] = set()

    for bar in price_bars:
        if not start <= bar.date <= end:
            raise ValueError(
                f"Price bar date {bar.date} is outside requested range {start} to {end}."
            )

        key = (bar.date, bar.source)
        if key in seen:
            raise ValueError(
                f"Duplicate price bar for {bar.date} from source {bar.source}."
            )
        seen.add(key)

        prices = {
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
        }
        if bar.adjusted_close is not None:
            prices["adjusted_close"] = bar.adjusted_close

        for field, value in prices.items():
            if not value.is_finite() or value <= 0:
                raise ValueError(
                    f"Invalid {field} price for {bar.symbol} on {bar.date}: {value}."
                )

        if bar.high < max(bar.open, bar.close):
            raise ValueError(
                f"High price is inconsistent with OHLC values for {bar.symbol} on {bar.date}."
            )

        if bar.low > min(bar.open, bar.close):
            raise ValueError(
                f"Low price is inconsistent with OHLC values for {bar.symbol} on {bar.date}."
            )

        if bar.volume is not None and bar.volume < 0:
            raise ValueError(
                f"Negative volume for {bar.symbol} on {bar.date}: {bar.volume}."
            )


def _log_price_quality_warnings(
    price_bars: list[PriceBar],
    company_profile: CompanyProfile,
) -> None:
    """Log non-blocking continuity and daily price-movement warnings."""
    if not price_bars:
        return

    bars_by_source: dict[str, list[PriceBar]] = {}
    for bar in price_bars:
        bars_by_source.setdefault(bar.source, []).append(bar)

    for source, bars in bars_by_source.items():
        ordered = sorted(bars, key=lambda bar: bar.date)
        first_date = ordered[0].date
        last_date = ordered[-1].date

        try:
            expected_dates = get_expected_trading_dates(
                first_date,
                last_date,
                company_profile.exchange,
            )
        except UnsupportedTradingCalendarError:
            expected_dates = None

        if expected_dates is not None:
            actual_dates = {bar.date for bar in ordered}
            missing_dates = [
                value for value in expected_dates if value not in actual_dates
            ]
            if missing_dates:
                logger.warning(
                    "Price history has missing trading sessions: "
                    "symbol=%s source=%s missing_dates=%s",
                    company_profile.symbol,
                    source,
                    missing_dates,
                )

        for previous, current in pairwise(ordered):
            previous_price = previous.adjusted_close or previous.close
            current_price = current.adjusted_close or current.close

            if previous_price <= 0:
                continue

            change_percent = (
                abs(current_price - previous_price) / previous_price * Decimal("100")
            )

            if change_percent > SUSPICIOUS_DAILY_PRICE_CHANGE_PERCENT:
                logger.warning(
                    "Unusually large daily price movement: "
                    "symbol=%s source=%s previous_date=%s current_date=%s "
                    "change_percent=%.2f threshold_percent=%s",
                    company_profile.symbol,
                    source,
                    previous.date,
                    current.date,
                    change_percent,
                    SUSPICIOUS_DAILY_PRICE_CHANGE_PERCENT,
                )


def ingest_price_history(
    data_service: DataService,
    symbol: str,
    start: date,
    end: date,
) -> int:
    """Fetch normalized price data and persist it to PostgreSQL."""

    company_profile = data_service.get_company_profile(symbol)
    price_bars = data_service.get_price_history(symbol, start, end)

    if not price_bars:
        return 0

    _validate_price_bars(price_bars, start, end)
    _log_price_quality_warnings(price_bars, company_profile)

    with get_connection() as connection, connection.cursor() as cursor:
        # Find or create company.
        cursor.execute(
            """
                SELECT id
                FROM companies
                WHERE symbol = %s
                  AND exchange IS NOT DISTINCT FROM %s
                LIMIT 1
                """,
            (
                company_profile.symbol,
                company_profile.exchange,
            ),
        )

        row = cursor.fetchone()

        if row:
            company_id = row[0]
        else:
            cursor.execute(
                """
                    INSERT INTO companies
                        (name, symbol, exchange, country, sector, industry)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                (
                    company_profile.name,
                    company_profile.symbol,
                    company_profile.exchange,
                    company_profile.country,
                    company_profile.sector,
                    company_profile.industry,
                ),
            )
            company_id = cursor.fetchone()[0]

        # Find or create financial instrument.
        cursor.execute(
            """
                SELECT id
                FROM financial_instruments
                WHERE company_id = %s
                  AND symbol = %s
                  AND exchange IS NOT DISTINCT FROM %s
                LIMIT 1
                """,
            (
                company_id,
                company_profile.symbol,
                company_profile.exchange,
            ),
        )

        row = cursor.fetchone()

        if row:
            instrument_id = row[0]
        else:
            cursor.execute(
                """
                    INSERT INTO financial_instruments
                        (
                            company_id,
                            symbol,
                            exchange,
                            instrument_type,
                            currency
                        )
                    VALUES
                        (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                (
                    company_id,
                    company_profile.symbol,
                    company_profile.exchange,
                    "equity",
                    company_profile.currency,
                ),
            )
            instrument_id = cursor.fetchone()[0]

        # Insert price history in one batched database operation.
        price_rows = [
            (
                instrument_id,
                bar.date,
                bar.open,
                bar.high,
                bar.low,
                bar.close,
                bar.volume,
                bar.adjusted_close,
                bar.source,
                bar.source_url,
                bar.retrieved_at,
            )
            for bar in price_bars
        ]

        cursor.executemany(
            """
                INSERT INTO price_history
                    (
                        instrument_id,
                        price_date,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        adjusted_close,
                        source,
                        source_url,
                        retrieved_at
                    )
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (instrument_id, price_date, source)
                DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume,
                    adjusted_close = EXCLUDED.adjusted_close,
                    source_url = EXCLUDED.source_url,
                    retrieved_at = EXCLUDED.retrieved_at
                WHERE price_history.retrieved_at IS NULL
                    OR EXCLUDED.retrieved_at > price_history.retrieved_at
                """,
            price_rows,
        )

        inserted = cursor.rowcount

    return inserted

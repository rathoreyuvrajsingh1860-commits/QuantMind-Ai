from datetime import date

from src.data.service import DataService
from src.storage.database import get_connection


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

    with get_connection() as connection:
        with connection.cursor() as cursor:
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

            # Insert price history.
            inserted = 0

            for bar in price_bars:
                cursor.execute(
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
                            source
                        )
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
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
                    ),
                )

                inserted += cursor.rowcount

    return inserted
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import yfinance as yf

from src.data.base import DataCapability, FinancialDataProvider
from src.data.errors import ProviderServerError, UnsupportedDataError
from src.data.models import CompanyProfile, NewsArticle, PriceBar


class YahooFinanceProvider(FinancialDataProvider):
    """Unofficial Yahoo Finance adapter for daily historical prices."""

    @property
    def capabilities(self) -> set[DataCapability]:
        return {DataCapability.PRICE_HISTORY}

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        if ":" not in symbol:
            return symbol.strip()

        ticker, exchange = symbol.rsplit(":", 1)
        exchange = exchange.strip().upper()
        suffixes = {
            "NSE": ".NS",
            "BSE": ".BO",
            "NASDAQ": "",
            "NYSE": "",
        }
        if exchange not in suffixes:
            raise ValueError(f"Unsupported Yahoo Finance exchange: {exchange}")
        return f"{ticker.strip()}{suffixes[exchange]}"

    def search_company(self, query: str) -> list[CompanyProfile]:
        raise UnsupportedDataError("Yahoo Finance adapter supports price history only")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise UnsupportedDataError("Yahoo Finance adapter supports price history only")

    def get_news(
        self,
        symbol: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[NewsArticle]:
        raise UnsupportedDataError("Yahoo Finance adapter does not provide news")

    def get_price_history(self, symbol: str, start: date, end: date) -> list[PriceBar]:
        if end < start:
            raise ValueError("end date must be on or after start date")

        ticker_symbol = self._normalize_symbol(symbol)
        try:
            frame = yf.Ticker(ticker_symbol).history(
                start=start.isoformat(),
                end=(end + timedelta(days=1)).isoformat(),
                interval="1d",
                auto_adjust=False,
                actions=False,
                raise_errors=True,
            )
        except Exception as exc:
            raise ProviderServerError(
                f"Yahoo Finance price-history request failed for {symbol}"
            ) from exc

        if frame is None or frame.empty:
            raise UnsupportedDataError(
                f"Yahoo Finance returned no daily prices for {symbol}"
            )

        # yfinance can return MultiIndex columns for some ticker responses.
        if getattr(frame.columns, "nlevels", 1) > 1:
            frame.columns = frame.columns.get_level_values(0)

        retrieved_at = datetime.now(UTC)
        bars: list[PriceBar] = []
        for timestamp, row in frame.iterrows():
            price_date = timestamp.date()
            if not start <= price_date <= end:
                continue

            def decimal_value(key: str, *, _row=row) -> Decimal:
                return Decimal(str(_row[key]))

            adjusted = row.get("Adj Close")
            bars.append(
                PriceBar(
                    symbol=symbol,
                    date=price_date,
                    open=decimal_value("Open"),
                    high=decimal_value("High"),
                    low=decimal_value("Low"),
                    close=decimal_value("Close"),
                    volume=int(row["Volume"]),
                    adjusted_close=(
                        Decimal(str(adjusted))
                        if adjusted is not None and str(adjusted) != "nan"
                        else None
                    ),
                    source="yahoo_finance",
                    source_url="https://finance.yahoo.com/",
                    retrieved_at=retrieved_at,
                )
            )

        bars.sort(key=lambda bar: bar.date)
        if not bars:
            raise UnsupportedDataError(
                f"Yahoo Finance returned no prices in the requested date range for {symbol}"
            )
        return bars

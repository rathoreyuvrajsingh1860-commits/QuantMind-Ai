from datetime import date, datetime, timezone
from decimal import Decimal

import httpx

from src.config.settings import settings
from src.data.base import FinancialDataProvider
from src.data.models import CompanyProfile, PriceBar


class AlphaVantageProvider(FinancialDataProvider):
    """Alpha Vantage implementation of the normalized data-provider interface."""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self) -> None:
        if not settings.financial_data_api_key:
            raise ValueError("FINANCIAL_DATA_API_KEY is not configured")

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=20.0,
        )

    def close(self) -> None:
        self.client.close()

    def _request(self, params: dict[str, str]) -> dict:
        response = self.client.get(
            "",
            params={
                **params,
                "apikey": settings.financial_data_api_key,
            },
        )
        response.raise_for_status()

        payload = response.json()

        if "Error Message" in payload:
            raise RuntimeError(payload["Error Message"])

        if "Note" in payload:
            raise RuntimeError(
                f"Alpha Vantage rate limit: {payload['Note']}"
            )

        return payload

    def _normalize_symbol(self, symbol: str) -> str:
        """
        Convert QuantMind's SYMBOL:EXCHANGE notation
        into Alpha Vantage's symbol notation.
        """
        if ":" not in symbol:
            return symbol.strip()

        ticker, exchange = symbol.rsplit(":", 1)

        ticker = ticker.strip()
        exchange = exchange.strip().upper()

        exchange_suffixes = {
            "BSE": ".BSE",
            "NSE": ".NSE",
            "NASDAQ": "",
            "NYSE": "",
        }

        suffix = exchange_suffixes.get(exchange)

        if suffix is None:
            raise ValueError(
                f"Unsupported Alpha Vantage exchange: {exchange}"
            )

        return f"{ticker}{suffix}"

    def search_company(self, query: str) -> list[CompanyProfile]:
        payload = self._request(
            {
                "function": "SYMBOL_SEARCH",
                "keywords": query,
            }
        )

        results = []

        for item in payload.get("bestMatches", []):
            results.append(
                CompanyProfile(
                    symbol=item.get("1. symbol", ""),
                    name=item.get("2. name", ""),
                    exchange=item.get("4. region"),
                    country=item.get("4. region"),
                    currency=item.get("8. currency"),
                )
            )

        return results

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        """Return a normalized company reference record."""

        normalized_symbol = self._normalize_symbol(symbol)

        search_symbol = normalized_symbol

        if "." in normalized_symbol:
            search_symbol = normalized_symbol.split(".", 1)[0]

        results = self.search_company(search_symbol)

        for company in results:
            if company.symbol.upper() == normalized_symbol.upper():
                return company

        # Alpha Vantage's symbol search can vary by market.
        # Return a minimal normalized reference if no exact match exists.
        return CompanyProfile(
            symbol=normalized_symbol,
            name=normalized_symbol,
            currency=None,
        )

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        """Return normalized daily historical prices."""

        normalized_symbol = self._normalize_symbol(symbol)

        payload = self._request(
            {
                "function": "TIME_SERIES_DAILY",
                "symbol": normalized_symbol,
                "outputsize": "compact",
            }
        )

        time_series = payload.get("Time Series (Daily)", {})

        if not time_series:
            raise RuntimeError(
                f"No daily price data returned for {symbol}"
            )

        retrieved_at = datetime.now(timezone.utc)

        prices: list[PriceBar] = []

        for date_string, values in time_series.items():
            price_date = datetime.strptime(
                date_string,
                "%Y-%m-%d",
            ).date()

            if not (start <= price_date <= end):
                continue

            prices.append(
                PriceBar(
                    symbol=symbol,
                    date=price_date,
                    open=Decimal(values["1. open"]),
                    high=Decimal(values["2. high"]),
                    low=Decimal(values["3. low"]),
                    close=Decimal(values["4. close"]),
                    volume=int(values["5. volume"]),
                    adjusted_close=None,
                    source="alpha_vantage",
                    retrieved_at=retrieved_at,
                )
            )

        prices.sort(key=lambda item: item.date)

        return prices
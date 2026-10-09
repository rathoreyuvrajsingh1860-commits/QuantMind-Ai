from collections.abc import Callable
from datetime import UTC, date, datetime
from decimal import Decimal

import httpx

from src.config.settings import settings
from src.data.base import (
    DataCapability,
    FinancialDataProvider,
)
from src.data.errors import (
    ProviderAuthenticationError,
    ProviderInvalidRequestError,
    ProviderServerError,
    RateLimitError,
    UnsupportedDataError,
)
from src.data.models import CompanyProfile, NewsArticle, PriceBar
from src.data.retry import retry_with_backoff


class AlphaVantageProvider(FinancialDataProvider):
    """Alpha Vantage implementation of the normalized data-provider interface."""

    BASE_URL = "https://www.alphavantage.co/query"

    @property
    def capabilities(self) -> set[DataCapability]:
        return {
            DataCapability.COMPANY_SEARCH,
            DataCapability.COMPANY_PROFILE,
            DataCapability.PRICE_HISTORY,
            DataCapability.NEWS,
        }

    def __init__(self) -> None:
        api_key = settings.alpha_vantage_api_key or settings.financial_data_api_key
        if not api_key:
            raise ValueError("Alpha Vantage API key is not configured")
        self.api_key = api_key

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=20.0,
        )

    def close(self) -> None:
        self.client.close()

    def _request_once(self, params: dict[str, str]) -> dict:
        try:
            response = self.client.get(
                "",
                params={
                    **params,
                    "apikey": self.api_key,
                },
            )
        except httpx.TimeoutException as exc:
            raise ProviderServerError("Alpha Vantage request timed out") from exc
        except httpx.RequestError as exc:
            raise ProviderServerError(f"Alpha Vantage request failed: {exc}") from exc

        if response.status_code in {401, 403}:
            raise ProviderAuthenticationError("Alpha Vantage authentication failed")

        if response.status_code == 429:
            raise RateLimitError("Alpha Vantage rate limit exceeded")

        if response.status_code >= 500:
            raise ProviderServerError(
                f"Alpha Vantage server error: HTTP {response.status_code}"
            )

        if response.status_code >= 400:
            raise ProviderInvalidRequestError(
                f"Alpha Vantage request failed: HTTP {response.status_code}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderServerError(
                "Alpha Vantage returned an invalid JSON response"
            ) from exc

        if not isinstance(payload, dict) or not payload:
            raise ProviderServerError(
                "Alpha Vantage returned an empty or invalid response"
            )

        if "Error Message" in payload:
            raise UnsupportedDataError(payload["Error Message"])

        if "Information" in payload:
            message = payload["Information"]

            if "rate limit" in message.lower():
                raise RateLimitError(message)

            raise ProviderInvalidRequestError(message)

        if "Note" in payload:
            raise RateLimitError(payload["Note"])

        return payload

    def _request(
        self,
        params: dict[str, str],
        *,
        on_attempt: Callable[[int], None] | None = None,
    ) -> dict:
        """Request provider data with controlled transient retries."""

        def operation() -> dict:
            return self._request_once(params)

        return retry_with_backoff(
            operation,
            on_attempt=on_attempt,
        )

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
            raise ValueError(f"Unsupported Alpha Vantage exchange: {exchange}")

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

        # For an explicitly qualified symbol such as RELIANCE:BSE,
        # we already know the provider symbol and exchange.
        if ":" in symbol:
            ticker, exchange = symbol.rsplit(":", 1)

            exchange = exchange.strip().upper()

            exchange_names = {
                "BSE": "BSE",
                "NSE": "NSE",
                "NASDAQ": "NASDAQ",
                "NYSE": "NYSE",
            }

            return CompanyProfile(
                symbol=normalized_symbol,
                name=ticker.strip(),
                exchange=exchange_names.get(exchange, exchange),
                country=("India" if exchange in {"BSE", "NSE"} else "United States"),
                currency=("INR" if exchange in {"BSE", "NSE"} else "USD"),
            )

        # For an unqualified symbol, use Alpha Vantage search.
        results = self.search_company(normalized_symbol)

        for company in results:
            if company.symbol.upper() == normalized_symbol.upper():
                return company

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
            raise ProviderServerError(f"No daily price data returned for {symbol}")

        retrieved_at = datetime.now(UTC)

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
                    source_url="https://www.alphavantage.co/documentation/#daily",
                    retrieved_at=retrieved_at,
                )
            )

        prices.sort(key=lambda item: item.date)

        return prices

    @staticmethod
    def _parse_news_timestamp(value: str | None) -> datetime | None:
        """Parse a provider timestamp without discarding an otherwise valid article."""

        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y%m%dT%H%M%S").replace(tzinfo=UTC)
        except (TypeError, ValueError):
            return None

    def get_news(
        self,
        symbol: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[NewsArticle]:
        """Return normalized market news for a company."""

        normalized_symbol = self._normalize_symbol(symbol)

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": normalized_symbol,
            "sort": "LATEST",
            "limit": "1000",
        }

        if start is not None:
            params["time_from"] = start.strftime("%Y%m%dT%H%M")

        if end is not None:
            params["time_to"] = end.strftime("%Y%m%dT%H%M")

        payload = self._request(params)

        retrieved_at = datetime.now(UTC)

        articles: list[NewsArticle] = []

        for item in payload.get("feed", []):
            published_at = item.get("time_published")

            articles.append(
                NewsArticle(
                    title=item.get("title", ""),
                    publisher=item.get("source"),
                    author=item.get("authors", [None])[0]
                    if item.get("authors")
                    else None,
                    published_at=self._parse_news_timestamp(published_at),
                    url=item.get("url"),
                    summary=item.get("summary"),
                    symbol=normalized_symbol,
                    source="alpha_vantage",
                    retrieved_at=retrieved_at,
                )
            )

        articles.sort(
            key=lambda item: item.published_at or datetime.min.replace(tzinfo=UTC),
            reverse=True,
        )

        return articles

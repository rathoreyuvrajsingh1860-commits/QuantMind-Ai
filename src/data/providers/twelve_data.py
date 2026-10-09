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


class TwelveDataProvider(FinancialDataProvider):
    """Twelve Data implementation of the normalized data-provider interface."""

    BASE_URL = "https://api.twelvedata.com"

    @property
    def capabilities(self) -> set[DataCapability]:
        return {
            DataCapability.COMPANY_SEARCH,
            DataCapability.COMPANY_PROFILE,
            DataCapability.PRICE_HISTORY,
        }

    def __init__(self) -> None:
        api_key = settings.twelve_data_api_key or settings.financial_data_api_key
        if not api_key:
            raise ValueError("Twelve Data API key is not configured")
        self.api_key = api_key

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=20.0,
            params={"apikey": self.api_key},
        )

    def close(self) -> None:
        self.client.close()

    def _request_once(
        self,
        path: str,
        *,
        params: dict[str, str],
    ) -> dict:
        try:
            response = self.client.get(path, params=params)
        except httpx.TimeoutException as exc:
            raise ProviderServerError("Twelve Data request timed out") from exc
        except httpx.RequestError as exc:
            raise ProviderServerError("Twelve Data request failed") from exc

        if response.status_code in {401, 403}:
            raise ProviderAuthenticationError("Twelve Data authentication failed")

        if response.status_code == 429:
            raise RateLimitError("Twelve Data rate limit exceeded")

        if response.status_code >= 500:
            raise ProviderServerError(
                f"Twelve Data server error: HTTP {response.status_code}"
            )

        if response.status_code >= 400:
            raise ProviderInvalidRequestError(
                f"Twelve Data request failed: HTTP {response.status_code}"
            )

        payload = response.json()

        if payload.get("status") != "ok":
            message = payload.get(
                "message",
                "Twelve Data request failed",
            )
            if "rate limit" in message.lower():
                raise RateLimitError(message)
            raise UnsupportedDataError(message)

        return payload

    def _request(
        self,
        path: str,
        *,
        params: dict[str, str],
        on_attempt=None,
    ) -> dict:
        return retry_with_backoff(
            lambda: self._request_once(
                path,
                params=params,
            ),
            on_attempt=on_attempt,
        )

    def search_company(self, query: str) -> list[CompanyProfile]:
        payload = self._request(
            "/symbol_search",
            params={"symbol": query},
        )

        return [
            CompanyProfile(
                symbol=item["symbol"],
                name=item.get("instrument_name", item["symbol"]),
                exchange=item.get("exchange"),
                country=item.get("country"),
                currency=item.get("currency"),
            )
            for item in payload.get("data", [])
        ]

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        """Return a company reference record, supporting SYMBOL:EXCHANGE notation."""
        if ":" in symbol:
            ticker, exchange = symbol.rsplit(":", 1)
            ticker = ticker.strip()
            exchange = exchange.strip().upper()
        else:
            ticker = symbol.strip()
            exchange = None

        results = self.search_company(ticker)

        for company in results:
            if company.symbol.upper() == ticker.upper() and (
                exchange is None or (company.exchange or "").upper() == exchange
            ):
                return company

        raise LookupError(f"Company not found: {symbol}")

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        """Return normalized daily historical prices."""
        if ":" in symbol:
            ticker, exchange = symbol.rsplit(":", 1)
            ticker = ticker.strip()
            exchange = exchange.strip().upper()
        else:
            ticker = symbol.strip()
            exchange = None

        params = {
            "symbol": ticker,
            "interval": "1day",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        }

        if exchange:
            params["exchange"] = exchange

        payload = self._request(
            "/time_series",
            params=params,
        )

        retrieved_at = datetime.now(UTC)

        return [
            PriceBar(
                symbol=symbol,
                date=datetime.strptime(
                    item["datetime"],
                    "%Y-%m-%d",
                ).date(),
                open=Decimal(item["open"]),
                high=Decimal(item["high"]),
                low=Decimal(item["low"]),
                close=Decimal(item["close"]),
                volume=int(item["volume"]) if item.get("volume") else None,
                source="twelve_data",
                source_url="https://twelvedata.com/docs#time-series",
                retrieved_at=retrieved_at,
            )
            for item in payload.get("values", [])
        ]

    def get_news(
        self,
        symbol: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[NewsArticle]:
        raise UnsupportedDataError("Twelve Data does not support market news")

from datetime import date, datetime, timezone
from decimal import Decimal

import httpx

from src.config.settings import settings
from src.data.base import FinancialDataProvider
from src.data.models import CompanyProfile, PriceBar


class TwelveDataProvider(FinancialDataProvider):
    """Twelve Data implementation of the normalized data-provider interface."""

    BASE_URL = "https://api.twelvedata.com"

    def __init__(self) -> None:
        if not settings.financial_data_api_key:
            raise ValueError("FINANCIAL_DATA_API_KEY is not configured")

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=20.0,
            params={"apikey": settings.financial_data_api_key},
        )

    def close(self) -> None:
        self.client.close()

    def search_company(self, query: str) -> list[CompanyProfile]:
        response = self.client.get(
            "/symbol_search",
            params={"symbol": query},
        )
        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "ok":
            raise RuntimeError(payload.get("message", "Twelve Data request failed"))

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
            if (
                company.symbol.upper() == ticker.upper()
                and (
                    exchange is None
                    or (company.exchange or "").upper() == exchange
                )
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

        response = self.client.get(
            "/time_series",
            params=params,
        )
        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "ok":
            raise RuntimeError(
                payload.get("message", "Twelve Data request failed")
            )

        retrieved_at = datetime.now(timezone.utc)

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
                retrieved_at=retrieved_at,
            )
            for item in payload.get("values", [])
        ]
    
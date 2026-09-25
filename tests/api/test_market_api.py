from datetime import date, datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from src.data.models import CompanyProfile, PriceBar
from src.main import app


client = TestClient(app)


class FakeMarketService:
    def get_profile(self, symbol: str) -> CompanyProfile:
        return CompanyProfile(
            symbol="RELIANCE.BSE",
            name="RELIANCE",
            exchange="BSE",
            country="India",
            sector="Energy",
            industry="Oil & Gas",
            currency="INR",
        )

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        return [
            PriceBar(
                symbol="RELIANCE:BSE",
                date=date(2026, 9, 24),
                open=Decimal("1238"),
                high=Decimal("1250"),
                low=Decimal("1230"),
                close=Decimal("1245"),
                volume=100000,
                adjusted_close=Decimal("1245"),
                source="test_provider",
                retrieved_at=datetime(2026, 9, 25),
            )
        ]

    def close(self):
        pass


class FailingMarketService:
    def get_profile(self, symbol: str):
        raise RuntimeError("Market data provider unavailable")

    def get_price_history(self, symbol, start, end):
        raise RuntimeError("Market data provider unavailable")

    def close(self):
        pass


def test_get_market_profile():
    from src.api import market

    original_factory = market.create_market_service
    market.create_market_service = lambda: FakeMarketService()

    try:
        response = client.get(
            "/api/market/RELIANCE:BSE/profile"
        )
    finally:
        market.create_market_service = original_factory

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "RELIANCE.BSE"
    assert data["name"] == "RELIANCE"
    assert data["exchange"] == "BSE"
    assert data["country"] == "India"
    assert data["currency"] == "INR"


def test_get_market_prices():
    from src.api import market

    original_factory = market.create_market_service
    market.create_market_service = lambda: FakeMarketService()

    try:
        response = client.get(
            "/api/market/RELIANCE:BSE/prices"
            "?start=2026-09-01"
            "&end=2026-09-24"
        )
    finally:
        market.create_market_service = original_factory

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "RELIANCE:BSE"
    assert data["start"] == "2026-09-01"
    assert data["end"] == "2026-09-24"
    assert data["count"] == 1

    assert data["data"][0]["date"] == "2026-09-24"
    assert Decimal(data["data"][0]["close"]) == Decimal("1245")
    assert data["data"][0]["source"] == "test_provider"


def test_get_market_prices_rejects_invalid_date_range():
    response = client.get(
        "/api/market/RELIANCE:BSE/prices"
        "?start=2026-09-24"
        "&end=2026-09-01"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "start date must be before or equal to end date"
    )


def test_get_market_profile_returns_502_on_service_failure():
    from src.api import market

    original_factory = market.create_market_service
    market.create_market_service = lambda: FailingMarketService()

    try:
        response = client.get(
            "/api/market/RELIANCE:BSE/profile"
        )
    finally:
        market.create_market_service = original_factory

    assert response.status_code == 502

    data = response.json()

    assert data["detail"] == "Market data provider unavailable"


def test_get_market_prices_returns_502_on_service_failure():
    from src.api import market

    original_factory = market.create_market_service
    market.create_market_service = lambda: FailingMarketService()

    try:
        response = client.get(
            "/api/market/RELIANCE:BSE/prices"
            "?start=2026-09-01"
            "&end=2026-09-24"
        )
    finally:
        market.create_market_service = original_factory

    assert response.status_code == 502

    data = response.json()

    assert data["detail"] == "Market data provider unavailable"
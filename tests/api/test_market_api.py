from datetime import date, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from src.api import market
from src.data.errors import (
    ProviderAuthenticationError,
    ProviderConfigurationError,
    ProviderInvalidRequestError,
    ProviderServerError,
    RateLimitError,
    TemporaryProviderError,
    UnsupportedDataError,
)
from src.data.models import CompanyProfile, PriceBar
from src.main import app

client = TestClient(app)


class FakeMarketService:
    def __init__(self, error=None):
        self.data_service = self
        self.error = error
        self.closed = False

    def get_profile(self, symbol: str) -> CompanyProfile:
        if self.error:
            raise self.error

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
        if self.error:
            raise self.error

        return [
            PriceBar(
                symbol="RELIANCE:BSE",
                date=date(2026, 9, 24),
                open=Decimal(1238),
                high=Decimal(1250),
                low=Decimal(1230),
                close=Decimal(1245),
                volume=100000,
                adjusted_close=Decimal(1245),
                source="test_provider",
                retrieved_at=datetime(2026, 9, 25),
            )
        ]

    def search_company(self, query: str) -> list[CompanyProfile]:
        if self.error:
            raise self.error
        return self.results

    @property
    def results(self):
        return getattr(self, "_results", [])

    @results.setter
    def results(self, value):
        self._results = value

    def close(self):
        self.closed = True


@pytest.fixture
def install_market_service(monkeypatch):
    """Install a fake market service and return it for assertions."""

    def install(service):
        monkeypatch.setattr(market, "create_market_service", lambda: service)
        return service

    return install


def test_get_market_profile(install_market_service):
    install_market_service(FakeMarketService())

    response = client.get("/api/market/RELIANCE:BSE/profile")

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE.BSE"
    assert data["name"] == "RELIANCE"
    assert data["exchange"] == "BSE"
    assert data["country"] == "India"
    assert data["currency"] == "INR"


def test_get_market_prices(install_market_service):
    install_market_service(FakeMarketService())

    response = client.get(
        "/api/market/RELIANCE:BSE/prices?start=2026-09-01&end=2026-09-24"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE:BSE"
    assert data["start"] == "2026-09-01"
    assert data["end"] == "2026-09-24"
    assert data["count"] == 1
    assert data["data"][0]["date"] == "2026-09-24"
    assert Decimal(data["data"][0]["close"]) == Decimal(1245)
    assert data["data"][0]["source"] == "test_provider"


def test_get_market_prices_rejects_invalid_date_range():
    response = client.get(
        "/api/market/RELIANCE:BSE/prices?start=2026-09-24&end=2026-09-01"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "start date must be before or equal to end date"
    )


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/api/market/RELIANCE:BSE/profile", "profile"),
        (
            "/api/market/RELIANCE:BSE/prices?start=2026-09-01&end=2026-09-24",
            "prices",
        ),
        ("/api/market/search?q=Apple", "search"),
    ],
)
@pytest.mark.parametrize(
    "error",
    [
        RateLimitError("Rate limit reached"),
        TemporaryProviderError("Provider temporarily unavailable"),
        ProviderServerError("Provider server error"),
        UnsupportedDataError("Requested data is unsupported"),
        ProviderAuthenticationError("Provider authentication failed"),
        ProviderConfigurationError("Provider configuration error"),
        ProviderInvalidRequestError("Invalid provider request"),
    ],
)
def test_market_endpoints_return_502_and_close_service(
    install_market_service, path, method, error
):
    service = FakeMarketService(error=error)
    install_market_service(service)

    response = client.get(path)

    assert response.status_code == 502
    assert response.json()["detail"] == str(error)
    assert service.closed is True


def test_market_profile_returns_502_on_runtime_failure(install_market_service):
    service = FakeMarketService(error=RuntimeError("Market data provider unavailable"))
    install_market_service(service)

    response = client.get("/api/market/RELIANCE:BSE/profile")

    assert response.status_code == 502
    assert response.json()["detail"] == "Market data provider unavailable"
    assert service.closed is True


def test_market_prices_returns_502_on_runtime_failure(install_market_service):
    service = FakeMarketService(error=RuntimeError("Market data provider unavailable"))
    install_market_service(service)

    response = client.get(
        "/api/market/RELIANCE:BSE/prices?start=2026-09-01&end=2026-09-24"
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "Market data provider unavailable"
    assert service.closed is True


def test_market_search_rejects_whitespace_query():
    response = client.get("/api/market/search?q=%20%20")

    assert response.status_code == 422


def test_market_search_limits_results_to_20(install_market_service):
    service = FakeMarketService()
    service.results = [
        CompanyProfile(
            symbol=f"TEST{i}",
            name=f"Test Company {i}",
            exchange="TEST",
            country="Test",
            sector=None,
            industry=None,
            currency="USD",
        )
        for i in range(25)
    ]
    install_market_service(service)

    response = client.get("/api/market/search?q=Test")

    assert response.status_code == 200
    assert len(response.json()) == 20
    assert service.closed is True

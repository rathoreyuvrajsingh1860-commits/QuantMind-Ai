from datetime import date, datetime
from decimal import Decimal
from unittest.mock import patch

from src.data.market_service import MarketService
from src.data.models import CompanyProfile, PriceBar


class FakeDataService:
    def __init__(self):
        self.price_history_calls = 0
        self.profile_calls = 0

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        self.profile_calls += 1
        return CompanyProfile(
            symbol="RELIANCE.BSE",
            name="RELIANCE",
            exchange="BSE",
            country="India",
            currency="INR",
        )

    def get_price_history(self, symbol, start, end):
        self.price_history_calls += 1

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
                source="fake_provider",
                retrieved_at=datetime(2026, 9, 25),
            )
        ]

    def close(self):
        pass


class FakeRepository:
    def __init__(self, stored_rows=None):
        self.stored_rows = stored_rows or []
        self.instrument_id = "test-instrument"

    def get_instrument_id(self, symbol, exchange):
        return self.instrument_id

    def get_price_history_coverage(self, instrument_id):
        if not self.stored_rows:
            return None

        dates = [row["date"] for row in self.stored_rows]

        return min(dates), max(dates)

    def get_price_history(self, instrument_id, start, end):
        return [
            row
            for row in self.stored_rows
            if start <= row["date"] <= end
        ]

def test_market_service_returns_stored_data_without_provider_fetch():
    stored_rows = [
        {
            "date": date(2026, 9, 24),
            "open": Decimal("1238"),
            "high": Decimal("1250"),
            "low": Decimal("1230"),
            "close": Decimal("1245"),
            "volume": 100000,
            "adjusted_close": Decimal("1245"),
            "source": "alpha_vantage",
            "retrieved_at": datetime(2026, 9, 25),
        }
    ]

    data_service = FakeDataService()
    repository = FakeRepository(stored_rows)

    service = MarketService(data_service, repository)

    result = service.get_price_history(
        "RELIANCE:BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
    )

    assert len(result) == 1
    assert result[0].close == Decimal("1245")
    assert result[0].source == "alpha_vantage"

    # Critical database-first behavior:
    # existing database data should prevent a provider call.
    assert data_service.price_history_calls == 0


def test_market_service_fetches_when_database_has_no_data():
    data_service = FakeDataService()
    repository = FakeRepository([])

    service = MarketService(data_service, repository)

    stored_row = {
        "date": date(2026, 9, 24),
        "open": Decimal("1238"),
        "high": Decimal("1250"),
        "low": Decimal("1230"),
        "close": Decimal("1245"),
        "volume": 100000,
        "adjusted_close": Decimal("1245"),
        "source": "fake_provider",
        "retrieved_at": datetime(2026, 9, 25),
    }

    def fake_ingest(*args, **kwargs):
        repository.stored_rows = [stored_row]
        return 1

    with patch(
        "src.data.market_service.ingest_price_history",
        side_effect=fake_ingest,
    ):
        result = service.get_price_history(
            "RELIANCE:BSE",
            date(2026, 9, 1),
            date(2026, 9, 24),
        )

    assert len(result) == 1
    assert result[0].close == Decimal("1245")
    assert result[0].source == "fake_provider"
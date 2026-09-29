from datetime import date, datetime, timezone
from decimal import Decimal

from src.data.models import CompanyProfile, PriceBar
from src.research.service import ResearchService


class FakeMarketService:
    def get_profile(self, symbol):
        return CompanyProfile(
            symbol="RELIANCE.BSE",
            name="Reliance Industries",
            exchange="BSE",
            country="India",
            sector="Energy",
            industry="Oil & Gas",
            currency="INR",
        )

    def get_price_history(self, symbol, start, end):
        retrieved_at = datetime(
            2026,
            9,
            30,
            tzinfo=timezone.utc,
        )

        return [
            PriceBar(
                symbol=symbol,
                date=date(2026, 1, 1),
                open=Decimal("100"),
                high=Decimal("110"),
                low=Decimal("95"),
                close=Decimal("100"),
                volume=1000,
                adjusted_close=None,
                source="test-provider",
                retrieved_at=retrieved_at,
            ),
            PriceBar(
                symbol=symbol,
                date=date(2026, 6, 1),
                open=Decimal("120"),
                high=Decimal("130"),
                low=Decimal("115"),
                close=Decimal("125"),
                volume=2000,
                adjusted_close=None,
                source="test-provider",
                retrieved_at=retrieved_at,
            ),
        ]

    def close(self):
        pass


def test_research_service_builds_market_research():
    service = ResearchService(
        FakeMarketService()
    )

    result = service.research(
        "RELIANCE:BSE",
        start=date(2026, 1, 1),
        end=date(2026, 6, 1),
    )

    assert result.entity.name == "Reliance Industries"
    assert result.entity.symbol == "RELIANCE.BSE"

    assert result.market.observations == 2
    assert result.market.first_close == Decimal("100")
    assert result.market.latest_close == Decimal("125")
    assert result.market.absolute_change == Decimal("25")
    assert result.market.percentage_change == Decimal("25.00")
    assert result.market.period_high == Decimal("130")
    assert result.market.period_low == Decimal("95")
    assert result.market.average_close == Decimal("112.50")
    assert result.market.total_volume == 3000

    assert len(result.evidence) == 2
    assert result.evidence[0].source == "test-provider"


def test_research_service_rejects_empty_query():
    service = ResearchService(
        FakeMarketService()
    )

    try:
        service.research("")
    except ValueError as exc:
        assert str(exc) == "Research query cannot be empty"
    else:
        raise AssertionError("Expected ValueError")

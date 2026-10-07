from datetime import UTC, date, datetime
from decimal import Decimal

from src.data.models import PriceBar
from src.research.models import MarketResearch
from src.verification.service import VerificationService


def make_prices() -> list[PriceBar]:
    return [
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 1),
            open=Decimal(1490),
            high=Decimal(1510),
            low=Decimal(1480),
            close=Decimal(1500),
            volume=1000,
            adjusted_close=Decimal(1500),
            source="alpha_vantage",
            retrieved_at=datetime.now(UTC),
        ),
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 2),
            open=Decimal(1510),
            high=Decimal(1530),
            low=Decimal(1500),
            close=Decimal(1520),
            volume=1200,
            adjusted_close=Decimal(1520),
            source="alpha_vantage",
            retrieved_at=datetime.now(UTC),
        ),
    ]


def make_valid_market() -> MarketResearch:
    return MarketResearch(
        start=date(2026, 9, 1),
        end=date(2026, 9, 2),
        observations=2,
        first_close=Decimal(1500),
        latest_close=Decimal(1520),
        absolute_change=Decimal(20),
        percentage_change=Decimal("1.33"),
        period_high=Decimal(1530),
        period_low=Decimal(1480),
        average_close=Decimal("1510.00"),
        total_volume=2200,
    )


def test_verification_passes_for_valid_research() -> None:
    result = VerificationService().verify_market_research(
        market=make_valid_market(),
        prices=make_prices(),
    )

    assert result.passed is True
    assert result.issues == []


def test_verification_detects_incorrect_calculation() -> None:
    market = make_valid_market()
    market.percentage_change = Decimal("2.50")

    result = VerificationService().verify_market_research(
        market=market,
        prices=make_prices(),
    )

    assert result.passed is False
    assert any(issue.field == "percentage_change" for issue in result.issues)


def test_verification_detects_incorrect_observation_count() -> None:
    market = make_valid_market()
    market.observations = 5

    result = VerificationService().verify_market_research(
        market=market,
        prices=make_prices(),
    )

    assert result.passed is False
    assert any(issue.field == "observations" for issue in result.issues)


def test_verification_handles_empty_prices() -> None:
    market = MarketResearch(
        start=date(2026, 9, 1),
        end=date(2026, 9, 2),
        observations=0,
    )

    result = VerificationService().verify_market_research(
        market=market,
        prices=[],
    )

    assert result.passed is True
    assert result.issues == []

from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from src.data.models import PriceBar
from src.main import app
from src.research.models import (
    MarketResearch,
    ResearchEntity,
    ResearchResult,
)
from src.verification.models import VerificationIssue, VerificationResult


client = TestClient(app)


def make_research() -> ResearchResult:
    return ResearchResult(
        query="RELIANCE:BSE",
        entity=ResearchEntity(
            symbol="RELIANCE:BSE",
            name="Reliance Industries",
            exchange="BSE",
            country="India",
            sector="Energy",
            industry="Oil & Gas",
            currency="INR",
        ),
        market=MarketResearch(
            start=date(2026, 9, 1),
            end=date(2026, 9, 24),
            observations=1,
            latest_close=Decimal("1245"),
            first_close=Decimal("1245"),
            absolute_change=Decimal("0"),
            percentage_change=Decimal("0"),
            period_high=Decimal("1250"),
            period_low=Decimal("1230"),
            average_close=Decimal("1245"),
            total_volume=100000,
        ),
        evidence=[],
        limitations=[],
    )


def test_research_api_skips_ai_when_verification_fails() -> None:
    research_service = MagicMock()
    research_service.research.return_value = make_research()
    research_service.last_prices = [
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

    verification = VerificationResult(
        passed=False,
        issues=[
            VerificationIssue(
                field="percentage_change",
                message="Verification failed.",
            )
        ],
    )

    verifier = MagicMock()
    verifier.verify_market_research.return_value = verification

    repository = MagicMock()
    repository.save_research.return_value = uuid4()

    with (
        patch(
            "src.api.research.create_research_service",
            return_value=research_service,
        ),
        patch(
            "src.api.research.VerificationService",
            return_value=verifier,
        ),
        patch(
            "src.api.research.ResearchRepository",
            return_value=repository,
        ),
        patch(
            "src.api.research.create_ai_research_service",
            side_effect=AssertionError(
                "AI service must not be created when verification fails"
            ),
        ),
    ):
        response = client.post(
            "/api/research",
            json={"query": "RELIANCE:BSE"},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["verification"]["passed"] is False
    assert data["ai_analysis"] is None

    repository.save_research.assert_called_once()

    save_kwargs = repository.save_research.call_args.kwargs

    assert save_kwargs["verification"].passed is False
    assert save_kwargs["status"] == "verification_failed"

    research_service.close.assert_called_once()
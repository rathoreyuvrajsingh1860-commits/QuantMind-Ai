from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from uuid import uuid4

from fastapi.testclient import TestClient

from src.data.models import PriceBar
from src.main import app
from src.research.models import (
    MarketResearch,
    ResearchCoverage,
    ResearchEntity,
    ResearchEvidence,
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
        coverage=ResearchCoverage(
        requested_start=date(2026, 9, 1),
        requested_end=date(2026, 9, 24),
        evidence_start=None,
        evidence_end=None,
        observations=0,
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

def test_research_api_marks_run_failed_on_unexpected_error() -> None:
    research_run_id = uuid4()

    research_service = MagicMock()
    research_service.research.side_effect = RuntimeError(
        "market provider unavailable"
    )

    repository = MagicMock()
    repository.create_research_run.return_value = research_run_id

    with (
        patch(
            "src.api.research.create_research_service",
            return_value=research_service,
        ),
        patch(
            "src.api.research.ResearchRepository",
            return_value=repository,
        ),
    ):
        with pytest.raises(RuntimeError, match="market provider unavailable"):
            client.post(
                "/api/research",
                json={"query": "RELIANCE:BSE"},
            )

    repository.create_research_run.assert_called_once_with(
        query="RELIANCE:BSE",
    )

    repository.update_research_run_status.assert_called_once_with(
        research_run_id,
        status="failed",
        metadata={"error": "market provider unavailable"},
    )

    repository.save_research.assert_not_called()
    research_service.close.assert_called_once()


def test_get_research_rejects_running_run() -> None:
    research_run_id = uuid4()

    repository = MagicMock()
    repository.get_research.return_value = {
        "id": research_run_id,
        "status": "running",
    }

    with patch(
        "src.api.research.ResearchRepository",
        return_value=repository,
    ):
        response = client.get(
            f"/api/research/{research_run_id}",
        )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Research run cannot be restored while its status is 'running'"
    )


def test_get_research_rejects_failed_run() -> None:
    research_run_id = uuid4()

    repository = MagicMock()
    repository.get_research.return_value = {
        "id": research_run_id,
        "status": "failed",
    }

    with patch(
        "src.api.research.ResearchRepository",
        return_value=repository,
    ):
        response = client.get(
            f"/api/research/{research_run_id}",
        )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Research run cannot be restored while its status is 'failed'"
    )


def test_get_research_reconstructs_legacy_coverage_from_evidence() -> None:
    research_run_id = uuid4()

    repository = MagicMock()
    repository.get_research.return_value = {
        "id": research_run_id,
        "query": "RELIANCE:BSE",
        "status": "completed",
        "model": None,
        "answer": None,
        "metadata": {
            "entity": {
                "symbol": "RELIANCE.BSE",
                "name": "RELIANCE",
                "exchange": "BSE",
                "country": "India",
                "sector": None,
                "industry": None,
                "currency": "INR",
            },
            "market": {
                "start": "2025-10-03",
                "end": "2026-10-03",
                "observations": 102,
                "latest_close": "1166.000000",
                "first_close": "1388.150000",
                "absolute_change": "-222.150000",
                "percentage_change": "-16.00",
                "period_high": "1427.450000",
                "period_low": "1161.000000",
                "average_close": "1298.33",
                "total_volume": 106769713,
            },
            "limitations": [
                "This research result contains market-data analysis only; it is not investment advice."
            ],
        },
        "evidence": [
            {
                "source_id": uuid4(),
                "title": None,
                "source_url": None,
                "excerpt": "First observation",
                "published_at": None,
                "retrieved_at": datetime(2026, 9, 30),
                "metadata": {
                    "source": "alpha_vantage",
                    "date": "2026-05-11",
                },
            },
            {
                "source_id": uuid4(),
                "title": None,
                "source_url": None,
                "excerpt": "Last observation",
                "published_at": None,
                "retrieved_at": datetime(2026, 10, 2),
                "metadata": {
                    "source": "alpha_vantage",
                    "date": "2026-10-01",
                },
            },
        ],
    }

    with patch(
        "src.api.research.ResearchRepository",
        return_value=repository,
    ):
        response = client.get(
            f"/api/research/{research_run_id}",
        )

    assert response.status_code == 200

    data = response.json()

    assert data["verification"] is None

    assert data["research"]["coverage"] == {
        "requested_start": "2025-10-03",
        "requested_end": "2026-10-03",
        "evidence_start": "2026-05-11",
        "evidence_end": "2026-10-01",
        "observations": 2,
    }

    assert (
        "Historical run predates coverage tracking"
        in data["research"]["limitations"][-1]
    )

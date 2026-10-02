from datetime import date, datetime
from decimal import Decimal

import pytest

from src.ai.base import AIProvider
from src.ai.models import AIMessage
from src.ai.service import AIResearchService
from src.research.models import (
    MarketResearch,
    ResearchCoverage,
    ResearchEntity,
    ResearchEvidence,
    ResearchResult,
)


class FakeAIProvider(AIProvider):
    name = "fake"

    def __init__(self, content: str) -> None:
        self.content = content
        self.received_user_prompt = ""

    def generate(self, *, system_prompt: str, user_prompt: str) -> AIMessage:
        self.received_user_prompt = user_prompt

        return AIMessage(
            content=self.content,
            model="fake-model",
            provider=self.name,
        )


def make_research() -> ResearchResult:
    return ResearchResult(
        query="RELIANCE",
        entity=ResearchEntity(
            symbol="RELIANCE:BSE",
            name="Reliance Industries",
            exchange="BSE",
            country="India",
            sector="Energy",
            industry="Integrated Oil & Gas",
            currency="INR",
        ),
        market=MarketResearch(
            start=date(2026, 1, 1),
            end=date(2026, 9, 1),
            observations=100,
            latest_close=Decimal("1500"),
            first_close=Decimal("1200"),
            absolute_change=Decimal("300"),
            percentage_change=Decimal("25"),
            period_high=Decimal("1550"),
            period_low=Decimal("1150"),
            average_close=Decimal("1350"),
            total_volume=1000000,
        ),
        evidence=[
            ResearchEvidence(
                source="alpha_vantage",
                retrieved_at=datetime(2026, 9, 1, 10, 0, 0),
                description="Historical market price observation.",
            )
        ],
        coverage=ResearchCoverage(
            requested_start=date(2026, 1, 1),
            requested_end=date(2026, 9, 1),
            evidence_start=date(2026, 9, 1),
            evidence_end=date(2026, 9, 1),
            observations=100,
        ),
        limitations=[],
    )

def test_ai_research_service_returns_structured_analysis() -> None:
    provider = FakeAIProvider(
        """
        {
          "executive_summary": "The supplied data shows a positive historical price change.",
          "key_findings": ["Price increased 25% over the supplied period."],
          "factual_observations": ["Latest close was 1500."],
          "interpretation": ["The supplied historical data indicates positive momentum over this period."],
          "risks": ["Historical performance does not establish future performance."],
          "uncertainty": ["No fundamental or news evidence was supplied."],
          "limitations": ["The analysis only covers the supplied market data."]
        }
        """
    )

    service = AIResearchService(provider)

    result = service.analyze(make_research())

    assert result.provider == "fake"
    assert result.model == "fake-model"
    assert result.analysis.executive_summary.startswith("The supplied data")
    assert result.analysis.key_findings
    assert "RELIANCE:BSE" in provider.received_user_prompt


def test_ai_research_service_rejects_invalid_json() -> None:
    provider = FakeAIProvider("not valid json")

    service = AIResearchService(provider)

    with pytest.raises(Exception, match="non-JSON"):
        service.analyze(make_research())


def test_ai_research_service_accepts_markdown_json_fence() -> None:
    provider = FakeAIProvider(
        """```json
        {
          "executive_summary": "Summary",
          "key_findings": [],
          "factual_observations": [],
          "interpretation": [],
          "risks": [],
          "uncertainty": [],
          "limitations": []
        }
        ```"""
    )

    result = AIResearchService(provider).analyze(make_research())

    assert result.analysis.executive_summary == "Summary"

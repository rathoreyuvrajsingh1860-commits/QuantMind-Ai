from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

from src.research.models import (
    MarketResearch,
    ResearchEntity,
    ResearchEvidence,
    ResearchResult,
)
from src.research.repositories.research import ResearchRepository


def make_research() -> ResearchResult:
    return ResearchResult(
        query="RELIANCE:BSE",
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
            observations=1,
            latest_close=Decimal("1500"),
            first_close=Decimal("1500"),
            absolute_change=Decimal("0"),
            percentage_change=Decimal("0"),
            period_high=Decimal("1500"),
            period_low=Decimal("1500"),
            average_close=Decimal("1500"),
            total_volume=1000,
        ),
        evidence=[
            ResearchEvidence(
                source="alpha_vantage",
                retrieved_at=datetime.now(timezone.utc),
                description="Daily market observation.",
            )
        ],
        limitations=[],
    )


def make_db_mocks(fetchone_values):
    connection = MagicMock()
    cursor = MagicMock()

    connection.__enter__.return_value = connection
    connection.__exit__.return_value = False

    connection.cursor.return_value.__enter__.return_value = cursor
    connection.cursor.return_value.__exit__.return_value = False

    cursor.fetchone.side_effect = fetchone_values

    return connection, cursor


def test_repository_persists_research_run() -> None:
    company_id = uuid4()
    instrument_id = uuid4()
    source_id = uuid4()
    research_run_id = uuid4()

    connection, cursor = make_db_mocks(
        [
            (company_id,),
            (instrument_id,),
            (source_id,),
            (research_run_id,),
        ]
    )

    with patch(
        "src.research.repositories.research.get_connection",
        return_value=connection,
    ):
        result = ResearchRepository().save_research(
            research=make_research(),
            prices=[],
        )

    assert result == research_run_id
    connection.commit.assert_called_once()

    sql_calls = [
        call.args[0]
        for call in cursor.execute.call_args_list
    ]

    assert any(
        "INSERT INTO research_runs" in sql
        for sql in sql_calls
    )


def test_repository_creates_evidence_for_prices() -> None:
    company_id = uuid4()
    instrument_id = uuid4()
    source_id = uuid4()
    research_run_id = uuid4()

    connection, cursor = make_db_mocks(
        [
            (company_id,),
            (instrument_id,),
            (source_id,),
            (research_run_id,),
        ]
    )

    from src.data.models import PriceBar

    price = PriceBar(
        symbol="RELIANCE:BSE",
        date=date(2026, 9, 1),
        open=Decimal("1490"),
        high=Decimal("1510"),
        low=Decimal("1480"),
        close=Decimal("1500"),
        volume=1000,
        adjusted_close=Decimal("1500"),
        source="alpha_vantage",
        retrieved_at=datetime.now(timezone.utc),
    )

    with patch(
        "src.research.repositories.research.get_connection",
        return_value=connection,
    ):
        ResearchRepository().save_research(
            research=make_research(),
            prices=[price],
        )

    sql_calls = [
        call.args[0]
        for call in cursor.execute.call_args_list
    ]

    assert any(
        "INSERT INTO evidence" in sql
        for sql in sql_calls
    )

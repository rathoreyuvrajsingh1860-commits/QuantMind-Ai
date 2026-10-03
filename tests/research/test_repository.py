from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

from src.data.models import PriceBar
from src.research.models import (
    MarketResearch,
    ResearchCoverage,
    ResearchEntity,
    ResearchEvidence,
    ResearchResult,
)
from src.research.repositories.research import ResearchRepository
from src.verification.models import VerificationResult


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
        coverage=ResearchCoverage(
            requested_start=date(2026, 1, 1),
            requested_end=date(2026, 9, 1),
            evidence_start=date(2026, 9, 1),
            evidence_end=date(2026, 9, 1),
            observations=1,
        ),
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


def test_repository_persists_research_run():
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


def test_repository_creates_evidence_for_prices():
    company_id = uuid4()
    instrument_id = uuid4()
    source_id = uuid4()
    research_run_id = uuid4()
    evidence_id = uuid4()

    connection, cursor = make_db_mocks(
        [
            (company_id,),
            (instrument_id,),
            (source_id,),
            (research_run_id,),
            (evidence_id,),  # evidence ID
            (uuid4(),),  # claim 1
            (uuid4(),),  # claim 2
            (uuid4(),),  # claim 3
            (uuid4(),),  # claim 4
            (uuid4(),),  # claim 5
            (uuid4(),),  # claim 6
            (uuid4(),),  # claim 7
            (uuid4(),),  # claim 8
        ]
    )
    cursor.fetchall.return_value = [(evidence_id,)]

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

    assert any(
        "INSERT INTO research_claims" in sql
        for sql in sql_calls
    )

    executemany_sql_calls = [
    call.args[0]
    for call in cursor.executemany.call_args_list
    ]

    assert any(
    "INSERT INTO claim_evidence" in sql
    for sql in executemany_sql_calls
    )


def test_repository_does_not_create_claims_when_verification_fails():
    company_id = uuid4()
    instrument_id = uuid4()
    source_id = uuid4()
    research_run_id = uuid4()
    evidence_id = uuid4()

    connection, cursor = make_db_mocks(
        [
            (company_id,),
            (instrument_id,),
            (source_id,),
            (research_run_id,),
            (evidence_id,),  # evidence ID
        ]
    )
    cursor.fetchall.return_value = [(evidence_id,)]

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

    verification = VerificationResult(
        passed=False,
        issues=[],
    )

    with patch(
        "src.research.repositories.research.get_connection",
        return_value=connection,
    ):
        ResearchRepository().save_research(
            research=make_research(),
            prices=[price],
            verification=verification,
        )

    sql_calls = [
        call.args[0]
        for call in cursor.execute.call_args_list
    ]

    assert not any(
        "INSERT INTO research_claims" in sql
        for sql in sql_calls
    )

    assert not any(
        "INSERT INTO claim_evidence" in sql
        for sql in sql_calls
    )

def test_repository_reuses_existing_data_source():
    existing_source_id = uuid4()

    connection, cursor = make_db_mocks(
        [
            (existing_source_id,),
        ]
    )

    research = make_research()

    result = ResearchRepository._ensure_sources(
        cursor,
        research=research,
    )

    assert result == {
        "alpha_vantage": existing_source_id,
    }

    sql_calls = [
        call.args[0]
        for call in cursor.execute.call_args_list
    ]

    assert any(
        "SELECT id" in sql
        and "FROM data_sources" in sql
        for sql in sql_calls
    )

    assert not any(
        "INSERT INTO data_sources" in sql
        for sql in sql_calls
    )
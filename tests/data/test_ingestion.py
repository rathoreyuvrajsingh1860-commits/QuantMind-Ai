from datetime import UTC, date, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from src.data.ingestion import (
    _log_price_quality_warnings,
    ingest_price_history,
)
from src.data.models import CompanyProfile, PriceBar


def test_ingestion_upsert_allows_legacy_null_retrieval_timestamp():
    retrieved_at = datetime.now(UTC)

    data_service = MagicMock()
    data_service.get_company_profile.return_value = CompanyProfile(
        symbol="RELIANCE.BSE",
        name="RELIANCE",
        exchange="BSE",
        country="India",
        currency="INR",
    )
    data_service.get_price_history.return_value = [
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 24),
            open=Decimal(1238),
            high=Decimal(1250),
            low=Decimal(1230),
            close=Decimal(1245),
            volume=100000,
            adjusted_close=Decimal(1245),
            source="alpha_vantage",
            retrieved_at=retrieved_at,
        )
    ]

    connection = MagicMock()
    cursor = MagicMock()
    connection.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchone.side_effect = [
        ("company-id",),
        ("instrument-id",),
    ]
    cursor.rowcount = 1

    with patch(
        "src.data.ingestion.get_connection",
        return_value=connection,
    ):
        result = ingest_price_history(
            data_service,
            "RELIANCE:BSE",
            date(2026, 9, 24),
            date(2026, 9, 24),
        )

    assert result == 1

    sql, parameters = cursor.executemany.call_args.args
    normalized_sql = " ".join(sql.split())

    assert (
        "WHERE price_history.retrieved_at IS NULL "
        "OR EXCLUDED.retrieved_at > price_history.retrieved_at"
    ) in normalized_sql

    assert len(parameters) == 1
    assert parameters[0][-1] == retrieved_at


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"high": Decimal(1220)}, "High price is inconsistent"),
        ({"low": Decimal(1260)}, "Low price is inconsistent"),
        ({"open": Decimal("-1")}, "Invalid open price"),
        ({"close": Decimal("-1")}, "Invalid close price"),
        ({"adjusted_close": Decimal(0)}, "Invalid adjusted_close price"),
        ({"volume": -1}, "Negative volume"),
        ({"date": date(2026, 9, 25)}, "outside requested range"),
    ],
)
def test_ingestion_rejects_invalid_price_bars_before_database_write(
    overrides,
    message,
):
    values = {
        "symbol": "RELIANCE:BSE",
        "date": date(2026, 9, 24),
        "open": Decimal(1238),
        "high": Decimal(1250),
        "low": Decimal(1230),
        "close": Decimal(1245),
        "volume": 100000,
        "adjusted_close": Decimal(1245),
        "source": "alpha_vantage",
        "retrieved_at": datetime.now(UTC),
    }
    values.update(overrides)

    data_service = MagicMock()
    data_service.get_company_profile.return_value = CompanyProfile(
        symbol="RELIANCE.BSE",
        name="RELIANCE",
        exchange="BSE",
        country="India",
        currency="INR",
    )
    data_service.get_price_history.return_value = [PriceBar(**values)]

    with (
        patch("src.data.ingestion.get_connection") as mock_connection,
        pytest.raises(ValueError, match=message),
    ):
        ingest_price_history(
            data_service,
            "RELIANCE:BSE",
            date(2026, 9, 24),
            date(2026, 9, 24),
        )

    mock_connection.assert_not_called()


def test_ingestion_rejects_duplicate_date_and_source_before_database_write():
    bar = PriceBar(
        symbol="RELIANCE:BSE",
        date=date(2026, 9, 24),
        open=Decimal(1238),
        high=Decimal(1250),
        low=Decimal(1230),
        close=Decimal(1245),
        volume=100000,
        adjusted_close=Decimal(1245),
        source="alpha_vantage",
        retrieved_at=datetime.now(UTC),
    )
    data_service = MagicMock()
    data_service.get_company_profile.return_value = CompanyProfile(
        symbol="RELIANCE.BSE",
        name="RELIANCE",
        exchange="BSE",
        country="India",
        currency="INR",
    )
    data_service.get_price_history.return_value = [bar, bar]

    with (
        patch("src.data.ingestion.get_connection") as mock_connection,
        pytest.raises(ValueError, match="Duplicate price bar"),
    ):
        ingest_price_history(
            data_service,
            "RELIANCE:BSE",
            date(2026, 9, 24),
            date(2026, 9, 24),
        )

    mock_connection.assert_not_called()


def test_price_quality_logs_missing_trading_sessions(caplog):
    profile = CompanyProfile(
        symbol="RELIANCE.BSE",
        name="RELIANCE",
        exchange="BSE",
    )
    bars = [
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 14),
            open=Decimal(100),
            high=Decimal(110),
            low=Decimal(95),
            close=Decimal(105),
            source="test_provider",
            retrieved_at=datetime.now(UTC),
        ),
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 16),
            open=Decimal(106),
            high=Decimal(112),
            low=Decimal(103),
            close=Decimal(110),
            source="test_provider",
            retrieved_at=datetime.now(UTC),
        ),
    ]

    _log_price_quality_warnings(bars, profile)

    assert "missing trading sessions" in caplog.text
    assert "datetime.date(2026, 9, 15)" in caplog.text


def test_price_quality_logs_large_daily_movement_without_rejecting(caplog):
    profile = CompanyProfile(
        symbol="RELIANCE.BSE",
        name="RELIANCE",
        exchange="BSE",
    )
    bars = [
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 14),
            open=Decimal(100),
            high=Decimal(105),
            low=Decimal(95),
            close=Decimal(100),
            source="test_provider",
            retrieved_at=datetime.now(UTC),
        ),
        PriceBar(
            symbol="RELIANCE:BSE",
            date=date(2026, 9, 15),
            open=Decimal(129),
            high=Decimal(135),
            low=Decimal(125),
            close=Decimal(130),
            source="test_provider",
            retrieved_at=datetime.now(UTC),
        ),
    ]

    _log_price_quality_warnings(bars, profile)

    assert "Unusually large daily price movement" in caplog.text
    assert "30.00" in caplog.text

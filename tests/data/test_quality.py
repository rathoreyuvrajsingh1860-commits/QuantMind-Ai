from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from src.data import quality
from src.data.quality import build_price_quality_report
from src.data.trading_calendar import UnsupportedTradingCalendarError


def make_row(
    day=date(2026, 9, 24),
    *,
    source="provider_a",
    open_price="100",
    high="105",
    low="95",
    close="102",
    adjusted_close="102",
    retrieved_at=None,
):
    return {
        "date": day,
        "source": source,
        "open": Decimal(open_price),
        "high": Decimal(high),
        "low": Decimal(low),
        "close": Decimal(close),
        "adjusted_close": Decimal(adjusted_close)
        if adjusted_close is not None
        else None,
        "retrieved_at": retrieved_at or datetime.now(UTC),
    }


def test_quality_report_returns_healthy_for_valid_complete_data(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [date(2026, 9, 24)],
    )

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [make_row()],
    )

    assert report["status"] == "healthy"
    assert report["observation_count"] == 1
    assert report["distinct_dates"] == 1
    assert report["expected_sessions"] == 1
    assert report["missing_sessions"] == 0
    assert report["findings"] == []


def test_quality_report_detects_invalid_ohlc(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [date(2026, 9, 24)],
    )

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [make_row(high="99")],
    )

    assert report["status"] == "error"
    assert any(item["code"] == "invalid_ohlc" for item in report["findings"])


def test_quality_report_detects_duplicate_observations(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [],
    )
    row = make_row()

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [row, row.copy()],
    )

    assert report["status"] == "error"
    assert any(item["code"] == "duplicate_observation" for item in report["findings"])


def test_quality_report_detects_missing_trading_sessions(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [
            date(2026, 9, 24),
            date(2026, 9, 25),
        ],
    )

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 25),
        [make_row()],
    )

    assert report["status"] == "warning"
    assert report["expected_sessions"] == 2
    assert report["missing_sessions"] == 1
    assert any(
        item["code"] == "missing_trading_session" and item["date"] == date(2026, 9, 25)
        for item in report["findings"]
    )


def test_quality_report_detects_large_movement_per_source(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [],
    )

    rows = [
        make_row(day=date(2026, 9, 24), close="100", adjusted_close="100"),
        make_row(
            day=date(2026, 9, 25),
            high="130",
            close="125",
            adjusted_close="125",
        ),
    ]

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 25),
        rows,
    )

    assert report["status"] == "warning"
    assert any(
        item["code"] == "large_daily_price_movement" for item in report["findings"]
    )


def test_quality_report_detects_stale_data(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [],
    )

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [make_row(retrieved_at=datetime.now(UTC) - timedelta(days=3))],
    )

    assert report["status"] == "warning"
    assert any(item["code"] == "stale_data" for item in report["findings"])


def test_quality_report_handles_unsupported_calendar(monkeypatch):
    def unsupported_calendar(start, end, exchange):
        raise UnsupportedTradingCalendarError("Unsupported exchange")

    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        unsupported_calendar,
    )

    report = build_price_quality_report(
        "UNKNOWN",
        "UNKNOWN",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [make_row()],
    )

    assert report["calendar_available"] is False
    assert report["expected_sessions"] is None
    assert report["missing_sessions"] is None
    assert any(
        item["code"] == "calendar_unavailable" and item["severity"] == "info"
        for item in report["findings"]
    )


def test_quality_report_returns_no_data_status(monkeypatch):
    monkeypatch.setattr(
        quality,
        "get_expected_trading_dates",
        lambda start, end, exchange: [],
    )

    report = build_price_quality_report(
        "RELIANCE.BSE",
        "BSE",
        date(2026, 9, 24),
        date(2026, 9, 24),
        [],
    )

    assert report["status"] == "no_data"
    assert report["observation_count"] == 0
    assert report["findings"] == []

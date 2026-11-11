from datetime import date

import pytest

from src.data.trading_calendar import get_expected_trading_dates


def test_bse_calendar_excludes_weekends():
    result = get_expected_trading_dates(
        date(2026, 10, 19),
        date(2026, 10, 24),
        "BSE",
    )

    assert result == [
        date(2026, 10, 19),
        date(2026, 10, 21),
        date(2026, 10, 22),
        date(2026, 10, 23),
    ]


def test_nyse_calendar_excludes_weekends():
    result = get_expected_trading_dates(
        date(2026, 10, 19),
        date(2026, 10, 24),
        "NYSE",
    )

    assert result == [
        date(2026, 10, 19),
        date(2026, 10, 20),
        date(2026, 10, 21),
        date(2026, 10, 22),
        date(2026, 10, 23),
    ]


@pytest.mark.parametrize(
    ("exchange", "expected"),
    [
        ("India/Bombay", "BSE"),
        ("Bombay Stock Exchange", "BSE"),
        ("BSE India", "BSE"),
        ("XBOM", "BSE"),
        ("NSE India", "NSE"),
        ("National Stock Exchange of India", "NSE"),
        ("XNSE", "NSE"),
        ("New York Stock Exchange", "NYSE"),
        ("XNYS", "NYSE"),
    ],
)
def test_exchange_aliases_use_verified_calendar(exchange, expected):
    canonical_dates = get_expected_trading_dates(
        date(2026, 10, 19), date(2026, 10, 24), expected
    )
    alias_dates = get_expected_trading_dates(
        date(2026, 10, 19), date(2026, 10, 24), exchange
    )
    assert alias_dates == canonical_dates


def test_country_only_exchange_is_not_assumed_to_be_nyse():
    with pytest.raises(ValueError, match="No verified trading calendar"):
        get_expected_trading_dates(
            date(2026, 10, 19), date(2026, 10, 24), "United States"
        )


@pytest.mark.parametrize("exchange", ["NASDAQ"])
def test_known_unsupported_exchange_raises(exchange):
    with pytest.raises(ValueError, match="No verified trading calendar"):
        get_expected_trading_dates(
            date(2026, 10, 19),
            date(2026, 10, 24),
            exchange,
        )


@pytest.mark.parametrize("exchange", ["UNKNOWN", None])
def test_unconfigured_exchange_requires_explicit_approximation(exchange):
    with pytest.raises(ValueError, match="No verified trading calendar"):
        get_expected_trading_dates(
            date(2026, 10, 19),
            date(2026, 10, 24),
            exchange,
        )


def test_weekday_approximation_requires_explicit_opt_in():
    result = get_expected_trading_dates(
        date(2026, 10, 19),
        date(2026, 10, 24),
        "UNKNOWN",
        allow_weekday_approximation=True,
    )
    assert len(result) == 5


def test_start_after_end_returns_empty():
    result = get_expected_trading_dates(
        date(2026, 10, 24),
        date(2026, 10, 19),
        "BSE",
    )

    assert result == []


def test_bse_date_outside_calendar_range_raises():
    with pytest.raises(ValueError, match="outside the supported"):
        get_expected_trading_dates(
            date(2000, 1, 1),
            date(2000, 1, 10),
            "BSE",
        )


@pytest.mark.parametrize(
    "holiday",
    [
        date(2025, 2, 26),
        date(2025, 10, 22),
        date(2026, 1, 15),
        date(2026, 3, 3),
        date(2026, 11, 10),
    ],
)
def test_nse_equity_calendar_excludes_official_weekday_holidays(holiday):
    assert get_expected_trading_dates(holiday, holiday, "NSE") == []


@pytest.mark.parametrize(
    "session",
    [
        date(2025, 10, 21),
        date(2026, 11, 8),
    ],
)
def test_nse_equity_calendar_includes_muhurat_special_sessions(session):
    assert get_expected_trading_dates(session, session, "NSE") == [session]


def test_nse_equity_calendar_excludes_regular_weekends():
    assert get_expected_trading_dates(
        date(2026, 11, 7),
        date(2026, 11, 9),
        "NSE",
    ) == [date(2026, 11, 8), date(2026, 11, 9)]


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (date(2024, 12, 30), date(2025, 1, 3)),
        (date(2026, 12, 30), date(2027, 1, 4)),
    ],
)
def test_nse_calendar_rejects_unverified_year_ranges(start, end):
    with pytest.raises(ValueError, match="verified only for 2025"):
        get_expected_trading_dates(start, end, "NSE")


def test_nse_equity_calendar_returns_regular_sessions():
    result = get_expected_trading_dates(
        date(2026, 11, 9),
        date(2026, 11, 13),
        "NSE",
    )
    assert result == [
        date(2026, 11, 9),
        date(2026, 11, 11),
        date(2026, 11, 12),
        date(2026, 11, 13),
    ]

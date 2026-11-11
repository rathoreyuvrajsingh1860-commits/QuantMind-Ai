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


@pytest.mark.parametrize("exchange", ["NSE", "NASDAQ"])
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

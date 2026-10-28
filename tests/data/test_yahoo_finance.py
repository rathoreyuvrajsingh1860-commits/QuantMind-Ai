from datetime import date
from unittest.mock import Mock

import pandas as pd
import pytest

from src.data.base import DataCapability
from src.data.errors import ProviderServerError, UnsupportedDataError
from src.data.providers.yahoo_finance import YahooFinanceProvider


@pytest.mark.parametrize(
    ("symbol", "expected"),
    [
        ("RELIANCE:NSE", "RELIANCE.NS"),
        ("RELIANCE:BSE", "RELIANCE.BO"),
        ("AAPL:NASDAQ", "AAPL"),
        ("IBM:NYSE", "IBM"),
        ("RELIANCE", "RELIANCE"),
    ],
)
def test_symbol_mapping(symbol, expected):
    assert YahooFinanceProvider._normalize_symbol(symbol) == expected


def test_capabilities_are_price_history_only():
    assert YahooFinanceProvider().capabilities == {DataCapability.PRICE_HISTORY}


def test_price_history_normalizes_rows(monkeypatch):
    frame = pd.DataFrame(
        {
            "Open": [100.0],
            "High": [110.0],
            "Low": [95.0],
            "Close": [105.0],
            "Adj Close": [104.0],
            "Volume": [1234],
        },
        index=pd.to_datetime(["2026-10-08"]),
    )
    ticker = Mock()
    ticker.history.return_value = frame
    monkeypatch.setattr(
        "src.data.providers.yahoo_finance.yf.Ticker", Mock(return_value=ticker)
    )

    bars = YahooFinanceProvider().get_price_history(
        "RELIANCE:NSE", date(2026, 10, 8), date(2026, 10, 8)
    )

    assert len(bars) == 1
    assert bars[0].symbol == "RELIANCE:NSE"
    assert bars[0].close == 105
    assert bars[0].adjusted_close == 104
    assert bars[0].source == "yahoo_finance"
    assert bars[0].volume == 1234
    ticker.history.assert_called_once_with(
        start="2026-10-08",
        end="2026-10-09",
        interval="1d",
        auto_adjust=False,
        actions=False,
        raise_errors=True,
    )


def test_empty_history_is_fallback_eligible(monkeypatch):
    ticker = Mock()
    ticker.history.return_value = pd.DataFrame()
    monkeypatch.setattr(
        "src.data.providers.yahoo_finance.yf.Ticker", Mock(return_value=ticker)
    )

    with pytest.raises(UnsupportedDataError):
        YahooFinanceProvider().get_price_history(
            "RELIANCE:NSE", date(2026, 10, 8), date(2026, 10, 8)
        )


def test_request_failure_is_fallback_eligible(monkeypatch):
    ticker = Mock()
    ticker.history.side_effect = RuntimeError("network unavailable")
    monkeypatch.setattr(
        "src.data.providers.yahoo_finance.yf.Ticker", Mock(return_value=ticker)
    )

    with pytest.raises(ProviderServerError):
        YahooFinanceProvider().get_price_history(
            "RELIANCE:NSE", date(2026, 10, 8), date(2026, 10, 8)
        )


def test_price_history_skips_rows_with_nan_close(monkeypatch):
    frame = pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [110.0, 111.0],
            "Low": [95.0, 96.0],
            "Close": [float("nan"), 105.0],
            "Adj Close": [float("nan"), 104.0],
            "Volume": [1234, 5678],
        },
        index=pd.to_datetime(["2026-10-07", "2026-10-08"]),
    )
    ticker = Mock()
    ticker.history.return_value = frame
    monkeypatch.setattr(
        "src.data.providers.yahoo_finance.yf.Ticker", Mock(return_value=ticker)
    )

    bars = YahooFinanceProvider().get_price_history(
        "RELIANCE:NSE", date(2026, 10, 7), date(2026, 10, 8)
    )

    assert len(bars) == 1
    assert bars[0].date == date(2026, 10, 8)
    assert bars[0].close == 105


def test_price_history_rejects_incomplete_historical_coverage(monkeypatch):
    frame = pd.DataFrame(
        {
            "Open": [1400.0],
            "High": [1420.0],
            "Low": [1390.0],
            "Close": [1410.0],
            "Adj Close": [1405.0],
            "Volume": [1000],
        },
        index=pd.to_datetime(["2026-10-22"]),
    )

    ticker = Mock()
    ticker.history.return_value = frame
    monkeypatch.setattr(
        "src.data.providers.yahoo_finance.yf.Ticker",
        Mock(return_value=ticker),
    )

    with pytest.raises(
        UnsupportedDataError,
        match="does not cover the requested start date",
    ):
        YahooFinanceProvider().get_price_history(
            "RELIANCE:BSE",
            date(2025, 10, 22),
            date(2026, 10, 22),
        )

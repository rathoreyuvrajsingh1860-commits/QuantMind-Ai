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

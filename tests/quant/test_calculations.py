from datetime import date
from decimal import Decimal
from datetime import datetime, timezone

from src.data.models import PriceBar
from src.quant.calculations import calculate_market_metrics


def make_price(
    *,
    trading_date: date,
    close: str,
    high: str,
    low: str,
    volume: int | None,
) -> PriceBar:
    return PriceBar(
        symbol="RELIANCE:BSE",
        date=trading_date,
        open=Decimal(close),
        high=Decimal(high),
        low=Decimal(low),
        close=Decimal(close),
        volume=volume,
        adjusted_close=Decimal(close),
        source="alpha_vantage",
        retrieved_at=datetime.now(timezone.utc),
    )


def test_calculate_market_metrics() -> None:
    prices = [
        make_price(
            trading_date=date(2026, 1, 1),
            close="100",
            high="110",
            low="90",
            volume=1000,
        ),
        make_price(
            trading_date=date(2026, 1, 2),
            close="110",
            high="120",
            low="95",
            volume=2000,
        ),
    ]

    result = calculate_market_metrics(prices)

    assert result == {
        "observations": 2,
        "first_close": Decimal("100"),
        "latest_close": Decimal("110"),
        "absolute_change": Decimal("10"),
        "percentage_change": Decimal("10.00"),
        "period_high": Decimal("120"),
        "period_low": Decimal("90"),
        "average_close": Decimal("105.00"),
        "total_volume": 3000,
    }


def test_calculate_market_metrics_handles_empty_prices() -> None:
    result = calculate_market_metrics([])

    assert result == {
        "observations": 0,
        "first_close": None,
        "latest_close": None,
        "absolute_change": None,
        "percentage_change": None,
        "period_high": None,
        "period_low": None,
        "average_close": None,
        "total_volume": None,
    }


def test_calculate_market_metrics_handles_zero_first_close() -> None:
    prices = [
        make_price(
            trading_date=date(2026, 1, 1),
            close="0",
            high="10",
            low="0",
            volume=100,
        ),
        make_price(
            trading_date=date(2026, 1, 2),
            close="10",
            high="15",
            low="5",
            volume=200,
        ),
    ]

    result = calculate_market_metrics(prices)

    assert result["percentage_change"] is None


def test_calculate_market_metrics_ignores_missing_volume() -> None:
    prices = [
        make_price(
            trading_date=date(2026, 1, 1),
            close="100",
            high="110",
            low="90",
            volume=None,
        ),
        make_price(
            trading_date=date(2026, 1, 2),
            close="110",
            high="120",
            low="95",
            volume=2000,
        ),
    ]

    result = calculate_market_metrics(prices)

    assert result["total_volume"] == 2000

from decimal import ROUND_HALF_UP, Decimal

from src.data.models import PriceBar


def calculate_market_metrics(
    prices: list[PriceBar],
) -> dict[str, int | Decimal | None]:
    """Calculate deterministic market metrics from price observations."""

    if not prices:
        return {
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

    first_close = prices[0].close
    latest_close = prices[-1].close

    absolute_change = latest_close - first_close

    if first_close != 0:
        percentage_change = (absolute_change / first_close * Decimal(100)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    else:
        percentage_change = None

    period_high = max(bar.high for bar in prices)
    period_low = min(bar.low for bar in prices)

    average_close = (
        sum(
            (bar.close for bar in prices),
            Decimal(0),
        )
        / len(prices)
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    volumes = [bar.volume for bar in prices if bar.volume is not None]

    total_volume = sum(volumes) if volumes else None

    return {
        "observations": len(prices),
        "first_close": first_close,
        "latest_close": latest_close,
        "absolute_change": absolute_change,
        "percentage_change": percentage_change,
        "period_high": period_high,
        "period_low": period_low,
        "average_close": average_close,
        "total_volume": total_volume,
    }

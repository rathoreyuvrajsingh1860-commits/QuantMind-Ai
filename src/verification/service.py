from decimal import Decimal, ROUND_HALF_UP

from src.data.models import PriceBar
from src.research.models import MarketResearch
from src.verification.models import (
    VerificationIssue,
    VerificationResult,
)


class VerificationService:
    """Deterministically verifies research calculations against price data."""

    def verify_market_research(
        self,
        *,
        market: MarketResearch,
        prices: list[PriceBar],
    ) -> VerificationResult:
        issues: list[VerificationIssue] = []

        if market.observations != len(prices):
            issues.append(
                VerificationIssue(
                    field="observations",
                    message=(
                        f"Expected {len(prices)} observations, "
                        f"got {market.observations}."
                    ),
                )
            )

        if not prices:
            return VerificationResult(
                passed=not issues,
                issues=issues,
            )

        first_close = prices[0].close
        latest_close = prices[-1].close
        absolute_change = latest_close - first_close

        if first_close != 0:
            percentage_change = (
                absolute_change / first_close * Decimal("100")
            ).quantize(
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
                Decimal("0"),
            )
            / len(prices)
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        volumes = [
            bar.volume
            for bar in prices
            if bar.volume is not None
        ]

        total_volume = sum(volumes) if volumes else None

        expected_values = {
            "first_close": first_close,
            "latest_close": latest_close,
            "absolute_change": absolute_change,
            "percentage_change": percentage_change,
            "period_high": period_high,
            "period_low": period_low,
            "average_close": average_close,
            "total_volume": total_volume,
        }

        actual_values = {
            "first_close": market.first_close,
            "latest_close": market.latest_close,
            "absolute_change": market.absolute_change,
            "percentage_change": market.percentage_change,
            "period_high": market.period_high,
            "period_low": market.period_low,
            "average_close": market.average_close,
            "total_volume": market.total_volume,
        }

        for field, expected in expected_values.items():
            actual = actual_values[field]

            if actual != expected:
                issues.append(
                    VerificationIssue(
                        field=field,
                        message=(
                            f"Expected {expected}, got {actual}."
                        ),
                    )
                )

        return VerificationResult(
            passed=not issues,
            issues=issues,
        )
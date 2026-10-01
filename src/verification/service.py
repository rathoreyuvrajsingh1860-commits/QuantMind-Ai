from src.data.models import PriceBar
from src.quant.calculations import calculate_market_metrics
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

        metrics = calculate_market_metrics(prices)

        expected_values = {
            "observations": metrics["observations"],
            "first_close": metrics["first_close"],
            "latest_close": metrics["latest_close"],
            "absolute_change": metrics["absolute_change"],
            "percentage_change": metrics["percentage_change"],
            "period_high": metrics["period_high"],
            "period_low": metrics["period_low"],
            "average_close": metrics["average_close"],
            "total_volume": metrics["total_volume"],
        }

        actual_values = {
            "observations": market.observations,
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
                        message=f"Expected {expected}, got {actual}.",
                    )
                )

        return VerificationResult(
            passed=not issues,
            issues=issues,
        )

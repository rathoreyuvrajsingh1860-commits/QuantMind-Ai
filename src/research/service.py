from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from src.data.market_service import MarketService
from src.research.models import (
    MarketResearch,
    ResearchEntity,
    ResearchEvidence,
    ResearchResult,
)


class ResearchService:
    """Application service for QuantMind research workflows."""

    def __init__(self, market_service: MarketService):
        self.market_service = market_service

    def _default_date_range(self) -> tuple[date, date]:
        end = date.today()
        start = end - timedelta(days=365)

        return start, end

    def research(
        self,
        query: str,
        *,
        start: date | None = None,
        end: date | None = None,
    ) -> ResearchResult:
        """Build a deterministic, evidence-backed research result."""

        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError("Research query cannot be empty")

        symbol = normalized_query

        if ":" not in symbol:
            symbol = f"{symbol}:BSE"

        start_date, end_date = (
            start,
            end,
        )

        if start_date is None or end_date is None:
            default_start, default_end = self._default_date_range()
            start_date = start_date or default_start
            end_date = end_date or default_end

        if start_date > end_date:
            raise ValueError("Research start date cannot be after end date")

        profile = self.market_service.get_profile(symbol)

        prices = self.market_service.get_price_history(
            symbol,
            start_date,
            end_date,
        )

        if prices:
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
                sum((bar.close for bar in prices), Decimal("0"))
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

            latest_retrieved_at = max(
                bar.retrieved_at
                for bar in prices
            )
        else:
            first_close = None
            latest_close = None
            absolute_change = None
            percentage_change = None
            period_high = None
            period_low = None
            average_close = None
            total_volume = None
            latest_retrieved_at = None

        market = MarketResearch(
            start=start_date,
            end=end_date,
            observations=len(prices),
            latest_close=latest_close,
            first_close=first_close,
            absolute_change=absolute_change,
            percentage_change=percentage_change,
            period_high=period_high,
            period_low=period_low,
            average_close=average_close,
            total_volume=total_volume,
        )

        evidence = [
            ResearchEvidence(
                source=bar.source,
                retrieved_at=bar.retrieved_at,
                description=(
                    f"Daily market data for {profile.symbol} "
                    f"on {bar.date.isoformat()}"
                ),
            )
            for bar in prices
        ]

        limitations: list[str] = []

        if not prices:
            limitations.append(
                "No market observations were available for the requested period."
            )

        limitations.append(
            "This research result contains market-data analysis only; "
            "it is not investment advice."
        )

        return ResearchResult(
            query=query,
            entity=ResearchEntity(
                symbol=profile.symbol,
                name=profile.name,
                exchange=profile.exchange,
                country=profile.country,
                sector=profile.sector,
                industry=profile.industry,
                currency=profile.currency,
            ),
            market=market,
            evidence=evidence,
            limitations=limitations,
        )

    def close(self) -> None:
        self.market_service.close()

from datetime import date, timedelta

from src.data.market_service import MarketService
from src.data.models import PriceBar
from src.quant.calculations import calculate_market_metrics
from src.research.models import (
    MarketResearch,
    ResearchCoverage,
    ResearchEntity,
    ResearchEvidence,
    ResearchResult,
)


class ResearchService:
    """Application service for QuantMind research workflows."""

    def __init__(self, market_service: MarketService):
        self.market_service = market_service
        self.last_prices: list[PriceBar] = []

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

        symbol = normalized_query.upper()

        if ":" in symbol:
            symbol_part, exchange_part = symbol.split(":", 1)
            symbol = f"{symbol_part.strip()}:{exchange_part.strip()}"
        else:
            symbol = symbol.strip()

        if start is None or end is None:
            default_start, default_end = self._default_date_range()
            start = start or default_start
            end = end or default_end

        if start > end:
            raise ValueError(
                "Research start date cannot be after end date"
            )

        profile = self.market_service.get_profile(symbol)
        resolved_symbol = profile.symbol

        prices = self.market_service.get_price_history(
            resolved_symbol,
            start,
            end,
        )

        self.last_prices = prices

        metrics = calculate_market_metrics(prices)

        first_close = metrics["first_close"]
        latest_close = metrics["latest_close"]
        absolute_change = metrics["absolute_change"]
        percentage_change = metrics["percentage_change"]
        period_high = metrics["period_high"]
        period_low = metrics["period_low"]
        average_close = metrics["average_close"]
        total_volume = metrics["total_volume"]
        market = MarketResearch(

            start=start,
            end=end,
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
                source_url=bar.source_url,
                retrieved_at=bar.retrieved_at,
                description=(
                    f"Daily market data for {profile.symbol} "
                    f"on {bar.date.isoformat()}"
                ),
            )
            for bar in prices
        ]

        limitations: list[str] = []

        coverage = ResearchCoverage(
        requested_start=start,
        requested_end=end,
        evidence_start=prices[0].date if prices else None,
        evidence_end=prices[-1].date if prices else None,
        observations=len(prices),
        )

        if not prices:
            limitations.append(
                "No market observations were available "
                "for the requested period."
            )

        limitations.append(
            "This research result contains market-data analysis "
            "only; it is not investment advice."
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
            coverage=coverage,
            limitations=limitations,
        )

    def close(self) -> None:
        self.market_service.close()

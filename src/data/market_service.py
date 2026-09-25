from datetime import date

from src.data.ingestion import ingest_price_history
from src.data.models import CompanyProfile, PriceBar
from src.data.service import DataService
from src.storage.repositories.market import MarketRepository


class MarketService:
    """Application service for market data retrieval."""

    def __init__(
        self,
        data_service: DataService,
        repository: MarketRepository | None = None,
    ):
        self.data_service = data_service
        self.repository = repository or MarketRepository()

    def get_profile(self, symbol: str) -> CompanyProfile:
        return self.data_service.get_company_profile(symbol)

    def _rows_to_price_bars(
        self,
        symbol: str,
        rows: list[dict],
    ) -> list[PriceBar]:
        return [
            PriceBar(
                symbol=symbol,
                date=row["date"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"],
                adjusted_close=row["adjusted_close"],
                source=row["source"],
                retrieved_at=row["retrieved_at"],
            )
            for row in rows
        ]

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        profile = self.get_profile(symbol)

        instrument_id = self.repository.get_instrument_id(
            profile.symbol,
            profile.exchange,
        )

        if instrument_id is not None:
            coverage = self.repository.get_price_history_coverage(
                instrument_id,
            )

            if coverage is not None:
                earliest, latest = coverage

                if earliest <= start and latest >= end:
                    missing_dates = (
                        self.repository.get_missing_expected_price_dates(
                            instrument_id,
                            start,
                            end,
                        )
                    )

                    if not missing_dates:
                        stored = self.repository.get_price_history(
                            instrument_id,
                            start,
                            end,
                        )

                        return self._rows_to_price_bars(
                            symbol,
                            stored,
                        )

        # Coverage is absent, incomplete, or contains an expected gap.
        ingest_price_history(
            self.data_service,
            symbol,
            start,
            end,
        )

        instrument_id = self.repository.get_instrument_id(
            profile.symbol,
            profile.exchange,
        )

        if instrument_id is None:
            raise RuntimeError(
                f"Instrument was not persisted: {symbol}"
            )

        stored = self.repository.get_price_history(
            instrument_id,
            start,
            end,
        )

        return self._rows_to_price_bars(
            symbol,
            stored,
        )

    def close(self):
        self.data_service.close()
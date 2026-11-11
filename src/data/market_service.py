from datetime import UTC, date, datetime, timedelta

from src.config.settings import settings
from src.data.errors import ProviderError
from src.data.ingestion import ingest_price_history
from src.data.models import CompanyProfile, PriceBar
from src.data.quality import build_price_quality_report
from src.data.service import DataService
from src.data.trading_calendar import (
    UnsupportedTradingCalendarError,
    get_expected_trading_dates,
)
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

    def get_price_quality_report(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> dict:
        """Assess stored price data without triggering ingestion."""
        profile = self.get_profile(symbol)
        instrument_id = self.repository.get_instrument_id(
            profile.symbol,
            profile.exchange,
        )
        rows = (
            self.repository.get_price_history(instrument_id, start, end)
            if instrument_id is not None
            else []
        )
        return build_price_quality_report(
            profile.symbol,
            profile.exchange,
            start,
            end,
            rows,
        )

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
                source_url=row.get("source_url"),
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
        cached_calendar_fallback = None

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

                try:
                    expected_dates = get_expected_trading_dates(
                        start,
                        end,
                        profile.exchange,
                    )
                except UnsupportedTradingCalendarError:
                    expected_dates = None
                    cached_calendar_fallback = self.repository.get_price_history(
                        instrument_id,
                        start,
                        end,
                    )

                if expected_dates:
                    latest_expected = expected_dates[-1]

                    # Only treat dates inside the stored coverage window as
                    # internal gaps. Dates before `earliest` may simply be
                    # unavailable because the provider returned limited history.
                    coverage_start = max(start, earliest)

                    missing_dates = (
                        self.repository.get_missing_expected_price_dates(
                            instrument_id,
                            coverage_start,
                            min(end, latest),
                            profile.exchange,
                        )
                        if coverage_start <= min(end, latest)
                        else []
                    )

                    # Complete coverage can be reused only while the latest
                    # expected trading day's data remains fresh.
                    if latest >= latest_expected and not missing_dates:
                        stored = self.repository.get_price_history(
                            instrument_id,
                            start,
                            end,
                        )

                        if stored:
                            retrieved_at = (
                                self.repository.get_latest_price_retrieved_at(
                                    instrument_id,
                                    latest_expected,
                                )
                            )

                            if retrieved_at is not None:
                                if retrieved_at.tzinfo is None:
                                    retrieved_at = retrieved_at.replace(tzinfo=UTC)

                                age = datetime.now(UTC) - retrieved_at
                                freshness_limit = timedelta(
                                    hours=settings.market_data_freshness_hours
                                )

                                if timedelta(0) <= age <= freshness_limit:
                                    return self._rows_to_price_bars(
                                        symbol,
                                        stored,
                                    )

                            # Stale or missing retrieval timestamp: refresh,
                            # but retain the stored data if this refresh fails.
                            try:
                                ingest_price_history(
                                    self.data_service,
                                    symbol,
                                    start,
                                    end,
                                )
                            except ProviderError:
                                return self._rows_to_price_bars(
                                    symbol,
                                    stored,
                                )
                            except RuntimeError as exc:
                                if isinstance(exc.__cause__, ProviderError):
                                    return self._rows_to_price_bars(
                                        symbol,
                                        stored,
                                    )
                                raise

                            refreshed = self.repository.get_price_history(
                                instrument_id,
                                start,
                                end,
                            )
                            return self._rows_to_price_bars(
                                symbol,
                                refreshed or stored,
                            )

        # Provider access remains available when no verified calendar exists.
        try:
            ingest_price_history(
                self.data_service,
                symbol,
                start,
                end,
            )
        except ProviderError:
            if cached_calendar_fallback:
                return self._rows_to_price_bars(symbol, cached_calendar_fallback)
            raise
        except RuntimeError as exc:
            if cached_calendar_fallback and isinstance(exc.__cause__, ProviderError):
                return self._rows_to_price_bars(symbol, cached_calendar_fallback)
            raise

        instrument_id = self.repository.get_instrument_id(
            profile.symbol,
            profile.exchange,
        )

        if instrument_id is None:
            raise RuntimeError(f"Instrument was not persisted: {symbol}")

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

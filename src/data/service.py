from datetime import date

from src.config.settings import settings
from src.data.base import FinancialDataProvider
from src.data.models import CompanyProfile, PriceBar
from src.data.providers.alpha_vantage import AlphaVantageProvider
from src.data.providers.twelve_data import TwelveDataProvider


class DataService:
    """Application-level interface for financial data."""

    def __init__(self, provider: FinancialDataProvider) -> None:
        self.provider = provider

    def search_company(self, query: str) -> list[CompanyProfile]:
        return self.provider.search_company(query)

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        return self.provider.get_company_profile(symbol)

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        return self.provider.get_price_history(
            symbol,
            start,
            end,
        )

    def close(self) -> None:
        close = getattr(self.provider, "close", None)

        if close is not None:
            close()


def create_data_service() -> DataService:
    """Create the configured financial data service."""

    provider_name = settings.financial_data_provider.lower().strip()

    providers: dict[str, type[FinancialDataProvider]] = {
        "alpha_vantage": AlphaVantageProvider,
        "twelve_data": TwelveDataProvider,
    }

    provider_class = providers.get(provider_name)

    if provider_class is None:
        raise ValueError(
            f"Unsupported financial data provider: {provider_name}"
        )

    return DataService(provider_class())
from src.config.settings import settings
from src.data.base import FinancialDataProvider
from src.data.models import CompanyProfile, PriceBar
from src.data.providers.alpha_vantage import AlphaVantageProvider
from src.data.providers.twelve_data import TwelveDataProvider


def create_financial_data_provider() -> FinancialDataProvider:
    """Create the configured financial data provider."""

    provider = settings.financial_data_provider.strip().lower()

    providers: dict[str, type[FinancialDataProvider]] = {
        "alpha_vantage": AlphaVantageProvider,
        "twelve_data": TwelveDataProvider,
    }

    provider_class = providers.get(provider)

    if provider_class is None:
        supported = ", ".join(sorted(providers))
        raise ValueError(
            f"Unsupported financial data provider: {provider!r}. "
            f"Supported providers: {supported}"
        )

    return provider_class()


class DataService:
    """Application service for financial data providers."""

    def __init__(self, provider: FinancialDataProvider):
        self.provider = provider

    def search_company(self, query: str) -> list[CompanyProfile]:
        return self.provider.search_company(query)

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        return self.provider.get_company_profile(symbol)

    def get_price_history(
        self,
        symbol: str,
        start,
        end,
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
    """Create the application financial data service."""

    return DataService(
        create_financial_data_provider()
    )
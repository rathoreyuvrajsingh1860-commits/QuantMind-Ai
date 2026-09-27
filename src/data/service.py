from datetime import date

from src.data.errors import is_fallback_eligible
from src.config.settings import settings
from src.data.base import (
    DataCapability,
    FinancialDataProvider,
)
from src.data.models import CompanyProfile, PriceBar
from src.data.providers.alpha_vantage import AlphaVantageProvider
from src.data.providers.twelve_data import TwelveDataProvider


PROVIDER_REGISTRY: dict[
    str,
    type[FinancialDataProvider],
] = {
    "alpha_vantage": AlphaVantageProvider,
    "twelve_data": TwelveDataProvider,
}


def _provider_names_from_settings() -> list[str]:
    """Return configured providers in priority order."""

    primary = settings.financial_data_provider.strip().lower()

    fallbacks = [
        value.strip().lower()
        for value in settings.financial_data_provider_fallbacks.split(",")
        if value.strip()
    ]

    names: list[str] = []

    for name in [primary, *fallbacks]:
        if name and name not in names:
            names.append(name)

    return names


def create_financial_data_providers() -> list[FinancialDataProvider]:
    """Create configured financial data providers in priority order."""

    provider_names = _provider_names_from_settings()

    if not provider_names:
        raise ValueError(
            "No financial data provider is configured"
        )

    providers: list[FinancialDataProvider] = []

    for name in provider_names:
        provider_class = PROVIDER_REGISTRY.get(name)

        if provider_class is None:
            supported = ", ".join(
                sorted(PROVIDER_REGISTRY)
            )
            raise ValueError(
                f"Unsupported financial data provider: {name!r}. "
                f"Supported providers: {supported}"
            )

        providers.append(provider_class())

    return providers


def create_financial_data_provider() -> FinancialDataProvider:
    """Create the primary configured financial data provider."""

    return create_financial_data_providers()[0]


class DataService:
    """Application service for financial data providers."""

    def __init__(
        self,
        provider: FinancialDataProvider,
        fallback_providers: list[FinancialDataProvider] | None = None,
    ):
        self.providers = [
            provider,
            *(fallback_providers or []),
        ]

    def _providers_for(
        self,
        capability: DataCapability,
    ) -> list[FinancialDataProvider]:
        """Return providers supporting a capability."""

        return [
            provider
            for provider in self.providers
            if capability in provider.capabilities
        ]

    def _execute_with_fallback(
        self,
        capability: DataCapability,
        operation,
    ):
        """Execute an operation using configured provider fallback."""

        providers = self._providers_for(capability)

        if not providers:
            raise RuntimeError(
                f"No configured provider supports "
                f"{capability.value}"
            )

        last_error: Exception | None = None

        for provider in providers:
            try:
                return operation(provider)
            except Exception as exc:
                if not is_fallback_eligible(exc):
                    raise

                last_error = exc
        raise RuntimeError(
            f"All providers failed for {capability.value}"
        ) from last_error

    def search_company(
        self,
        query: str,
    ) -> list[CompanyProfile]:
        return self._execute_with_fallback(
            DataCapability.COMPANY_SEARCH,
            lambda provider: provider.search_company(query),
        )

    def get_company_profile(
        self,
        symbol: str,
    ) -> CompanyProfile:
        return self._execute_with_fallback(
            DataCapability.COMPANY_PROFILE,
            lambda provider: provider.get_company_profile(symbol),
        )

    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        return self._execute_with_fallback(
            DataCapability.PRICE_HISTORY,
            lambda provider: provider.get_price_history(
                symbol,
                start,
                end,
            ),
        )

    def close(self) -> None:
        for provider in self.providers:
            close = getattr(provider, "close", None)

            if close is not None:
                close()


def create_data_service() -> DataService:
    """Create the configured financial data service."""

    providers = create_financial_data_providers()

    return DataService(
        providers[0],
        fallback_providers=providers[1:],
    )
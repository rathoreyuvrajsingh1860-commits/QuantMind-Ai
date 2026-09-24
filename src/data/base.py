from abc import ABC, abstractmethod
from datetime import date

from src.data.models import CompanyProfile, PriceBar


class FinancialDataProvider(ABC):
    """Provider interface for normalized financial data."""

    @abstractmethod
    def search_company(self, query: str) -> list[CompanyProfile]:
        """Search for companies/instruments."""
        raise NotImplementedError

    @abstractmethod
    def get_company_profile(self, symbol: str) -> CompanyProfile:
        """Return normalized company information."""
        raise NotImplementedError

    @abstractmethod
    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        """Return normalized historical price data."""
        raise NotImplementedError
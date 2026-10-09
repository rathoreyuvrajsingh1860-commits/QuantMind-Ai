from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import StrEnum

from src.data.models import CompanyProfile, NewsArticle, PriceBar


class DataCapability(StrEnum):
    """Operations supported by financial data providers."""

    COMPANY_SEARCH = "company_search"
    COMPANY_PROFILE = "company_profile"
    PRICE_HISTORY = "price_history"
    NEWS = "news"


class FinancialDataProvider(ABC):
    """Abstract interface for financial data providers."""

    @property
    @abstractmethod
    def capabilities(self) -> set[DataCapability]:
        """Return the capabilities supported by this provider."""
        raise NotImplementedError

    @abstractmethod
    def search_company(self, query: str) -> list[CompanyProfile]:
        raise NotImplementedError

    @abstractmethod
    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise NotImplementedError

    @abstractmethod
    def get_price_history(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> list[PriceBar]:
        raise NotImplementedError

    @abstractmethod
    def get_news(
        self,
        symbol: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[NewsArticle]:
        raise NotImplementedError

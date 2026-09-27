from unittest.mock import patch

import pytest

from src.data.base import DataCapability
from src.data.service import (
    DataService,
    create_financial_data_provider,
)
from src.data.errors import (
    ProviderAuthenticationError,
    ProviderServerError,
    RateLimitError,
    TemporaryProviderError,
)

def test_create_alpha_vantage_provider():
    mock_provider = lambda: "alpha-provider"

    with patch(
        "src.data.service.settings.financial_data_provider",
        "alpha_vantage",
    ), patch.dict(
        "src.data.service.PROVIDER_REGISTRY",
        {"alpha_vantage": mock_provider},
        clear=True,
    ):
        result = create_financial_data_provider()

    assert result == "alpha-provider"


def test_create_twelve_data_provider():
    mock_provider = lambda: "twelve-provider"

    with patch(
        "src.data.service.settings.financial_data_provider",
        "twelve_data",
    ), patch.dict(
        "src.data.service.PROVIDER_REGISTRY",
        {"twelve_data": mock_provider},
        clear=True,
    ):
        result = create_financial_data_provider()

    assert result == "twelve-provider"

def test_unknown_provider_raises_error():
    with patch(
        "src.data.service.settings.financial_data_provider",
        "unknown_provider",
    ):
        with pytest.raises(ValueError, match="Unsupported financial data provider"):
            create_financial_data_provider()


def test_data_service_delegates_to_provider():
    class FakeProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_SEARCH,
                DataCapability.COMPANY_PROFILE,
                DataCapability.PRICE_HISTORY,
            }

        def search_company(self, query):
            return [query]

        def get_company_profile(self, symbol):
            return symbol

        def get_price_history(self, symbol, start, end):
            return [symbol, start, end]

        def close(self):
            self.closed = True

    provider = FakeProvider()
    service = DataService(provider)

    assert service.search_company("RELIANCE") == ["RELIANCE"]
    assert service.get_company_profile("RELIANCE:BSE") == "RELIANCE:BSE"
    assert service.get_price_history(
        "RELIANCE:BSE",
        "start",
        "end",
    ) == [
        "RELIANCE:BSE",
        "start",
        "end",
    ]

    service.close()
    assert provider.closed is True

def test_data_service_falls_back_when_primary_provider_fails():
    class PrimaryProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            raise TemporaryProviderError("primary unavailable")

        def close(self):
            pass

    class FallbackProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            return "fallback-result"

        def close(self):
            pass

    service = DataService(
        PrimaryProvider(),
        fallback_providers=[FallbackProvider()],
    )

    assert service.get_company_profile("RELIANCE:BSE") == "fallback-result"


def test_data_service_does_not_use_provider_without_capability():
    class ProviderWithoutProfile:
        @property
        def capabilities(self):
            return {
                DataCapability.PRICE_HISTORY,
            }

        def get_company_profile(self, symbol):
            raise AssertionError(
                "Provider without capability should not be called"
            )

        def close(self):
            pass

    service = DataService(
        ProviderWithoutProfile(),
    )

    with pytest.raises(
        RuntimeError,
        match="No configured provider supports company_profile",
    ):
        service.get_company_profile("RELIANCE:BSE")

def test_data_service_falls_back_on_rate_limit():
    class PrimaryProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            raise RateLimitError()

        def close(self):
            pass

    class FallbackProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            return "fallback-result"

        def close(self):
            pass

    service = DataService(
        PrimaryProvider(),
        fallback_providers=[FallbackProvider()],
    )

    assert service.get_company_profile(
        "RELIANCE:BSE"
    ) == "fallback-result"


def test_data_service_falls_back_on_server_error():
    class PrimaryProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            raise ProviderServerError()

        def close(self):
            pass

    class FallbackProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            return "fallback-result"

        def close(self):
            pass

    service = DataService(
        PrimaryProvider(),
        fallback_providers=[FallbackProvider()],
    )

    assert service.get_company_profile(
        "RELIANCE:BSE"
    ) == "fallback-result"


def test_data_service_does_not_fallback_on_authentication_error():
    class PrimaryProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            raise ProviderAuthenticationError(
                "invalid API key"
            )

        def close(self):
            pass

    class FallbackProvider:
        @property
        def capabilities(self):
            return {
                DataCapability.COMPANY_PROFILE,
            }

        def get_company_profile(self, symbol):
            raise AssertionError(
                "Fallback provider must not be called"
            )

        def close(self):
            pass

    service = DataService(
        PrimaryProvider(),
        fallback_providers=[FallbackProvider()],
    )

    with pytest.raises(
        ProviderAuthenticationError,
        match="invalid API key",
    ):
        service.get_company_profile("RELIANCE:BSE")
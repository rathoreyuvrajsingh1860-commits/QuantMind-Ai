from unittest.mock import patch

import pytest

from src.data.service import (
    DataService,
    create_financial_data_provider,
)


def test_create_alpha_vantage_provider():
    with patch(
        "src.data.service.settings.financial_data_provider",
        "alpha_vantage",
    ), patch(
        "src.data.service.AlphaVantageProvider"
    ) as mock_provider:
        result = create_financial_data_provider()

    mock_provider.assert_called_once()
    assert result == mock_provider.return_value


def test_create_twelve_data_provider():
    with patch(
        "src.data.service.settings.financial_data_provider",
        "twelve_data",
    ), patch(
        "src.data.service.TwelveDataProvider"
    ) as mock_provider:
        result = create_financial_data_provider()

    mock_provider.assert_called_once()
    assert result == mock_provider.return_value


def test_unknown_provider_raises_error():
    with patch(
        "src.data.service.settings.financial_data_provider",
        "unknown_provider",
    ):
        with pytest.raises(ValueError, match="Unsupported financial data provider"):
            create_financial_data_provider()


def test_data_service_delegates_to_provider():
    class FakeProvider:
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
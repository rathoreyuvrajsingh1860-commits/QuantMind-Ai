from unittest.mock import MagicMock, patch

from src.data.providers.alpha_vantage import AlphaVantageProvider


def test_alpha_vantage_request_uses_retry_wrapper():
    provider = object.__new__(
        AlphaVantageProvider
    )

    expected = {
        "test": "value",
    }

    with patch(
        "src.data.providers.alpha_vantage.retry_with_backoff",
        return_value=expected,
    ) as mock_retry:
        result = provider._request(
            {
                "function": "TEST",
            }
        )

    assert result == expected
    mock_retry.assert_called_once()


def test_alpha_vantage_request_once_uses_http_client():
    provider = object.__new__(
        AlphaVantageProvider
    )

    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "test": "value",
    }

    provider.client.get.return_value = response

    with patch(
        "src.data.providers.alpha_vantage.settings.financial_data_api_key",
        "test-key",
    ):
        result = provider._request_once(
            {
                "function": "TEST",
            }
        )

    assert result == {
        "test": "value",
    }

    provider.client.get.assert_called_once()
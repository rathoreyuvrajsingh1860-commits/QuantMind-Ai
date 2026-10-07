from unittest.mock import MagicMock, patch

from src.data.providers.twelve_data import TwelveDataProvider


def test_twelve_data_request_uses_retry_wrapper():
    provider = object.__new__(TwelveDataProvider)

    expected = {
        "test": "value",
    }

    attempt_callback = MagicMock()

    with patch(
        "src.data.providers.twelve_data.retry_with_backoff",
        return_value=expected,
    ) as mock_retry:
        result = provider._request(
            "/test",
            params={"symbol": "TEST"},
            on_attempt=attempt_callback,
        )

    assert result == expected
    mock_retry.assert_called_once()

    args, kwargs = mock_retry.call_args

    assert callable(args[0])
    assert kwargs["on_attempt"] is attempt_callback


def test_twelve_data_request_once_uses_http_client():
    provider = object.__new__(TwelveDataProvider)

    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "status": "ok",
        "data": [],
    }

    provider.client.get.return_value = response

    result = provider._request_once(
        "/time_series",
        params={"symbol": "TEST"},
    )

    assert result == {
        "status": "ok",
        "data": [],
    }

    provider.client.get.assert_called_once()


def test_twelve_data_rate_limit_raises_rate_limit_error():
    provider = object.__new__(TwelveDataProvider)
    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 429
    provider.client.get.return_value = response

    from src.data.errors import RateLimitError

    with patch("src.data.providers.twelve_data.retry_with_backoff") as mock_retry:
        mock_retry.side_effect = lambda operation, **kwargs: operation()

        try:
            provider._request(
                "/time_series",
                params={"symbol": "TEST"},
            )
            raise AssertionError("Expected RateLimitError")
        except RateLimitError:
            pass


def test_twelve_data_server_error_raises_provider_server_error():
    provider = object.__new__(TwelveDataProvider)
    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 500
    provider.client.get.return_value = response

    from src.data.errors import ProviderServerError

    with patch("src.data.providers.twelve_data.retry_with_backoff") as mock_retry:
        mock_retry.side_effect = lambda operation, **kwargs: operation()

        try:
            provider._request(
                "/time_series",
                params={"symbol": "TEST"},
            )
            raise AssertionError("Expected ProviderServerError")
        except ProviderServerError:
            pass


def test_twelve_data_authentication_error_raises_provider_authentication_error():
    provider = object.__new__(TwelveDataProvider)
    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 401
    provider.client.get.return_value = response

    from src.data.errors import ProviderAuthenticationError

    with patch("src.data.providers.twelve_data.retry_with_backoff") as mock_retry:
        mock_retry.side_effect = lambda operation, **kwargs: operation()

        try:
            provider._request(
                "/time_series",
                params={"symbol": "TEST"},
            )
            raise AssertionError("Expected ProviderAuthenticationError")
        except ProviderAuthenticationError:
            pass

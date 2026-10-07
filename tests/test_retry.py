from unittest.mock import patch

import pytest

from src.data.errors import (
    ProviderAuthenticationError,
    ProviderServerError,
    RateLimitError,
    TemporaryProviderError,
)
from src.data.retry import retry_with_backoff


def test_retry_succeeds_after_transient_failures():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1

        if attempts < 3:
            raise TemporaryProviderError("temporary failure")

        return "success"

    with patch("src.data.retry.time.sleep") as mock_sleep:
        result = retry_with_backoff(
            operation,
            max_attempts=3,
            delays=(1.0, 2.0),
        )

    assert result == "success"
    assert attempts == 3

    mock_sleep.assert_any_call(1.0)
    mock_sleep.assert_any_call(2.0)


def test_retry_raises_after_max_attempts():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise ProviderServerError("server unavailable")

    with (
        patch("src.data.retry.time.sleep") as mock_sleep,
        pytest.raises(
            ProviderServerError,
            match="server unavailable",
        ),
    ):
        retry_with_backoff(
            operation,
            max_attempts=3,
            delays=(1.0, 2.0),
        )

    assert attempts == 3
    assert mock_sleep.call_count == 2


def test_rate_limit_is_not_retried():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise RateLimitError("rate limited")

    with (
        patch("src.data.retry.time.sleep") as mock_sleep,
        pytest.raises(
            RateLimitError,
            match="rate limited",
        ),
    ):
        retry_with_backoff(operation)

    assert attempts == 1
    mock_sleep.assert_not_called()


def test_authentication_error_is_not_retried():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise ProviderAuthenticationError("invalid API key")

    with (
        patch("src.data.retry.time.sleep") as mock_sleep,
        pytest.raises(
            ProviderAuthenticationError,
            match="invalid API key",
        ),
    ):
        retry_with_backoff(operation)

    assert attempts == 1
    mock_sleep.assert_not_called()


def test_retry_validates_attempt_count():
    with pytest.raises(
        ValueError,
        match="max_attempts must be at least 1",
    ):
        retry_with_backoff(
            lambda: "success",
            max_attempts=0,
        )


def test_retry_reports_attempt_numbers():
    attempts = []

    def operation():
        if len(attempts) < 2:
            raise TemporaryProviderError("temporary failure")

        return "success"

    with patch("src.data.retry.time.sleep"):
        result = retry_with_backoff(
            operation,
            max_attempts=3,
            delays=(1.0, 2.0),
            on_attempt=attempts.append,
        )

    assert result == "success"
    assert attempts == [1, 2]


def test_retry_without_callback_still_works():
    result = retry_with_backoff(
        lambda: "success",
    )

    assert result == "success"

import time
from collections.abc import Callable
from typing import TypeVar

from src.data.errors import (
    ProviderServerError,
    TemporaryProviderError,
)


T = TypeVar("T")


RETRYABLE_ERRORS = (
    TemporaryProviderError,
    ProviderServerError,
)


def retry_with_backoff(
    operation: Callable[[], T],
    *,
    max_attempts: int = 3,
    delays: tuple[float, ...] = (1.0, 2.0),
) -> T:
    """Retry transient provider failures with exponential backoff."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    last_error: Exception | None = None

    for attempt in range(max_attempts):
        try:
            return operation()

        except RETRYABLE_ERRORS as exc:
            last_error = exc

            if attempt >= max_attempts - 1:
                raise

            delay_index = min(
                attempt,
                len(delays) - 1,
            )

            time.sleep(delays[delay_index])

    raise RuntimeError(
        "Retry operation failed unexpectedly"
    ) from last_error
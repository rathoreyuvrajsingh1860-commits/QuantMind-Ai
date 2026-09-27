from enum import StrEnum


class ProviderErrorCode(StrEnum):
    RATE_LIMITED = "rate_limited"
    TEMPORARY_FAILURE = "temporary_failure"
    SERVER_ERROR = "server_error"
    UNSUPPORTED = "unsupported"
    AUTHENTICATION = "authentication"
    INVALID_REQUEST = "invalid_request"
    CONFIGURATION = "configuration"


class ProviderError(Exception):
    """Base error raised by a financial data provider."""

    def __init__(
        self,
        message: str,
        code: ProviderErrorCode,
    ):
        super().__init__(message)
        self.code = code


class RateLimitError(ProviderError):
    def __init__(self, message: str = "Provider rate limit exceeded"):
        super().__init__(message, ProviderErrorCode.RATE_LIMITED)


class TemporaryProviderError(ProviderError):
    def __init__(self, message: str = "Temporary provider failure"):
        super().__init__(
            message,
            ProviderErrorCode.TEMPORARY_FAILURE,
        )


class ProviderServerError(ProviderError):
    def __init__(self, message: str = "Provider server error"):
        super().__init__(
            message,
            ProviderErrorCode.SERVER_ERROR,
        )


class UnsupportedDataError(ProviderError):
    def __init__(self, message: str = "Data is unsupported"):
        super().__init__(
            message,
            ProviderErrorCode.UNSUPPORTED,
        )


class ProviderAuthenticationError(ProviderError):
    def __init__(self, message: str = "Provider authentication failed"):
        super().__init__(
            message,
            ProviderErrorCode.AUTHENTICATION,
        )


class ProviderInvalidRequestError(ProviderError):
    def __init__(self, message: str = "Invalid provider request"):
        super().__init__(
            message,
            ProviderErrorCode.INVALID_REQUEST,
        )


class ProviderConfigurationError(ProviderError):
    def __init__(self, message: str = "Provider configuration error"):
        super().__init__(
            message,
            ProviderErrorCode.CONFIGURATION,
        )


def is_fallback_eligible(error: Exception) -> bool:
    """Return whether another provider should be attempted."""

    return isinstance(
        error,
        (
            RateLimitError,
            TemporaryProviderError,
            ProviderServerError,
            UnsupportedDataError,
        ),
    )
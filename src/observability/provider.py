from dataclasses import dataclass


@dataclass
class ProviderRequestMetrics:
    """Observability metrics for a single provider operation."""

    provider: str
    operation: str
    attempts: int = 0
    retries: int = 0
    fallback_used: bool = False
    duration_ms: float = 0.0
    success: bool = False
    error_code: str | None = None

    def record_attempt(self, attempt_number: int) -> None:
        """Record a provider request attempt."""

        self.attempts = max(
            self.attempts,
            attempt_number,
        )
        self.retries = max(
            0,
            self.attempts - 1,
        )

    def record_success(self) -> None:
        """Record a successful provider operation."""

        self.success = True
        self.error_code = None

    def record_failure(self, error_code: str | None) -> None:
        """Record a failed provider operation."""

        self.success = False
        self.error_code = error_code
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

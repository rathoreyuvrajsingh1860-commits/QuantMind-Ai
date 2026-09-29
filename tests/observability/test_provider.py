from src.observability.provider import ProviderRequestMetrics


def test_provider_request_metrics_defaults():
    metrics = ProviderRequestMetrics(
        provider="alpha_vantage",
        operation="price_history",
    )

    assert metrics.provider == "alpha_vantage"
    assert metrics.operation == "price_history"
    assert metrics.attempts == 0
    assert metrics.retries == 0
    assert metrics.fallback_used is False
    assert metrics.duration_ms == 0.0
    assert metrics.success is False
    assert metrics.error_code is None


def test_provider_request_metrics_records_failure():
    metrics = ProviderRequestMetrics(
        provider="alpha_vantage",
        operation="price_history",
        attempts=3,
        retries=2,
        fallback_used=True,
        duration_ms=1250.5,
        success=False,
        error_code="rate_limited",
    )

    assert metrics.attempts == 3
    assert metrics.retries == 2
    assert metrics.fallback_used is True
    assert metrics.duration_ms == 1250.5
    assert metrics.success is False
    assert metrics.error_code == "rate_limited"


def test_provider_request_metrics_records_success():
    metrics = ProviderRequestMetrics(
        provider="twelve_data",
        operation="company_profile",
        attempts=1,
        retries=0,
        duration_ms=84.2,
        success=True,
    )

    assert metrics.provider == "twelve_data"
    assert metrics.operation == "company_profile"
    assert metrics.attempts == 1
    assert metrics.retries == 0
    assert metrics.fallback_used is False
    assert metrics.duration_ms == 84.2
    assert metrics.success is True
    assert metrics.error_code is None

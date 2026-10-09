from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from src.data.providers.alpha_vantage import AlphaVantageProvider


def test_alpha_vantage_request_uses_retry_wrapper():
    provider = object.__new__(AlphaVantageProvider)

    expected = {
        "test": "value",
    }

    attempt_callback = MagicMock()

    with patch(
        "src.data.providers.alpha_vantage.retry_with_backoff",
        return_value=expected,
    ) as mock_retry:
        result = provider._request(
            {
                "function": "TEST",
            },
            on_attempt=attempt_callback,
        )

    assert result == expected
    mock_retry.assert_called_once()

    args, kwargs = mock_retry.call_args

    assert callable(args[0])
    assert kwargs["on_attempt"] is attempt_callback


def test_alpha_vantage_request_once_uses_http_client():
    provider = object.__new__(AlphaVantageProvider)
    provider.api_key = "test-key"

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


def test_alpha_vantage_get_news_builds_request_and_normalizes_articles():
    provider = object.__new__(AlphaVantageProvider)

    published_at = "20261008T153000"

    with patch.object(
        provider,
        "_request",
        return_value={
            "feed": [
                {
                    "title": "Reliance announces new investment",
                    "source": "Example News",
                    "authors": ["Jane Doe"],
                    "time_published": published_at,
                    "url": "https://example.com/article",
                    "summary": "Reliance announced a new investment.",
                }
            ]
        },
    ) as mock_request:
        result = provider.get_news(
            "RELIANCE:NSE",
            datetime(2026, 10, 1, tzinfo=UTC),
            datetime(2026, 10, 8, 23, 59, tzinfo=UTC),
        )

    mock_request.assert_called_once_with(
        {
            "function": "NEWS_SENTIMENT",
            "tickers": "RELIANCE.NSE",
            "sort": "LATEST",
            "limit": "1000",
            "time_from": "20261001T0000",
            "time_to": "20261008T2359",
        }
    )

    assert len(result) == 1

    article = result[0]

    assert article.title == "Reliance announces new investment"
    assert article.publisher == "Example News"
    assert article.author == "Jane Doe"
    assert article.published_at == datetime(
        2026,
        10,
        8,
        15,
        30,
        tzinfo=UTC,
    )
    assert article.url == "https://example.com/article"
    assert article.summary == "Reliance announced a new investment."
    assert article.symbol == "RELIANCE.NSE"
    assert article.source == "alpha_vantage"
    assert article.retrieved_at.tzinfo == UTC


def test_alpha_vantage_get_news_handles_articles_without_author():
    provider = object.__new__(AlphaVantageProvider)

    with patch.object(
        provider,
        "_request",
        return_value={
            "feed": [
                {
                    "title": "Market update",
                    "source": "Example News",
                    "authors": [],
                    "time_published": "20261008T100000",
                }
            ]
        },
    ):
        result = provider.get_news("RELIANCE:NSE")

    assert len(result) == 1
    assert result[0].author is None


def test_alpha_vantage_get_news_returns_empty_list_for_empty_feed():
    provider = object.__new__(AlphaVantageProvider)

    with patch.object(
        provider,
        "_request",
        return_value={"feed": []},
    ):
        result = provider.get_news("RELIANCE:NSE")

    assert result == []


def test_alpha_vantage_prefers_provider_specific_api_key():
    with (
        patch(
            "src.data.providers.alpha_vantage.settings.alpha_vantage_api_key",
            "alpha-key",
        ),
        patch(
            "src.data.providers.alpha_vantage.settings.financial_data_api_key",
            "generic-key",
        ),
        patch("src.data.providers.alpha_vantage.httpx.Client") as mock_client,
    ):
        provider = AlphaVantageProvider()

    assert provider.api_key == "alpha-key"
    mock_client.assert_called_once()
    provider.close()


def test_alpha_vantage_falls_back_to_generic_api_key():
    with (
        patch("src.data.providers.alpha_vantage.settings.alpha_vantage_api_key", ""),
        patch(
            "src.data.providers.alpha_vantage.settings.financial_data_api_key",
            "generic-key",
        ),
        patch("src.data.providers.alpha_vantage.httpx.Client"),
    ):
        provider = AlphaVantageProvider()

    assert provider.api_key == "generic-key"
    provider.close()


def test_alpha_vantage_rejects_empty_response():
    provider = object.__new__(AlphaVantageProvider)
    provider.api_key = "test-key"
    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {}
    provider.client.get.return_value = response

    from src.data.errors import ProviderServerError

    try:
        provider._request_once({"function": "TEST"})
    except ProviderServerError as exc:
        assert "empty or invalid response" in str(exc)
    else:
        raise AssertionError("Expected ProviderServerError")


def test_alpha_vantage_rejects_invalid_json():
    provider = object.__new__(AlphaVantageProvider)
    provider.api_key = "test-key"
    provider.client = MagicMock()

    response = MagicMock()
    response.status_code = 200
    response.json.side_effect = ValueError("invalid JSON")
    provider.client.get.return_value = response

    from src.data.errors import ProviderServerError

    try:
        provider._request_once({"function": "TEST"})
    except ProviderServerError as exc:
        assert "invalid JSON" in str(exc)
    else:
        raise AssertionError("Expected ProviderServerError")


def test_alpha_vantage_normalizes_exchange_qualified_symbols():
    provider = object.__new__(AlphaVantageProvider)

    assert provider._normalize_symbol("RELIANCE:NSE") == "RELIANCE.NSE"
    assert provider._normalize_symbol("RELIANCE:BSE") == "RELIANCE.BSE"
    assert provider._normalize_symbol("AAPL:NASDAQ") == "AAPL"
    assert provider._normalize_symbol("IBM:NYSE") == "IBM"


def test_alpha_vantage_rejects_unsupported_exchange():
    import pytest

    provider = object.__new__(AlphaVantageProvider)

    with pytest.raises(ValueError, match="Unsupported Alpha Vantage exchange"):
        provider._normalize_symbol("RELIANCE:UNKNOWN")


def test_alpha_vantage_price_history_rejects_missing_time_series():
    from datetime import date

    import pytest

    from src.data.errors import ProviderServerError

    provider = object.__new__(AlphaVantageProvider)

    with (
        patch.object(provider, "_request", return_value={"Meta Data": {}}),
        pytest.raises(ProviderServerError, match="No daily price data"),
    ):
        provider.get_price_history(
            "RELIANCE:NSE",
            date(2026, 5, 1),
            date(2026, 10, 1),
        )


def test_alpha_vantage_get_news_handles_malformed_timestamp():
    provider = object.__new__(AlphaVantageProvider)

    with patch.object(
        provider,
        "_request",
        return_value={
            "feed": [
                {
                    "title": "Market update",
                    "source": "Example News",
                    "time_published": "not-a-valid-timestamp",
                }
            ]
        },
    ):
        result = provider.get_news("RELIANCE:NSE")

    assert len(result) == 1
    assert result[0].title == "Market update"
    assert result[0].published_at is None

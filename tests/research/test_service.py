from datetime import UTC, date, datetime
from decimal import Decimal

from src.data.models import CompanyProfile, PriceBar
from src.research.service import ResearchService


class FakeDataService:
    def __init__(self, *, news_error=None):
        self.news_error = news_error

    def search_company(self, query):
        return [
            CompanyProfile(
                symbol="RELIANCE",
                name="Reliance Industries Ltd.",
                exchange="NSE",
                country="India",
                currency="INR",
            ),
            CompanyProfile(
                symbol="RELIANCE",
                name="Reliance Industries Ltd.",
                exchange="BSE",
                country="India",
                currency="INR",
            ),
        ]

    def get_news(self, symbol, start=None, end=None):
        if self.news_error is not None:
            raise self.news_error

        from src.data.models import NewsArticle

        return [
            NewsArticle(
                title="Reliance announces new investment",
                publisher="Test News",
                author="Test Author",
                published_at=datetime(2026, 5, 15, 10, 30, tzinfo=UTC),
                url="https://example.com/reliance",
                summary="Reliance announced a new investment.",
                symbol=symbol,
                source="test-provider",
                retrieved_at=datetime(2026, 5, 15, 11, 0, tzinfo=UTC),
            )
        ]


class FakeMarketService:
    def __init__(self, *, news_error=None):
        self.data_service = FakeDataService(news_error=news_error)
        self.profile_symbols = []
        self.price_history_symbols = []

    def get_profile(self, symbol):
        self.profile_symbols.append(symbol)
        return CompanyProfile(
            symbol="RELIANCE.BSE",
            name="Reliance Industries",
            exchange="BSE",
            country="India",
            sector="Energy",
            industry="Oil & Gas",
            currency="INR",
        )

    def get_price_history(self, symbol, start, end):
        self.price_history_symbols.append(symbol)

        retrieved_at = datetime(
            2026,
            9,
            30,
            tzinfo=UTC,
        )

        return [
            PriceBar(
                symbol=symbol,
                date=date(2026, 1, 1),
                open=Decimal(100),
                high=Decimal(110),
                low=Decimal(95),
                close=Decimal(100),
                volume=1000,
                adjusted_close=None,
                source="test-provider",
                retrieved_at=retrieved_at,
            ),
            PriceBar(
                symbol=symbol,
                date=date(2026, 6, 1),
                open=Decimal(120),
                high=Decimal(130),
                low=Decimal(115),
                close=Decimal(125),
                volume=2000,
                adjusted_close=None,
                source="test-provider",
                retrieved_at=retrieved_at,
            ),
        ]

    def close(self):
        pass


def test_research_service_builds_market_research():
    service = ResearchService(FakeMarketService())

    result = service.research(
        "RELIANCE:BSE",
        start=date(2026, 1, 1),
        end=date(2026, 6, 1),
    )

    assert result.entity.name == "Reliance Industries"
    assert result.entity.symbol == "RELIANCE.BSE"

    assert result.market.observations == 2
    assert result.market.first_close == Decimal(100)
    assert result.market.latest_close == Decimal(125)
    assert result.market.absolute_change == Decimal(25)
    assert result.market.percentage_change == Decimal("25.00")
    assert result.market.period_high == Decimal(130)
    assert result.market.period_low == Decimal(95)
    assert result.market.average_close == Decimal("112.50")
    assert result.market.total_volume == 3000

    assert len(result.evidence) == 2
    assert result.evidence[0].source == "test-provider"


def test_research_service_rejects_ambiguous_unqualified_symbol_with_whitespace():
    service = ResearchService(FakeMarketService())

    try:
        service.research(
            "  reliance  ",
            start=date(2026, 1, 1),
            end=date(2026, 6, 1),
        )
    except ValueError as exc:
        assert str(exc) == (
            "Ambiguous company query: RELIANCE. Specify an exchange (BSE, NSE)."
        )
    else:
        raise AssertionError("Expected ValueError")


def test_research_service_normalizes_explicit_exchange():
    service = ResearchService(FakeMarketService())

    result = service.research(
        "  reliance:bse  ",
        start=date(2026, 1, 1),
        end=date(2026, 6, 1),
    )

    assert result.entity.symbol == "RELIANCE.BSE"


def test_research_service_rejects_ambiguous_unqualified_symbol():
    service = ResearchService(FakeMarketService())

    try:
        service.research(
            "RELIANCE",
            start=date(2026, 1, 1),
            end=date(2026, 6, 1),
        )
    except ValueError as exc:
        assert str(exc) == (
            "Ambiguous company query: RELIANCE. Specify an exchange (BSE, NSE)."
        )
    else:
        raise AssertionError("Expected ValueError")


def test_research_service_rejects_empty_query():
    service = ResearchService(FakeMarketService())

    try:
        service.research("")
    except ValueError as exc:
        assert str(exc) == "Research query cannot be empty"
    else:
        raise AssertionError("Expected ValueError")


def test_research_service_reports_actual_evidence_coverage():
    service = ResearchService(FakeMarketService())

    result = service.research(
        "RELIANCE:BSE",
        start=date(2026, 1, 1),
        end=date(2026, 9, 1),
    )

    assert result.coverage.requested_start == date(2026, 1, 1)
    assert result.coverage.requested_end == date(2026, 9, 1)
    assert result.coverage.evidence_start == date(2026, 1, 1)
    assert result.coverage.evidence_end == date(2026, 6, 1)
    assert result.coverage.observations == result.market.observations


def test_research_service_includes_news():
    service = ResearchService(FakeMarketService())

    result = service.research(
        "RELIANCE:BSE",
        start=date(2026, 1, 1),
        end=date(2026, 6, 1),
    )

    assert len(result.news) == 1

    article = result.news[0]

    assert article.title == "Reliance announces new investment"
    assert article.publisher == "Test News"
    assert article.author == "Test Author"
    assert article.source_url == "https://example.com/reliance"
    assert article.source == "test-provider"
    assert article.published_at == datetime(
        2026,
        5,
        15,
        10,
        30,
        tzinfo=UTC,
    )


def test_research_service_continues_when_news_fails():
    service = ResearchService(
        FakeMarketService(
            news_error=RuntimeError("news unavailable"),
        )
    )

    result = service.research(
        "RELIANCE:BSE",
        start=date(2026, 1, 1),
        end=date(2026, 6, 1),
    )

    assert result.market.observations == 2
    assert result.news == []
    assert (
        "News data was unavailable for the requested research period."
        in result.limitations
    )

from datetime import date as Date
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ResearchEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    name: str
    exchange: str | None = None
    country: str | None = None
    sector: str | None = None
    industry: str | None = None
    currency: str | None = None


class PriceHistoryPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: Date
    close: Decimal
    source: str


class MarketResearch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: Date
    end: Date
    observations: int
    latest_close: Decimal | None = None
    first_close: Decimal | None = None
    absolute_change: Decimal | None = None
    percentage_change: Decimal | None = None
    period_high: Decimal | None = None
    period_low: Decimal | None = None
    average_close: Decimal | None = None
    total_volume: int | None = None


class ResearchEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: Date | None = None
    source: str
    source_url: str | None = None
    retrieved_at: datetime | None = None
    description: str


class ResearchNews(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    publisher: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    source_url: str | None = None
    summary: str | None = None
    source: str
    retrieved_at: datetime


class ResearchCoverage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requested_start: Date
    requested_end: Date
    evidence_start: Date | None = None
    evidence_end: Date | None = None
    observations: int


class ResearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    entity: ResearchEntity
    market: MarketResearch
    evidence: list[ResearchEvidence]
    coverage: ResearchCoverage
    limitations: list[str]
    news: list[ResearchNews] = Field(default_factory=list)
    price_history: list[PriceHistoryPoint] = Field(default_factory=list)


class PersistedResearch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research_run_id: str

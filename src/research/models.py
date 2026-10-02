from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ResearchEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    name: str
    exchange: str | None = None
    country: str | None = None
    sector: str | None = None
    industry: str | None = None
    currency: str | None = None


class MarketResearch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: date
    end: date
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

    source: str
    retrieved_at: datetime | None = None
    description: str

class ResearchCoverage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requested_start: date
    requested_end: date
    evidence_start: date | None = None
    evidence_end: date | None = None
    observations: int

class ResearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    entity: ResearchEntity
    market: MarketResearch
    evidence: list[ResearchEvidence]
    coverage: ResearchCoverage
    limitations: list[str]


class PersistedResearch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research_run_id: str

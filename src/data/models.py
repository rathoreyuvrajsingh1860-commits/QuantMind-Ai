from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CompanyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    name: str
    exchange: str | None = None
    country: str | None = None
    sector: str | None = None
    industry: str | None = None
    currency: str | None = None


class PriceBar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int | None = None
    adjusted_close: Decimal | None = None
    source: str
    source_url: str | None = None
    retrieved_at: datetime


class NewsArticle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    publisher: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    url: str | None = None
    summary: str | None = None
    symbol: str | None = None
    source: str
    retrieved_at: datetime

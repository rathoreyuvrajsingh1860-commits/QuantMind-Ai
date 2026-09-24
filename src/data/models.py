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
    retrieved_at: datetime
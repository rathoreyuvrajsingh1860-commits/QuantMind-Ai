from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MarketProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    name: str
    exchange: str | None = None
    country: str | None = None
    sector: str | None = None
    industry: str | None = None
    currency: str | None = None


class PriceBarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int | None = None
    adjusted_close: Decimal | None = None
    source: str
    retrieved_at: datetime


class PriceHistoryResponse(BaseModel):
    symbol: str
    start: date
    end: date
    count: int
    data: list[PriceBarResponse]
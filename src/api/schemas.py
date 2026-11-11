from __future__ import annotations

from datetime import date as DateType
from datetime import datetime
from decimal import Decimal
from typing import Literal

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

    date: DateType
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
    start: DateType
    end: DateType
    count: int
    data: list[PriceBarResponse]


class PriceQualityFindingResponse(BaseModel):
    severity: Literal["error", "warning", "info"]
    code: str
    message: str
    date: DateType | None = None
    source: str | None = None


class PriceQualityResponse(BaseModel):
    symbol: str
    exchange: str | None = None
    start: DateType
    end: DateType
    status: Literal["healthy", "warning", "error", "no_data"]
    observation_count: int
    distinct_dates: int
    expected_sessions: int | None = None
    missing_sessions: int | None = None
    calendar_available: bool
    latest_retrieved_at: datetime | None = None
    latest_data_age_hours: float | None = None
    findings: list[PriceQualityFindingResponse]

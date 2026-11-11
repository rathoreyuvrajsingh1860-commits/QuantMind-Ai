from datetime import date, timedelta

import exchange_calendars as xcals
import pandas as pd
from exchange_calendars.errors import DateOutOfBounds, InvalidCalendarName

EXCHANGE_CALENDARS = {
    "BSE": "XBOM",
    "NYSE": "XNYS",
}

CALENDAR_EXCHANGE_ALIASES = {
    "INDIA/BOMBAY": "BSE",
    "BOMBAY STOCK EXCHANGE": "BSE",
    "BSE INDIA": "BSE",
    "XBOM": "BSE",
    "NEW YORK STOCK EXCHANGE": "NYSE",
    "XNYS": "NYSE",
}


class UnsupportedTradingCalendarError(ValueError):
    """Raised when a verified exchange calendar is unavailable."""


def is_weekday(value: date) -> bool:
    """Return True when the date falls on Monday through Friday."""
    return value.weekday() < 5


def get_expected_trading_dates(
    start: date,
    end: date,
    exchange: str | None = None,
    *,
    allow_weekday_approximation: bool = False,
) -> list[date]:
    """Return dates from a verified calendar, or an opted-in approximation."""
    if start > end:
        return []

    normalized_exchange = exchange.strip().upper() if exchange else None
    calendar_exchange = CALENDAR_EXCHANGE_ALIASES.get(
        normalized_exchange,
        normalized_exchange,
    )

    calendar_code = EXCHANGE_CALENDARS.get(calendar_exchange)

    if calendar_code is None:
        if not allow_weekday_approximation:
            label = normalized_exchange or "missing exchange"
            raise UnsupportedTradingCalendarError(
                f"No verified trading calendar configured for {label}."
            )

        dates: list[date] = []
        current = start
        while current <= end:
            if is_weekday(current):
                dates.append(current)
            current += timedelta(days=1)
        return dates

    try:
        calendar = xcals.get_calendar(calendar_code)
    except InvalidCalendarName as exc:
        raise RuntimeError(
            f"Configured exchange calendar {calendar_code} is unavailable."
        ) from exc

    first_session = calendar.first_session.date()
    last_session = calendar.last_session.date()

    if start < first_session or end > last_session:
        raise UnsupportedTradingCalendarError(
            f"Date range {start} to {end} is outside the supported "
            f"{normalized_exchange} calendar range "
            f"({first_session} to {last_session})."
        )

    try:
        sessions = calendar.sessions_in_range(
            pd.Timestamp(start),
            pd.Timestamp(end),
        )
    except DateOutOfBounds as exc:
        raise UnsupportedTradingCalendarError(
            f"Date range is outside the supported {normalized_exchange} calendar range."
        ) from exc

    return [session.date() for session in sessions]

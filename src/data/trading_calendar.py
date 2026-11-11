from datetime import date, timedelta

import exchange_calendars as xcals
import pandas as pd
from exchange_calendars.errors import DateOutOfBounds, InvalidCalendarName

EXCHANGE_CALENDARS = {
    "BSE": "XBOM",
    "NYSE": "XNYS",
}

NSE_EQUITY_HOLIDAYS = {
    2025: frozenset(
        date(2025, month, day)
        for month, day in (
            (2, 26),
            (3, 14),
            (3, 31),
            (4, 10),
            (4, 14),
            (4, 18),
            (5, 1),
            (8, 15),
            (8, 27),
            (10, 2),
            (10, 22),
            (11, 5),
            (12, 25),
        )
    ),
    2026: frozenset(
        date(2026, month, day)
        for month, day in (
            (1, 15),
            (1, 26),
            (3, 3),
            (3, 26),
            (3, 31),
            (4, 3),
            (4, 14),
            (5, 1),
            (5, 28),
            (6, 26),
            (9, 14),
            (10, 2),
            (10, 20),
            (11, 10),
            (11, 24),
            (12, 25),
        )
    ),
}

NSE_EQUITY_SPECIAL_SESSIONS = frozenset(
    {
        date(2025, 10, 21),
        date(2026, 11, 8),
    }
)

CALENDAR_EXCHANGE_ALIASES = {
    "INDIA/BOMBAY": "BSE",
    "BOMBAY STOCK EXCHANGE": "BSE",
    "BSE INDIA": "BSE",
    "XBOM": "BSE",
    "NSE INDIA": "NSE",
    "NATIONAL STOCK EXCHANGE OF INDIA": "NSE",
    "XNSE": "NSE",
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

    if calendar_exchange == "NSE":
        if start.year < 2025 or end.year > 2026:
            raise UnsupportedTradingCalendarError(
                "NSE equities calendar is verified only for 2025-2026."
            )

        holidays = set().union(
            *(NSE_EQUITY_HOLIDAYS[year] for year in range(start.year, end.year + 1))
        )

        dates: list[date] = []
        current = start
        while current <= end:
            if current in NSE_EQUITY_SPECIAL_SESSIONS or (
                is_weekday(current) and current not in holidays
            ):
                dates.append(current)
            current += timedelta(days=1)
        return dates

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

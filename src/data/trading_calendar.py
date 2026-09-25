from datetime import date, timedelta


def is_weekday(value: date) -> bool:
    """Return True when the date falls on Monday through Friday."""
    return value.weekday() < 5


def get_expected_trading_dates(
    start: date,
    end: date,
) -> list[date]:
    """Return weekday dates between start and end, inclusive."""

    dates: list[date] = []
    current = start

    while current <= end:
        if is_weekday(current):
            dates.append(current)

        current += timedelta(days=1)

    return dates
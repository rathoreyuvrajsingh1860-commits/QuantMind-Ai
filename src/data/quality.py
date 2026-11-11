from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from itertools import pairwise

from src.config.settings import settings
from src.data.trading_calendar import (
    UnsupportedTradingCalendarError,
    get_expected_trading_dates,
)


def build_price_quality_report(
    symbol: str,
    exchange: str | None,
    start: date,
    end: date,
    rows: list[dict],
) -> dict:
    """Build a read-only quality assessment for stored price observations."""
    findings = []
    ordered = sorted(rows, key=lambda row: (row["date"], row["source"]))
    dates = {row["date"] for row in ordered}

    seen = set()
    for row in ordered:
        key = (row["date"], row["source"])
        if key in seen:
            findings.append(
                {
                    "severity": "error",
                    "code": "duplicate_observation",
                    "message": "Duplicate stored observation for this source and date.",
                    "date": row["date"],
                    "source": row["source"],
                }
            )
        seen.add(key)

        prices = (row["open"], row["high"], row["low"], row["close"])
        if (
            any(not value.is_finite() or value <= 0 for value in prices)
            or row["high"] < max(row["open"], row["close"])
            or row["low"] > min(row["open"], row["close"])
            or row["low"] > row["high"]
        ):
            findings.append(
                {
                    "severity": "error",
                    "code": "invalid_ohlc",
                    "message": "Stored OHLC values are non-positive or inconsistent.",
                    "date": row["date"],
                    "source": row["source"],
                }
            )

    try:
        expected = get_expected_trading_dates(start, end, exchange)
        calendar_available = True
    except UnsupportedTradingCalendarError:
        expected = []
        calendar_available = False
        findings.append(
            {
                "severity": "info",
                "code": "calendar_unavailable",
                "message": "No verified exchange calendar is configured for this exchange and date range.",
                "date": None,
                "source": None,
            }
        )

    missing = [value for value in expected if value not in dates]
    for value in missing:
        findings.append(
            {
                "severity": "warning",
                "code": "missing_trading_session",
                "message": "No stored price observation exists for an expected trading session.",
                "date": value,
                "source": None,
            }
        )

    by_source = {}
    for row in ordered:
        by_source.setdefault(row["source"], []).append(row)

    threshold = Decimal("20")
    for source, source_rows in by_source.items():
        for previous, current in pairwise(source_rows):
            previous_price = previous.get("adjusted_close") or previous["close"]
            current_price = current.get("adjusted_close") or current["close"]
            if (
                not previous_price.is_finite()
                or not current_price.is_finite()
                or previous_price <= 0
            ):
                continue

            change = (
                abs(current_price - previous_price) / previous_price * Decimal("100")
            )
            if change > threshold:
                findings.append(
                    {
                        "severity": "warning",
                        "code": "large_daily_price_movement",
                        "message": f"Price movement is {change:.2f}% between consecutive stored observations.",
                        "date": current["date"],
                        "source": source,
                    }
                )

    timestamps = [
        row["retrieved_at"] for row in ordered if row.get("retrieved_at") is not None
    ]
    latest = max(timestamps) if timestamps else None
    age_hours = None

    if latest is not None:
        if latest.tzinfo is None:
            latest = latest.replace(tzinfo=UTC)
        age = datetime.now(UTC) - latest
        age_hours = round(age.total_seconds() / 3600, 2)
        if age > timedelta(hours=settings.market_data_freshness_hours):
            findings.append(
                {
                    "severity": "warning",
                    "code": "stale_data",
                    "message": f"Latest stored observation exceeds the {settings.market_data_freshness_hours}-hour freshness target.",
                    "date": None,
                    "source": None,
                }
            )
    elif ordered:
        findings.append(
            {
                "severity": "warning",
                "code": "missing_retrieval_timestamp",
                "message": "Stored observations have no retrieval timestamp.",
                "date": None,
                "source": None,
            }
        )

    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    status = "error" if errors else "warning" if warnings else "healthy"
    if not ordered:
        status = "no_data"

    return {
        "symbol": symbol,
        "exchange": exchange,
        "start": start,
        "end": end,
        "status": status,
        "observation_count": len(ordered),
        "distinct_dates": len(dates),
        "expected_sessions": len(expected) if calendar_available else None,
        "missing_sessions": len(missing) if calendar_available else None,
        "calendar_available": calendar_available,
        "latest_retrieved_at": latest,
        "latest_data_age_hours": age_hours,
        "findings": findings,
    }

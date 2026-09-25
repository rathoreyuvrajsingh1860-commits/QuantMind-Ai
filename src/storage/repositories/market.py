from datetime import date
from uuid import UUID

from src.storage.database import get_connection


class MarketRepository:
    """Persistence operations for market data."""

    def get_instrument_id(
        self,
        symbol: str,
        exchange: str | None,
    ) -> UUID | None:
        """Return the database instrument ID for a symbol."""

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id
                    FROM financial_instruments
                    WHERE symbol = %s
                      AND exchange IS NOT DISTINCT FROM %s
                    LIMIT 1
                    """,
                    (
                        symbol,
                        exchange,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                return row[0]

    def get_price_history_coverage(
        self,
        instrument_id: UUID,
    ) -> tuple[date, date] | None:
        """Return the earliest and latest stored price dates."""

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        MIN(price_date),
                        MAX(price_date)
                    FROM price_history
                    WHERE instrument_id = %s
                    """,
                    (instrument_id,),
                )
                row = cursor.fetchone()

        if row is None or row[0] is None or row[1] is None:
            return None

        return row[0], row[1]
    
        

    def get_price_history(
        self,
        instrument_id: UUID,
        start: date,
        end: date,
    ) -> list[dict]:
        """Return stored price history for an instrument."""

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        price_date,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        adjusted_close,
                        source,
                        retrieved_at
                    FROM price_history
                    WHERE instrument_id = %s
                      AND price_date BETWEEN %s AND %s
                    ORDER BY price_date ASC
                    """,
                    (
                        instrument_id,
                        start,
                        end,
                    ),
                )

                rows = cursor.fetchall()

        return [
            {
                "date": row[0],
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
                "volume": row[5],
                "adjusted_close": row[6],
                "source": row[7],
                "retrieved_at": row[8],
            }
            for row in rows
        ]
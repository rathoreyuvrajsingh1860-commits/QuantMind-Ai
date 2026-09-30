from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from psycopg.types.json import Jsonb

from src.ai.models import AIResearchResult
from src.data.models import PriceBar
from src.research.models import ResearchResult
from src.storage.database import get_connection


class ResearchRepository:
    """Persistence boundary for QuantMind research runs and evidence."""

    def save_research(
        self,
        *,
        research: ResearchResult,
        prices: list[PriceBar],
        ai_result: AIResearchResult | None = None,
        status: str = "completed",
    ) -> UUID:
        """
        Persist a complete research run and its evidence atomically.

        The repository intentionally owns persistence details so the
        application/service layer does not contain SQL.
        """

        now = datetime.now(timezone.utc)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                company_id = self._ensure_company(
                    cursor,
                    research,
                )

                instrument_id = self._ensure_instrument(
                    cursor,
                    company_id=company_id,
                    research=research,
                )

                source_ids = self._ensure_sources(
                    cursor,
                    research=research,
                )

                model = ai_result.model if ai_result else None

                answer: str | None = None

                if ai_result is not None:
                    answer = ai_result.analysis.model_dump_json()

                metadata = {
                    "entity": research.entity.model_dump(mode="json"),
                    "market": research.market.model_dump(mode="json"),
                    "limitations": research.limitations,
                    "ai_provider": (
                        ai_result.provider
                        if ai_result is not None
                        else None
                    ),
                    "ai_model": (
                        ai_result.model
                        if ai_result is not None
                        else None
                    ),
                }

                cursor.execute(
                    """
                    INSERT INTO research_runs (
                        company_id,
                        instrument_id,
                        query,
                        status,
                        model,
                        answer,
                        started_at,
                        completed_at,
                        metadata_json
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        company_id,
                        instrument_id,
                        research.query,
                        status,
                        model,
                        answer,
                        now,
                        now,
                        Jsonb(metadata),
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        "Failed to create research run"
                    )

                research_run_id: UUID = row[0]

                self._insert_evidence(
                    cursor,
                    research_run_id=research_run_id,
                    research=research,
                    prices=prices,
                    source_ids=source_ids,
                )

            connection.commit()

        return research_run_id

    @staticmethod
    def _ensure_company(cursor: Any, research: ResearchResult) -> UUID:
        entity = research.entity

        cursor.execute(
            """
            SELECT id
            FROM companies
            WHERE symbol = %s
              AND COALESCE(exchange, '') = COALESCE(%s, '')
            LIMIT 1
            """,
            (
                entity.symbol,
                entity.exchange,
            ),
        )

        row = cursor.fetchone()

        if row:
            company_id = row[0]

            cursor.execute(
                """
                UPDATE companies
                SET
                    name = %s,
                    country = %s,
                    sector = %s,
                    industry = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (
                    entity.name,
                    entity.country,
                    entity.sector,
                    entity.industry,
                    company_id,
                ),
            )

            return company_id

        cursor.execute(
            """
            INSERT INTO companies (
                name,
                symbol,
                exchange,
                country,
                sector,
                industry,
                metadata_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                entity.name,
                entity.symbol,
                entity.exchange,
                entity.country,
                entity.sector,
                entity.industry,
                Jsonb({}),
            ),
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Failed to create company")

        return row[0]

    @staticmethod
    def _ensure_instrument(
        cursor: Any,
        *,
        company_id: UUID,
        research: ResearchResult,
    ) -> UUID:
        entity = research.entity

        cursor.execute(
            """
            SELECT id
            FROM financial_instruments
            WHERE company_id = %s
              AND symbol = %s
              AND COALESCE(exchange, '') = COALESCE(%s, '')
            LIMIT 1
            """,
            (
                company_id,
                entity.symbol,
                entity.exchange,
            ),
        )

        row = cursor.fetchone()

        if row:
            return row[0]

        cursor.execute(
            """
            INSERT INTO financial_instruments (
                company_id,
                symbol,
                exchange,
                instrument_type,
                currency,
                metadata_json
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                company_id,
                entity.symbol,
                entity.exchange,
                "equity",
                entity.currency,
                Jsonb({}),
            ),
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Failed to create financial instrument"
            )

        return row[0]

    @staticmethod
    def _ensure_sources(
        cursor: Any,
        *,
        research: ResearchResult,
    ) -> dict[str, UUID]:
        source_names = {
            evidence.source
            for evidence in research.evidence
        }

        source_ids: dict[str, UUID] = {}

        for source_name in source_names:
            cursor.execute(
                """
                SELECT id
                FROM data_sources
                WHERE name = %s
                   OR provider = %s
                LIMIT 1
                """,
                (
                    source_name,
                    source_name,
                ),
            )

            row = cursor.fetchone()

            if row:
                source_ids[source_name] = row[0]
                continue

            cursor.execute(
                """
                INSERT INTO data_sources (
                    name,
                    source_type,
                    provider,
                    active,
                    metadata_json
                )
                VALUES (%s, %s, %s, TRUE, %s)
                RETURNING id
                """,
                (
                    source_name,
                    "market_data",
                    source_name,
                    Jsonb({}),
                ),
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError(
                    f"Failed to create data source: {source_name}"
                )

            source_ids[source_name] = row[0]

        return source_ids

    @staticmethod
    def _insert_evidence(
        cursor: Any,
        *,
        research_run_id: UUID,
        research: ResearchResult,
        prices: list[PriceBar],
        source_ids: dict[str, UUID],
    ) -> None:
        """
        Store evidence as immutable research observations.

        The research run is kept in metadata so the future Evidence Graph
        can connect claims -> evidence -> source -> research run.
        """

        for bar in prices:
            source_id = source_ids.get(bar.source)

            metadata = {
                "research_run_id": str(research_run_id),
                "symbol": research.entity.symbol,
                "date": bar.date.isoformat(),
                "open": str(bar.open),
                "high": str(bar.high),
                "low": str(bar.low),
                "close": str(bar.close),
                "volume": bar.volume,
                "adjusted_close": (
                    str(bar.adjusted_close)
                    if bar.adjusted_close is not None
                    else None
                ),
            }

            cursor.execute(
                """
                INSERT INTO evidence (
                    source_id,
                    title,
                    source_url,
                    excerpt,
                    published_at,
                    retrieved_at,
                    metadata_json
                )
                VALUES (
                    %s,
                    %s,
                    NULL,
                    %s,
                    NULL,
                    %s,
                    %s
                )
                """,
                (
                    source_id,
                    f"{research.entity.symbol} market data "
                    f"{bar.date.isoformat()}",
                    (
                        f"Daily market observation for "
                        f"{research.entity.symbol} on "
                        f"{bar.date.isoformat()}: "
                        f"close={bar.close}"
                    ),
                    bar.retrieved_at,
                    Jsonb(metadata),
                ),
            )

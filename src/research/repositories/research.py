from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from psycopg.types.json import Jsonb

from src.ai.models import AIResearchResult
from src.data.models import PriceBar
from src.research.models import ResearchResult
from src.storage.database import get_connection
from src.verification.models import VerificationResult


class ResearchRepository:
    """Persistence boundary for QuantMind research runs and evidence."""

    def list_recent_research(
        self,
        *,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Return recent research runs ordered by completion time."""
        if limit < 1:
            raise ValueError("limit must be at least 1")

        limit = min(limit, 100)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        query,
                        status,
                        model,
                        started_at,
                        completed_at,
                        metadata_json
                    FROM research_runs
                    ORDER BY COALESCE(completed_at, started_at) DESC
                    LIMIT %s
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "query": row[1],
                "status": row[2],
                "model": row[3],
                "started_at": row[4],
                "completed_at": row[5],
                "metadata": row[6],
            }
            for row in rows
        ]

    def get_research(
        self,
        research_run_id: UUID,
    ) -> dict[str, Any] | None:
        """Return a persisted research run and its evidence."""
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        query,
                        status,
                        model,
                        answer,
                        started_at,
                        completed_at,
                        metadata_json
                    FROM research_runs
                    WHERE id = %s
                    """,
                    (research_run_id,),
                )

                run = cursor.fetchone()

                if run is None:
                    return None

                cursor.execute(
                    """
                    SELECT
                        source_id,
                        title,
                        source_url,
                        excerpt,
                        published_at,
                        retrieved_at,
                        metadata_json
                    FROM evidence
                    WHERE metadata_json->>'research_run_id' = %s
                    ORDER BY (metadata_json->>'date')::date ASC
                    """,
                    (str(research_run_id),),
                )

                evidence_rows = cursor.fetchall()

        return {
            "id": run[0],
            "query": run[1],
            "status": run[2],
            "model": run[3],
            "answer": run[4],
            "started_at": run[5],
            "completed_at": run[6],
            "metadata": run[7],
            "evidence": [
                {
                    "source_id": row[0],
                    "title": row[1],
                    "source_url": row[2],
                    "excerpt": row[3],
                    "published_at": row[4],
                    "retrieved_at": row[5],
                    "metadata": row[6],
                }
                for row in evidence_rows
            ],
        }

    def create_research_run(
        self,
        *,
        query: str,
        status: str = "running",
        metadata: dict | None = None,
    ) -> UUID:
        """Create a research-run lifecycle record before execution starts."""
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO research_runs (
                        query,
                        status,
                        started_at,
                        metadata_json
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        query,
                        status,
                        datetime.now(timezone.utc),
                        Jsonb(metadata or {}),
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        "Failed to create research run"
                    )

            connection.commit()

        return row[0]

    def update_research_run_status(
        self,
        research_run_id: UUID,
        *,
        status: str,
        metadata: dict | None = None,
    ) -> None:
        """Update research-run lifecycle status and completion metadata."""
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE research_runs
                    SET
                        status = %s,
                        completed_at = %s,
                        metadata_json = COALESCE(
                            metadata_json,
                            '{}'::jsonb
                        ) || %s
                    WHERE id = %s
                    """,
                    (
                        status,
                        datetime.now(timezone.utc),
                        Jsonb(metadata or {}),
                        research_run_id,
                    ),
                )

                if cursor.rowcount != 1:
                    raise RuntimeError(
                        f"Research run not found: {research_run_id}"
                    )

            connection.commit()

    def save_research(
        self,
        *,
        research: ResearchResult,
        prices: list[PriceBar],
        verification: VerificationResult | None = None,
        ai_result: AIResearchResult | None = None,
        status: str = "completed",
        research_run_id: UUID | None = None,
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
                    "coverage": research.coverage.model_dump(mode="json"),
                    "limitations": research.limitations,
                    "verification": (
                        verification.model_dump(mode="json")
                        if verification is not None
                        else None
                    ),
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

                if research_run_id is None:
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

                    research_run_id = row[0]
                else:
                    cursor.execute(
                        """
                        UPDATE research_runs
                        SET
                            company_id = %s,
                            instrument_id = %s,
                            query = %s,
                            status = %s,
                            model = %s,
                            answer = %s,
                            completed_at = %s,
                            metadata_json = %s
                        WHERE id = %s
                        """,
                        (
                            company_id,
                            instrument_id,
                            research.query,
                            status,
                            model,
                            answer,
                            now,
                            Jsonb(metadata),
                            research_run_id,
                        ),
                    )

                    if cursor.rowcount != 1:
                        raise RuntimeError(
                            f"Research run not found: {research_run_id}"
                        )

                evidence_ids = self._insert_evidence(
                    cursor,
                    research_run_id=research_run_id,
                    research=research,
                    prices=prices,
                    source_ids=source_ids,
                )

                self._insert_claims(
                    cursor,
                    research_run_id=research_run_id,
                    research=research,
                    evidence_ids=evidence_ids,
                    verification=verification,
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
    ) -> list[UUID]:
        """
        Store evidence as immutable research observations.

        Returns the evidence IDs created for the research run.
        """

        if not prices:
            return []

        values_sql = []
        parameters: list[Any] = []

        for bar in prices:
            source_id = source_ids.get(bar.source)

            metadata = {
                "research_run_id": str(research_run_id),
                "source": bar.source,
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

            values_sql.append(
                "(%s, %s, NULL, %s, NULL, %s, %s)"
            )

            parameters.extend(
                [
                    source_id,
                    (
                        f"{research.entity.symbol} market data "
                        f"{bar.date.isoformat()}"
                    ),
                    (
                        f"Daily market observation for "
                        f"{research.entity.symbol} on "
                        f"{bar.date.isoformat()}: "
                        f"close={bar.close}"
                    ),
                    bar.retrieved_at,
                    Jsonb(metadata),
                ]
            )

        cursor.execute(
            f"""
            INSERT INTO evidence (
                source_id,
                title,
                source_url,
                excerpt,
                published_at,
                retrieved_at,
                metadata_json
            )
            VALUES {", ".join(values_sql)}
            RETURNING id
            """,
            parameters,
        )

        rows = cursor.fetchall()
        evidence_ids = [row[0] for row in rows]

        if len(evidence_ids) != len(prices):
            raise RuntimeError(
                "Evidence insert returned an unexpected number of IDs"
            )

        return evidence_ids

    @staticmethod
    def _insert_claims(
        cursor: Any,
        *,
        research_run_id: UUID,
        research: ResearchResult,
        evidence_ids: list[UUID],
        verification: VerificationResult | None,
    ) -> None:
        """
        Persist deterministic research claims and link them to evidence.

        Claims are derived from the deterministic research layer rather
        than generated by the AI provider.
        """

        market = research.market

        if not evidence_ids:
            return

        if verification is not None and not verification.passed:
            return

        claims: list[tuple[str, str, str]] = []

        if market.observations > 0 and market.latest_close is not None:
            claims.append(
                (
                    "fact",
                    f"The latest observed closing price was "
                    f"{market.latest_close}.",
                    "supported",
                )
            )

        if market.observations > 0 and market.first_close is not None:
            claims.append(
                (
                    "fact",
                    f"The first observed closing price was "
                    f"{market.first_close}.",
                    "supported",
                )
            )

        if market.absolute_change is not None:
            claims.append(
                (
                    "calculation",
                    f"The absolute change over the research period was "
                    f"{market.absolute_change}.",
                    "supported",
                )
            )

        if market.percentage_change is not None:
            claims.append(
                (
                    "calculation",
                    f"The percentage change over the research period was "
                    f"{market.percentage_change}%.",
                    "supported",
                )
            )

        if market.period_high is not None:
            claims.append(
                (
                    "calculation",
                    f"The period high was {market.period_high}.",
                    "supported",
                )
            )

        if market.period_low is not None:
            claims.append(
                (
                    "calculation",
                    f"The period low was {market.period_low}.",
                    "supported",
                )
            )

        if market.average_close is not None:
            claims.append(
                (
                    "calculation",
                    f"The average closing price was "
                    f"{market.average_close}.",
                    "supported",
                )
            )

        if market.total_volume is not None:
            claims.append(
                (
                    "calculation",
                    f"Total observed volume was {market.total_volume}.",
                    "supported",
                )
            )

        for claim_type, claim_text, status in claims:
            cursor.execute(
                """
                INSERT INTO research_claims (
                    research_run_id,
                    claim_type,
                    claim_text,
                    status,
                    metadata_json
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id
                """,
                (
                    research_run_id,
                    claim_type,
                    claim_text,
                    status,
                    Jsonb({}),
                ),
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Failed to create research claim")

            claim_id = row[0]

            claim_evidence_rows = [
                (
                    claim_id,
                    evidence_id,
                    "supports",
                )
                for evidence_id in evidence_ids
            ]

            cursor.executemany(
                """
                INSERT INTO claim_evidence (
                claim_id,
                evidence_id,
                relationship
                )
                VALUES (
                %s,
                %s,
                %s
                )
                ON CONFLICT (
                claim_id,
                evidence_id,
                relationship
                ) DO NOTHING
                """,
                claim_evidence_rows,
            )
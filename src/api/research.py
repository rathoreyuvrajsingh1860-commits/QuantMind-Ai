from datetime import date
import json
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from src.ai.models import AIResearchResult
from src.ai.providers import OpenAICompatibleProvider
from src.ai.service import AIResearchService
from src.config.settings import settings
from src.data.market_service import MarketService
from src.data.service import create_data_service
from src.research.models import ResearchResult
from src.research.repositories.research import ResearchRepository
from src.research.service import ResearchService
from src.verification.models import VerificationResult
from src.verification.service import VerificationService


router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    start: date | None = None
    end: date | None = None


class ResearchHistoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    query: str
    status: str
    model: str | None = None
    started_at: str
    completed_at: str | None = None


class ResearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research_run_id: str
    research: ResearchResult
    verification: VerificationResult | None
    ai_analysis: AIResearchResult | None = None


def create_research_service() -> ResearchService:
    data_service = create_data_service()
    market_service = MarketService(data_service)
    return ResearchService(market_service)


def create_ai_research_service() -> AIResearchService | None:
    if not settings.ai_api_key or not settings.ai_model:
        return None

    provider = OpenAICompatibleProvider(
        api_key=settings.ai_api_key,
        model=settings.ai_model,
        base_url=settings.ai_base_url,
    )

    return AIResearchService(provider)


@router.get("/history", response_model=list[ResearchHistoryItem])
def research_history(limit: int = 20) -> list[ResearchHistoryItem]:
    repository = ResearchRepository()

    try:
        rows = repository.list_recent_research(limit=limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return [
        ResearchHistoryItem(
            id=str(row["id"]),
            query=row["query"],
            status=row["status"],
            model=row["model"],
            started_at=row["started_at"].isoformat(),
            completed_at=(
                row["completed_at"].isoformat()
                if row["completed_at"] is not None
                else None
            ),
        )
        for row in rows
    ]



@router.get("/{research_run_id}", response_model=ResearchResponse)
def get_research(research_run_id: str) -> ResearchResponse:
    try:
        run_id = UUID(research_run_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid research run ID",
        ) from exc

    repository = ResearchRepository()
    persisted = repository.get_research(run_id)

    if persisted is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    if persisted["status"] in {"running", "failed"}:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Research run cannot be restored while its status "
                f"is '{persisted['status']}'"
            ),
        )

    metadata = persisted["metadata"]

    evidence = [
        {
            "source": item["metadata"]["source"],
            "retrieved_at": item["retrieved_at"],
            "description": item["excerpt"] or item["title"] or "",
        }
        for item in persisted["evidence"]
    ]

    market_metadata = metadata["market"]

    coverage = metadata.get("coverage")
    limitations = list(metadata.get("limitations", []))

    if coverage is None:
        # Legacy research runs predate persisted coverage metadata.
        # Reconstruct requested period from the persisted market payload,
        # but derive evidence coverage from the actual persisted evidence rows.
        evidence_dates = [
            item["metadata"].get("date")
            for item in persisted["evidence"]
            if item["metadata"].get("date")
        ]

        coverage = {
            "requested_start": market_metadata["start"],
            "requested_end": market_metadata["end"],
            "evidence_start": evidence_dates[0] if evidence_dates else None,
            "evidence_end": evidence_dates[-1] if evidence_dates else None,
            "observations": len(persisted["evidence"]),
        }

        limitations.append(
            "Historical run predates coverage tracking; "
            "requested period was reconstructed from persisted market metadata "
            "and evidence coverage was derived from persisted evidence rows."
        )

    research_payload = {
        "query": persisted["query"],
        "entity": metadata["entity"],
        "market": market_metadata,
        "coverage": coverage,
        "evidence": evidence,
        "limitations": limitations,
    }

    research = ResearchResult.model_validate(research_payload)

    verification_data = metadata.get("verification")

    verification = (
        VerificationResult.model_validate(verification_data)
        if verification_data is not None
        else None
    )

    ai_result = None

    if persisted["answer"]:
        try:
            analysis_payload = json.loads(persisted["answer"])
            ai_result = AIResearchResult(
                analysis=analysis_payload,
                provider=metadata.get("ai_provider") or "unknown",
                model=persisted["model"] or metadata.get("ai_model") or "unknown",
            )
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=500,
                detail="Persisted AI analysis is invalid",
            ) from exc

    return ResearchResponse(
        research_run_id=str(persisted["id"]),
        research=research,
        verification=verification,
        ai_analysis=ai_result,
    )

@router.post("", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    service = create_research_service()
    repository = ResearchRepository()
    verifier = VerificationService()
    research_run_id: UUID | None = None

    try:
        research_run_id = repository.create_research_run(
            query=request.query,
        )

        result = service.research(
            request.query,
            start=request.start,
            end=request.end,
        )

        verification = verifier.verify_market_research(
            market=result.market,
            prices=service.last_prices,
        )

        ai_result = None

        if verification.passed:
            ai_service = create_ai_research_service()

            if ai_service is not None:
                try:
                    ai_result = ai_service.analyze(result)
                except Exception:
                    # AI failure must not destroy deterministic research.
                    ai_result = None

        research_run_id = repository.save_research(
            research=result,
            prices=service.last_prices,
            verification=verification,
            ai_result=ai_result,
            status="completed" if verification.passed else "verification_failed",
            research_run_id=research_run_id,
        )

        return ResearchResponse(
            research_run_id=str(research_run_id),
            research=result,
            verification=verification,
            ai_analysis=ai_result,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        if research_run_id is not None:
            try:
                repository.update_research_run_status(
                    research_run_id,
                    status="failed",
                )
            except Exception:
                pass

        raise

    finally:
        service.close()
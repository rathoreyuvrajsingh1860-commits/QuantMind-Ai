from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from src.ai.models import AIResearchResult
from src.ai.providers import OpenAICompatibleProvider
from src.ai.service import AIResearchService
from src.config.settings import settings
from src.data.market_service import MarketService
from src.data.service import DataService
from src.research.models import ResearchResult
from src.research.repositories.research import ResearchRepository
from src.research.service import ResearchService


router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    start: date | None = None
    end: date | None = None


class ResearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research_run_id: str
    research: ResearchResult
    ai_analysis: AIResearchResult | None = None


def create_research_service() -> ResearchService:
    data_service = DataService.from_settings()
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


@router.post("", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    service = create_research_service()
    repository = ResearchRepository()

    try:
        result = service.research(
            request.query,
            start=request.start,
            end=request.end,
        )

        ai_result = None
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
            ai_result=ai_result,
            status="completed",
        )

        return ResearchResponse(
            research_run_id=str(research_run_id),
            research=result,
            ai_analysis=ai_result,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        service.close()

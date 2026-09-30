from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from src.ai.providers import OpenAICompatibleProvider
from src.ai.service import AIResearchService
from src.config.settings import settings
from src.data.service import DataService
from src.data.market_service import MarketService
from src.research.service import ResearchService


router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    start: date | None = None
    end: date | None = None


class ResearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research: object
    ai_analysis: object | None = None


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

    try:
        result = service.run(
            request.query,
            start=request.start,
            end=request.end,
        )

        ai_service = create_ai_research_service()

        if ai_service is None:
            return ResearchResponse(
                research=result,
                ai_analysis=None,
            )

        try:
            ai_result = ai_service.analyze(result)
        except Exception as exc:
            # Research data remains usable even when the AI layer fails.
            return ResearchResponse(
                research=result,
                ai_analysis={
                    "error": "AI analysis unavailable",
                    "detail": str(exc),
                },
            )

        return ResearchResponse(
            research=result,
            ai_analysis=ai_result,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    finally:
        service.market_service.data_service.close()

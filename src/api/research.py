from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from src.data.market_service import MarketService
from src.data.service import create_data_service
from src.research.models import ResearchResult
from src.research.service import ResearchService


router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=200)
    start: date | None = None
    end: date | None = None


def create_research_service() -> ResearchService:
    data_service = create_data_service()
    market_service = MarketService(data_service)

    return ResearchService(market_service)


@router.post("", response_model=ResearchResult)
def research(request: ResearchRequest) -> ResearchResult:
    service = create_research_service()

    try:
        return service.research(
            request.query,
            start=request.start,
            end=request.end,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    finally:
        service.close()

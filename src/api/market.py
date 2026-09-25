from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import (
    MarketProfileResponse,
    PriceHistoryResponse,
)
from src.data.market_service import MarketService
from src.data.service import create_data_service


router = APIRouter(
    prefix="/market",
    tags=["market"],
)


def create_market_service() -> MarketService:
    """Create the application market-data service."""
    return MarketService(create_data_service())


@router.get(
    "/{symbol:path}/profile",
    response_model=MarketProfileResponse,
)
def get_market_profile(symbol: str) -> MarketProfileResponse:
    """Return normalized company/instrument information."""

    service = create_market_service()

    try:
        profile = service.get_profile(symbol)

        return MarketProfileResponse(
            symbol=profile.symbol,
            name=profile.name,
            exchange=profile.exchange,
            country=profile.country,
            sector=profile.sector,
            industry=profile.industry,
            currency=profile.currency,
        )

    except (ValueError, LookupError, RuntimeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    finally:
        service.close()


@router.get(
    "/{symbol:path}/prices",
    response_model=PriceHistoryResponse,
)
def get_market_prices(
    symbol: str,
    start: date = Query(...),
    end: date = Query(...),
) -> PriceHistoryResponse:
    """Return historical daily prices."""

    if start > end:
        raise HTTPException(
            status_code=400,
            detail="start date must be before or equal to end date",
        )

    service = create_market_service()

    try:
        prices = service.get_price_history(
            symbol,
            start,
            end,
        )

        return PriceHistoryResponse(
            symbol=symbol,
            start=start,
            end=end,
            count=len(prices),
            data=prices,
        )

    except (ValueError, LookupError, RuntimeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    finally:
        service.close()
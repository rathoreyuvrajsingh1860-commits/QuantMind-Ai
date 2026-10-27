from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import (
    MarketProfileResponse,
    PriceHistoryResponse,
)
from src.data.errors import ProviderError
from src.data.market_service import MarketService
from src.data.service import create_data_service

router = APIRouter(
    prefix="/market",
    tags=["market"],
)


def create_market_service() -> MarketService:
    """Create the application market-data service."""
    return MarketService(create_data_service())


def _raise_market_http_error(exc: Exception) -> None:
    """Translate market-data exceptions into HTTP responses."""
    message = str(exc)

    if isinstance(exc, ValueError):
        raise HTTPException(
            status_code=400,
            detail=message,
        ) from exc

    if isinstance(exc, LookupError):
        status_code = 404 if "company not found" in message.lower() else 502
        raise HTTPException(
            status_code=status_code,
            detail=message,
        ) from exc

    if isinstance(exc, (ProviderError, RuntimeError)):
        raise HTTPException(
            status_code=502,
            detail=message,
        ) from exc

    raise exc


@router.get(
    "/search",
    response_model=list[MarketProfileResponse],
)
def search_market_instruments(
    q: str = Query(..., min_length=1, max_length=100),
) -> list[MarketProfileResponse]:
    """Search supported market instruments through configured providers."""
    query = q.strip()

    if not query:
        raise HTTPException(
            status_code=422,
            detail="Search query cannot be empty",
        )

    service = create_market_service()

    try:
        results = service.data_service.search_company(query)

        return [
            MarketProfileResponse(
                symbol=item.symbol,
                name=item.name,
                exchange=item.exchange,
                country=item.country,
                sector=item.sector,
                industry=item.industry,
                currency=item.currency,
            )
            for item in results[:20]
        ]
    except (ProviderError, ValueError, LookupError, RuntimeError) as exc:
        _raise_market_http_error(exc)
    finally:
        service.close()


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
    except (ProviderError, ValueError, LookupError, RuntimeError) as exc:
        _raise_market_http_error(exc)
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
    except (ProviderError, ValueError, LookupError, RuntimeError) as exc:
        _raise_market_http_error(exc)
    finally:
        service.close()

from fastapi import APIRouter

from src.storage.database import get_connection
from src.api.market import router as market_router


router = APIRouter(prefix="/api")

router.include_router(market_router)


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "quantmind-ai",
    }


@router.get("/health/database")
def database_health_check() -> dict[str, str]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

    return {
        "status": "ok",
        "database": "connected",
    }

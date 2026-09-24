import psycopg

from src.config.settings import settings


def get_connection() -> psycopg.Connection:
    """Create a PostgreSQL connection using the application settings."""
    return psycopg.connect(
        settings.database_url,
        connect_timeout=10,
    )
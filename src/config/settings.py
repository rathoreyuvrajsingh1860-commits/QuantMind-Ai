from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "quantmind-ai"
    app_version: str = "0.1.0"

    api_host: str = "127.0.0.1"
    api_port: int = 8000

    database_url: str = ""

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    ai_fallback_model: str = ""

    financial_data_provider: str = ""
    financial_data_api_key: str = ""

    secret_key: str = ""

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
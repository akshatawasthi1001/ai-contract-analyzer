from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    app_name: str = "AI Contract Analyzer API"
    app_version: str = "1.0.0"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # Database settings
    database_host: str = "postgres"
    database_port: int = 5432
    database_name: str = "contract_analyzer"
    database_user: str = "postgres"
    database_password: str = "postgres"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
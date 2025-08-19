from __future__ import annotations

from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from env vars (and a .env file in dev).

    Priority order (highest first):
      1) Environment variables
      2) .env file at project root (dev)
      3) Defaults below
    """

    # pydantic-settings (v2) configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    APP_NAME: str = "Template API"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: SecretStr = Field(default=SecretStr("postgres"))
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "app"
    # Build metadata (optionally set by CI)
    BUILD_SHA: str | None = None
    BUILD_DATE: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy/psycopg-style DSN built from individual DB_* fields.
        Example: postgresql+psycopg://user:pass@host:5432/dbname
        """
        pwd = self.DB_PASSWORD.get_secret_value()
        return f"postgresql+psycopg://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Singleton settings object to import elsewhere
settings = Settings()

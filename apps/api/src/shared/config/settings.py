from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["dev", "staging", "prod"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Environment = "dev"
    log_level: str = "INFO"

    host: str = "0.0.0.0"
    port: int = 8000

    cors_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
        ]
    )

    pocketbase_url: str = "http://localhost:8090"
    pocketbase_admin_email: str = ""
    pocketbase_admin_password: str = ""

    openai_api_key: str = ""
    openai_base_url: str = "https://api.groq.com/openai/v1"
    ai_model: str = "llama-3.3-70b-versatile"

    submit_rate_limit: str = "5/minute"

    @property
    def is_production(self) -> bool:
        return self.environment == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()

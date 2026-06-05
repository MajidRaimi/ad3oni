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
    ai_model: str = "openai/gpt-oss-120b"

    redis_url: str = "redis://localhost:6379/0"

    compliance_effort: str = "high"
    spelling_effort: str = "low"
    dedup_effort: str = "medium"
    diacritization_effort: str = "medium"
    categorization_effort: str = "medium"

    diacritization_mode: Literal["partial", "full"] = "partial"
    diacritization_max_attempts: int = 2
    diacritization_verify_enabled: bool = True

    worker_max_jobs: int = 1
    job_max_tries: int = 3
    job_timeout: int = 120

    submit_rate_limit: str = "5/minute"

    discord_public_key: str = ""
    discord_app_id: str = ""
    discord_bot_token: str = ""
    discord_guild_id: str = ""
    discord_schedule_limit: int = 15

    @property
    def is_production(self) -> bool:
        return self.environment == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()

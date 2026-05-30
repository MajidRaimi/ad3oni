from pydantic import BaseModel

from src.shared.config.settings import Environment


class HealthStatus(BaseModel):
    status: str
    environment: Environment

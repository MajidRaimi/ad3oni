from dataclasses import dataclass

from openai import AsyncOpenAI

from src.shared.config.settings import Settings
from src.shared.pocketbase.client import PocketBaseClient


@dataclass(slots=True)
class AppState:
    settings: Settings
    pocketbase: PocketBaseClient
    ai: AsyncOpenAI

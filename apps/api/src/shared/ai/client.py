from openai import AsyncOpenAI

from src.shared.config.settings import Settings


def create_ai_client(settings: Settings) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

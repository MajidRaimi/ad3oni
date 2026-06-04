from dataclasses import dataclass
from typing import Any

import httpx
from openai import AsyncOpenAI

from src.shared.config.settings import Settings
from src.shared.pocketbase.client import PocketBaseClient

_CONTEXT_KEY = "worker_context"


@dataclass(slots=True)
class WorkerContext:
    settings: Settings
    pocketbase: PocketBaseClient
    ai: AsyncOpenAI
    http: httpx.AsyncClient


def set_worker_context(ctx: dict[Any, Any], context: WorkerContext) -> None:
    ctx[_CONTEXT_KEY] = context


def get_worker_context(ctx: dict[Any, Any]) -> WorkerContext:
    context: WorkerContext = ctx[_CONTEXT_KEY]
    return context

from typing import Annotated

from arq import ArqRedis
from fastapi import Depends, Request

from src.shared.pocketbase.client import PocketBaseClient


def get_pocketbase(request: Request) -> PocketBaseClient:
    client: PocketBaseClient = request.app.state.app_state.pocketbase
    return client


def get_queue(request: Request) -> ArqRedis:
    queue: ArqRedis = request.app.state.app_state.queue
    return queue


PocketBaseDep = Annotated[PocketBaseClient, Depends(get_pocketbase)]
QueueDep = Annotated[ArqRedis, Depends(get_queue)]

from typing import Annotated

from fastapi import Depends, Request

from src.shared.pocketbase.client import PocketBaseClient


def get_pocketbase(request: Request) -> PocketBaseClient:
    client: PocketBaseClient = request.app.state.app_state.pocketbase
    return client


PocketBaseDep = Annotated[PocketBaseClient, Depends(get_pocketbase)]

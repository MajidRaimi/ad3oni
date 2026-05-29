from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"

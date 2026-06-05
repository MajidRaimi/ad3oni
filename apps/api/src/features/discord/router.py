import json

from fastapi import APIRouter, BackgroundTasks, Request, Response
from fastapi.responses import JSONResponse

from src.features.discord.handlers import DiscordDeps, handle_interaction
from src.features.discord.keys import PING, PONG
from src.features.discord.verify import verify_signature

router = APIRouter(prefix="/discord", tags=["discord"])


@router.post("/interactions")
async def interactions(request: Request, background_tasks: BackgroundTasks) -> Response:
    body = await request.body()
    signature = request.headers.get("X-Signature-Ed25519", "")
    timestamp = request.headers.get("X-Signature-Timestamp", "")

    state = request.app.state.app_state
    if not verify_signature(
        state.settings.discord_public_key, signature, timestamp, body
    ):
        return Response(status_code=401)

    payload = json.loads(body)
    if payload.get("type") == PING:
        return JSONResponse({"type": PONG})

    deps = DiscordDeps(
        settings=state.settings,
        pocketbase=state.pocketbase,
        queue=state.queue,
        ai=state.ai,
        http=state.http,
    )
    result = await handle_interaction(payload, deps)
    if result.background is not None:
        background_tasks.add_task(result.background)
    return JSONResponse(result.response)

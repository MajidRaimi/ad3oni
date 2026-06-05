from typing import Any

import httpx

from src.features.discord.keys import DISCORD_API_BASE


class DiscordRest:
    def __init__(self, http: httpx.AsyncClient, bot_token: str) -> None:
        self._http = http
        self._token = bot_token

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bot {self._token}"}

    async def post_message(
        self, channel_id: str, embed: dict[str, Any]
    ) -> httpx.Response:
        return await self._http.post(
            f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
            headers=self._headers,
            json={"embeds": [embed]},
        )

    async def edit_original(
        self,
        app_id: str,
        interaction_token: str,
        embed: dict[str, Any],
        components: list[dict[str, Any]] | None = None,
    ) -> httpx.Response:
        payload: dict[str, Any] = {"embeds": [embed]}
        if components is not None:
            payload["components"] = components
        return await self._http.patch(
            f"{DISCORD_API_BASE}/webhooks/{app_id}/{interaction_token}/messages/@original",
            json=payload,
        )

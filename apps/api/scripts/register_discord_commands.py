import asyncio
import sys

import httpx
from src.features.discord.commands import command_definitions
from src.features.discord.keys import DISCORD_API_BASE
from src.shared.config.settings import get_settings


async def main() -> None:
    settings = get_settings()
    if not settings.discord_bot_token or not settings.discord_app_id:
        print("missing DISCORD_BOT_TOKEN or DISCORD_APP_ID")
        return

    guild = "" if "--global" in sys.argv else settings.discord_guild_id
    if guild:
        url = (
            f"{DISCORD_API_BASE}/applications/{settings.discord_app_id}"
            f"/guilds/{guild}/commands"
        )
        scope = f"guild {guild}"
    else:
        url = f"{DISCORD_API_BASE}/applications/{settings.discord_app_id}/commands"
        scope = "global"

    headers = {"Authorization": f"Bot {settings.discord_bot_token}"}
    async with httpx.AsyncClient(timeout=30.0) as http:
        response = await http.put(url, headers=headers, json=command_definitions())
        response.raise_for_status()
        print(f"registered {len(response.json())} commands ({scope})")


if __name__ == "__main__":
    asyncio.run(main())

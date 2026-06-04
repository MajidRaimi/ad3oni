import asyncio
import json
from typing import Any

import httpx
from src.shared.config.settings import get_settings

_REMOVED_FIELDS = ("text_original", "text_diacritized", "diacritization_confidence")


async def _authenticate(
    http: httpx.AsyncClient, base: str, email: str, password: str
) -> dict[str, str]:
    response = await http.post(
        f"{base}/api/collections/_superusers/auth-with-password",
        json={"identity": email, "password": password},
    )
    response.raise_for_status()
    return {"Authorization": response.json()["token"]}


async def _delete_all_prayers(
    http: httpx.AsyncClient, base: str, headers: dict[str, str]
) -> None:
    deleted = 0
    while True:
        response = await http.get(
            f"{base}/api/collections/prayers/records",
            headers=headers,
            params={"perPage": 200, "page": 1, "skipTotal": True},
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        if not items:
            break
        for item in items:
            removal = await http.delete(
                f"{base}/api/collections/prayers/records/{item['id']}",
                headers=headers,
            )
            removal.raise_for_status()
            deleted += 1
    print(f"deleted {deleted} prayers")


async def _drop_fields(
    http: httpx.AsyncClient, base: str, headers: dict[str, str]
) -> None:
    response = await http.get(f"{base}/api/collections/prayers", headers=headers)
    response.raise_for_status()
    collection: dict[str, Any] = response.json()
    print(json.dumps(collection, ensure_ascii=False, indent=2))

    fields = [
        field
        for field in collection["fields"]
        if field["name"] not in _REMOVED_FIELDS
    ]
    indexes: list[str] = collection.get("indexes", [])

    patch = await http.patch(
        f"{base}/api/collections/{collection['id']}",
        headers=headers,
        json={"fields": fields, "indexes": indexes},
    )
    patch.raise_for_status()
    print("dropped fields:", ", ".join(_REMOVED_FIELDS))


async def main() -> None:
    settings = get_settings()
    base = settings.pocketbase_url.rstrip("/")
    async with httpx.AsyncClient(timeout=60.0) as http:
        headers = await _authenticate(
            http,
            base,
            settings.pocketbase_admin_email,
            settings.pocketbase_admin_password,
        )
        await _delete_all_prayers(http, base, headers)
        await _drop_fields(http, base, headers)


if __name__ == "__main__":
    asyncio.run(main())

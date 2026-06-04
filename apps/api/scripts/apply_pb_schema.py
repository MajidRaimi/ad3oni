import asyncio
import json
from typing import Any

import httpx
from src.shared.arabic.normalize import normalize_arabic
from src.shared.config.settings import get_settings

_PRAYER_TEXT_FIELDS = [
    "text_original",
    "text_diacritized",
    "normalized",
    "text_hash",
    "rejection_reason",
    "ai_model",
]
_PRAYER_STATUS_VALUES = ["processing", "rejected", "duplicate", "failed"]
_TAXONOMY_COLLECTIONS = ["categories", "types", "groups"]


def _text_field(name: str) -> dict[str, Any]:
    return {"name": name, "type": "text", "required": False, "hidden": False}


async def _get_collection(
    http: httpx.AsyncClient, base: str, headers: dict[str, str], name: str
) -> dict[str, Any]:
    response = await http.get(f"{base}/api/collections/{name}", headers=headers)
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return data


async def _patch_collection(
    http: httpx.AsyncClient,
    base: str,
    headers: dict[str, str],
    collection_id: str,
    payload: dict[str, Any],
) -> None:
    response = await http.patch(
        f"{base}/api/collections/{collection_id}", headers=headers, json=payload
    )
    response.raise_for_status()


def _ensure_index(indexes: list[str], index_name: str, table: str, column: str) -> None:
    if any(column in index for index in indexes):
        return
    indexes.append(f"CREATE INDEX `{index_name}` ON `{table}` (`{column}`)")


def _field_names(fields: list[dict[str, Any]]) -> set[str]:
    return {field["name"] for field in fields}


async def _migrate_prayers(http: httpx.AsyncClient, base: str, headers: dict[str, str]) -> None:
    collection = await _get_collection(http, base, headers, "prayers")
    print(json.dumps(collection, ensure_ascii=False, indent=2))

    fields: list[dict[str, Any]] = collection["fields"]
    names = _field_names(fields)

    for name in _PRAYER_TEXT_FIELDS:
        if name not in names:
            fields.append(_text_field(name))

    if "processed_at" not in names:
        fields.append({"name": "processed_at", "type": "date", "required": False, "hidden": False})
    if "diacritization_confidence" not in names:
        fields.append(
            {
                "name": "diacritization_confidence",
                "type": "number",
                "required": False,
                "hidden": False,
            }
        )
    if "duplicate_of" not in names:
        fields.append(
            {
                "name": "duplicate_of",
                "type": "relation",
                "required": False,
                "hidden": False,
                "maxSelect": 1,
                "minSelect": 0,
                "collectionId": collection["id"],
                "cascadeDelete": False,
            }
        )

    for field in fields:
        if field["name"] == "status":
            for value in _PRAYER_STATUS_VALUES:
                if value not in field["values"]:
                    field["values"].append(value)

    indexes: list[str] = collection.get("indexes", [])
    _ensure_index(indexes, "idx_prayers_text_hash", "prayers", "text_hash")

    await _patch_collection(
        http, base, headers, collection["id"], {"fields": fields, "indexes": indexes}
    )
    print("migrated prayers")


async def _backfill_name_normalized(
    http: httpx.AsyncClient, base: str, headers: dict[str, str], collection: str
) -> None:
    page = 1
    while True:
        response = await http.get(
            f"{base}/api/collections/{collection}/records",
            headers=headers,
            params={"perPage": 200, "page": page},
        )
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            if item.get("name_normalized"):
                continue
            await http.patch(
                f"{base}/api/collections/{collection}/records/{item['id']}",
                headers=headers,
                json={"name_normalized": normalize_arabic(item.get("name", ""))},
            )
        if page >= data.get("totalPages", 1):
            return
        page += 1


async def _migrate_taxonomy(
    http: httpx.AsyncClient, base: str, headers: dict[str, str], collection: str
) -> None:
    record = await _get_collection(http, base, headers, collection)
    fields: list[dict[str, Any]] = record["fields"]
    if "name_normalized" not in _field_names(fields):
        fields.append(_text_field("name_normalized"))

    indexes: list[str] = record.get("indexes", [])
    _ensure_index(indexes, f"idx_{collection}_name_normalized", collection, "name_normalized")

    await _patch_collection(
        http, base, headers, record["id"], {"fields": fields, "indexes": indexes}
    )
    await _backfill_name_normalized(http, base, headers, collection)
    print(f"migrated {collection}")


async def _authenticate(
    http: httpx.AsyncClient, base: str, email: str, password: str
) -> dict[str, str]:
    response = await http.post(
        f"{base}/api/collections/_superusers/auth-with-password",
        json={"identity": email, "password": password},
    )
    response.raise_for_status()
    return {"Authorization": response.json()["token"]}


async def main() -> None:
    settings = get_settings()
    base = settings.pocketbase_url.rstrip("/")
    async with httpx.AsyncClient(timeout=60.0) as http:
        headers = await _authenticate(
            http, base, settings.pocketbase_admin_email, settings.pocketbase_admin_password
        )
        await _migrate_prayers(http, base, headers)
        for collection in _TAXONOMY_COLLECTIONS:
            await _migrate_taxonomy(http, base, headers, collection)


if __name__ == "__main__":
    asyncio.run(main())

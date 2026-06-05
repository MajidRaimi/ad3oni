import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from src.features.seed.schema import VerifiedEntry
from src.shared.arabic.hashing import text_hash
from src.shared.arabic.normalize import normalize_arabic
from src.shared.config.settings import get_settings
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.pocketbase.filters import quote

_VERIFIED = (
    Path(__file__).resolve().parent.parent / "src" / "features" / "seed" / "verified.json"
)
_TYPE_SLUGS = ["quranic", "prophetic", "athar", "custom"]


async def _resolve(pb: PocketBaseClient, collection: str, slug: str) -> str | None:
    record = await pb.get_first(collection, f"slug = {quote(slug)}")
    return record["id"] if record else None


async def _has_source_field(pb: PocketBaseClient) -> bool:
    data = await pb.list_records("prayers", {"perPage": 1, "skipTotal": True})
    items = data.get("items", [])
    if not items:
        return True
    return "source" in items[0]


async def _exists(pb: PocketBaseClient, digest: str) -> bool:
    record = await pb.get_first("prayers", f"text_hash = {quote(digest)}")
    return record is not None


async def main() -> None:
    entries = [
        VerifiedEntry.model_validate(item)
        for item in json.loads(_VERIFIED.read_text(encoding="utf-8"))
    ]
    publishable = [entry for entry in entries if entry.verdict == "auto_publish"]

    settings = get_settings()
    async with httpx.AsyncClient(timeout=60.0) as http:
        pb = PocketBaseClient(
            settings.pocketbase_url,
            http,
            settings.pocketbase_admin_email,
            settings.pocketbase_admin_password,
        )
        await pb.authenticate()

        type_ids = {slug: await _resolve(pb, "types", slug) for slug in _TYPE_SLUGS}
        category_slugs = {entry.category_slug for entry in publishable}
        category_ids = {slug: await _resolve(pb, "categories", slug) for slug in category_slugs}
        with_source = await _has_source_field(pb)

        missing = [s for s, i in {**type_ids, **category_ids}.items() if i is None]
        if missing:
            raise SystemExit(f"missing slugs: {missing}")

        inserted = 0
        skipped = 0
        for entry in publishable:
            normalized = normalize_arabic(entry.text)
            digest = text_hash(normalized)
            if await _exists(pb, digest):
                skipped += 1
                continue
            payload: dict[str, Any] = {
                "text": entry.text,
                "normalized": normalized,
                "text_hash": digest,
                "status": "confirmed",
                "category": category_ids[entry.category_slug],
                "type": type_ids[entry.type_slug],
                "ai_model": "seed",
                "processed_at": datetime.now(tz=UTC).isoformat(),
            }
            if with_source:
                payload["source"] = entry.source
            await pb.create_record("prayers", payload)
            inserted += 1

    print(f"publishable: {len(publishable)} | inserted: {inserted} | skipped: {skipped}")


if __name__ == "__main__":
    asyncio.run(main())

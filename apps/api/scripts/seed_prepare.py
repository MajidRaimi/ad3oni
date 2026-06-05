import asyncio
import json
from pathlib import Path

import httpx
from src.features.seed.data import SEED_ENTRIES
from src.features.seed.quran import fetch_ayah, verify_quranic

_SEED_DIR = Path(__file__).resolve().parent.parent / "src" / "features" / "seed"
_OUTPUT = _SEED_DIR / "candidates.json"


async def main() -> None:
    candidates: list[dict[str, object]] = []
    async with httpx.AsyncClient(timeout=30.0) as http:
        for entry in SEED_ENTRIES:
            text = entry.text
            quran_verified = False
            if entry.type_slug == "quranic" and entry.quran_ref is not None:
                ayah = await fetch_ayah(http, *entry.quran_ref)
                ok, resolved = verify_quranic(entry.text, entry.dua_substring, ayah)
                quran_verified = ok
                if ok:
                    text = resolved
            candidates.append(
                {
                    "text": text,
                    "type_slug": entry.type_slug,
                    "category_slug": entry.category_slug,
                    "source": entry.source,
                    "is_quranic": entry.type_slug == "quranic",
                    "quran_verified": quran_verified,
                }
            )
    _OUTPUT.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    quranic_ok = sum(1 for c in candidates if c["is_quranic"] and c["quran_verified"])
    quranic_total = sum(1 for c in candidates if c["is_quranic"])
    print(f"candidates: {len(candidates)} | quranic verified: {quranic_ok}/{quranic_total}")
    print(f"written: {_OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())

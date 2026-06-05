import json
from pathlib import Path
from typing import Any

from src.features.seed.schema import VerifiedEntry
from src.shared.arabic.hashing import text_hash
from src.shared.arabic.normalize import harakat_preserves_wording, normalize_arabic

_SEED_DIR = Path(__file__).resolve().parent.parent / "src" / "features" / "seed"
_CANDIDATES = _SEED_DIR / "candidates.json"
_OUTPUT = _SEED_DIR / "verified.json"
_VERDICT_FILES = [
    Path("/tmp/seed_verdicts_A.json"),
    Path("/tmp/seed_verdicts_B.json"),
    Path("/tmp/seed_verdicts_C.json"),
]


def _load_verdicts(path: Path) -> dict[int, dict[str, Any]]:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].lstrip("json").strip()
    items: list[dict[str, Any]] = json.loads(raw)
    return {int(item["i"]): item for item in items}


def _pick_text(candidate_text: str, verdicts: list[dict[str, Any]]) -> str:
    for verdict in verdicts:
        corrected = str(verdict.get("corrected_text") or "").strip()
        if corrected and harakat_preserves_wording(candidate_text, corrected):
            return corrected
    return candidate_text


def _resolve_taxonomy(
    candidate: dict[str, Any], verdicts: list[dict[str, Any]], key: str, suggestion: str
) -> str:
    field = "category_slug" if key == "category_ok" else "type_slug"
    ok_votes = sum(1 for v in verdicts if v.get(key) is True)
    if ok_votes * 2 >= len(verdicts):
        return str(candidate[field])
    suggestions = [v.get(suggestion) for v in verdicts if v.get(suggestion)]
    for value in suggestions:
        if suggestions.count(value) >= 2:
            return str(value)
    return str(candidate[field])


def main() -> None:
    candidates: list[dict[str, Any]] = json.loads(
        _CANDIDATES.read_text(encoding="utf-8")
    )
    verdict_maps = [_load_verdicts(path) for path in _VERDICT_FILES]

    verified: list[VerifiedEntry] = []
    dropped: list[dict[str, Any]] = []
    review: list[dict[str, Any]] = []

    for index, candidate in enumerate(candidates):
        if candidate["is_quranic"]:
            verdict = "auto_publish" if candidate["quran_verified"] else "human_review"
            text = str(candidate["text"])
            normalized = normalize_arabic(text)
            verified.append(
                VerifiedEntry(
                    text=text,
                    type_slug=str(candidate["type_slug"]),
                    category_slug=str(candidate["category_slug"]),
                    source=str(candidate["source"]),
                    normalized=normalized,
                    text_hash=text_hash(normalized),
                    verdict=verdict,  # type: ignore[arg-type]
                    quran_verified=bool(candidate["quran_verified"]),
                    notes="quran_api_exact",
                )
            )
            continue

        present = [vmap[index] for vmap in verdict_maps if index in vmap]
        compliant = sum(1 for v in present if v.get("compliant") is True)
        authentic = sum(1 for v in present if v.get("authentic") is True)
        publish = sum(1 for v in present if v.get("verdict") == "publish")
        drop = sum(1 for v in present if v.get("verdict") == "drop")
        total = len(present)

        base = {
            "i": index,
            "text": candidate["text"],
            "type": candidate["type_slug"],
            "category": candidate["category_slug"],
            "notes": " | ".join(str(v.get("notes", "")) for v in present),
        }

        if total == 0 or compliant * 2 <= total or drop >= 2:
            dropped.append(base)
            continue

        text = _pick_text(str(candidate["text"]), present)
        category_slug = _resolve_taxonomy(candidate, present, "category_ok", "suggested_category")
        type_slug = _resolve_taxonomy(candidate, present, "type_ok", "suggested_type")
        normalized = normalize_arabic(text)

        if publish >= 2 and authentic >= 2 and compliant == total:
            verdict = "auto_publish"
        else:
            verdict = "human_review"
            review.append(base)

        verified.append(
            VerifiedEntry(
                text=text,
                type_slug=type_slug,
                category_slug=category_slug,
                source=str(candidate["source"]),
                normalized=normalized,
                text_hash=text_hash(normalized),
                verdict=verdict,  # type: ignore[arg-type]
                quran_verified=False,
                notes=base["notes"][:300],
            )
        )

    payload = [entry.model_dump() for entry in verified]
    _OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    auto = sum(1 for e in verified if e.verdict == "auto_publish")
    print(
        f"verified: {len(verified)} | auto_publish: {auto} | "
        f"human_review: {len(review)} | dropped: {len(dropped)}"
    )
    print(f"written: {_OUTPUT}")
    for label, bucket in (("HUMAN REVIEW", review), ("DROPPED", dropped)):
        if not bucket:
            continue
        print(f"\n=== {label} ===")
        for item in bucket:
            snippet = str(item["text"])[:55]
            note = str(item["notes"])[:110]
            print(f"  [{item['i']}] {item['type']}/{item['category']}: {snippet} -- {note}")


if __name__ == "__main__":
    main()

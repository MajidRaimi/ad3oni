import re

import httpx

from src.shared.arabic.normalize import normalize_arabic

_EDITION = "quran-simple"
_BASE = "https://api.alquran.cloud/v1/ayah"
_PAUSE_MARKS = {code: None for code in range(0x06D6, 0x06ED + 1)}
_WHITESPACE = re.compile(r"\s+")


def _clean(text: str) -> str:
    return _WHITESPACE.sub(" ", text.translate(_PAUSE_MARKS)).strip()


async def fetch_ayah(http: httpx.AsyncClient, surah: int, ayah: int) -> str:
    response = await http.get(f"{_BASE}/{surah}:{ayah}/{_EDITION}")
    response.raise_for_status()
    data = response.json()
    return _clean(str(data["data"]["text"]))


def _matching_windows(ayah_words: list[str], target: str) -> list[str]:
    target_norm = normalize_arabic(target)
    if not target_norm:
        return []
    norms = [normalize_arabic(word) for word in ayah_words]
    matches: list[str] = []
    total = len(ayah_words)
    for start in range(total):
        accumulated: list[str] = []
        for end in range(start, total):
            accumulated.append(norms[end])
            joined = " ".join(part for part in accumulated if part).strip()
            if joined == target_norm:
                matches.append(" ".join(ayah_words[start : end + 1]).strip())
                break
            if len(joined) > len(target_norm):
                break
    return matches


def verify_quranic(
    curated_text: str, dua_substring: str | None, ayah_text: str
) -> tuple[bool, str]:
    if dua_substring is None:
        if normalize_arabic(curated_text) == normalize_arabic(ayah_text):
            return True, ayah_text
        return False, curated_text
    windows = _matching_windows(ayah_text.split(), dua_substring)
    if len(windows) == 1:
        return True, windows[0]
    return False, curated_text

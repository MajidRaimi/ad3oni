import hashlib
import re

from src.shared.arabic.normalize import normalize_arabic

_TRANSLITERATION = {
    "ا": "a",
    "ب": "b",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "ح": "h",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "d",
    "ط": "t",
    "ظ": "z",
    "ع": "a",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ي": "y",
}

_SEPARATORS = re.compile(r"[^a-z0-9]+")


def slugify_arabic(name: str) -> str:
    normalized = normalize_arabic(name)
    transliterated = "".join(
        _TRANSLITERATION.get(char, " " if char.isspace() else "") for char in normalized
    )
    slug = _SEPARATORS.sub("-", transliterated.lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    return f"item-{digest}"

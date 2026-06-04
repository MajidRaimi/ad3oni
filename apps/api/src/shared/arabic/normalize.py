import re

_DIACRITIC_RANGES = (
    (0x064B, 0x0652),
    (0x06D6, 0x06ED),
)
_DIACRITIC_CHARS = (0x0670, 0x0640)

_TASHKIL_TABLE = {code: None for start, end in _DIACRITIC_RANGES for code in range(start, end + 1)}
_TASHKIL_TABLE.update({code: None for code in _DIACRITIC_CHARS})

_LETTER_FOLD = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ٱ": "ا",
    "ى": "ي",
    "ة": "ه",
    "ؤ": "و",
    "ئ": "ي",
    "ء": "",
}
_FOLD_TABLE = {ord(source): target or None for source, target in _LETTER_FOLD.items()}

_NON_ARABIC = re.compile(r"[^ء-ي\s]")
_WHITESPACE = re.compile(r"\s+")


def strip_tashkil(text: str) -> str:
    return text.translate(_TASHKIL_TABLE)


def fold_letters(text: str) -> str:
    return text.translate(_FOLD_TABLE)


def normalize_arabic(text: str) -> str:
    stripped = strip_tashkil(text)
    folded = fold_letters(stripped)
    letters_only = _NON_ARABIC.sub(" ", folded)
    return _WHITESPACE.sub(" ", letters_only).strip()

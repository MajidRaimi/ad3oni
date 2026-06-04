from src.shared.arabic.hashing import text_hash
from src.shared.arabic.normalize import normalize_arabic, strip_tashkil
from src.shared.arabic.slugify import slugify_arabic


def test_strip_tashkil_removes_harakat() -> None:
    assert strip_tashkil("اللَّهُمَّ") == "اللهم"


def test_normalize_folds_alef_and_maqsura() -> None:
    assert normalize_arabic("أسأل الهُدَى") == "اسال الهدي"


def test_normalize_collapses_punctuation_and_whitespace() -> None:
    assert normalize_arabic("اللهم،   ارحمني!") == "اللهم ارحمني"


def test_diacritized_and_bare_normalize_identically() -> None:
    diacritized = "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى"
    bare = "اللهم اني اسالك الهدى والتقى"
    assert normalize_arabic(diacritized) == normalize_arabic(bare)
    assert text_hash(normalize_arabic(diacritized)) == text_hash(normalize_arabic(bare))


def test_text_hash_is_stable_and_hex() -> None:
    digest = text_hash("اللهم ارحمني")
    assert digest == text_hash("اللهم ارحمني")
    assert len(digest) == 64


def test_slugify_produces_ascii_slug() -> None:
    assert slugify_arabic("الرزق والمال") == "alrzq-walmal"


def test_slugify_falls_back_when_no_letters() -> None:
    slug = slugify_arabic("123 !!!")
    assert slug.startswith("item-")

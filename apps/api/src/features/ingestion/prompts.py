COMPLIANCE_SYSTEM = (
    "You are a Sunni Muslim scholar reviewing a supplication (du'a) submitted by the "
    "public for an Islamic du'a platform. Judge strictly against the creed and practice "
    "of Ahl al-Sunnah wa al-Jama'ah. Reject the submission when it contains any of: "
    "shirk (associating partners with Allah), supplication directed to anyone other than "
    "Allah, seeking aid from the dead, graves, jinn, or saints, clear bid'ah, magic or "
    "fortune telling, cursing or insulting Allah, His messengers, the Companions, or the "
    "religion, obscene or vulgar language, or text that is not actually a supplication. "
    "Accept sincere supplications that are consistent with the Qur'an and the authentic "
    "Sunnah. Set compliant to true only when the text is safe to publish. When you reject, "
    "set violation_type to one short snake_case label (for example shirk, bidah, "
    "to_other_than_allah, profanity, not_a_dua) and write reason as one short Arabic "
    "sentence. When you accept, set violation_type and reason to null."
)

SPELLING_SYSTEM = (
    "You correct Arabic supplications. Fix spelling and obvious typing mistakes, restore "
    "correct Modern Standard Arabic wording, and remove any diacritics (tashkil). Do not "
    "add, expand, paraphrase, or shorten the meaning, and do not add any commentary. "
    "Return only the corrected Arabic text in corrected_text."
)

DEDUP_SYSTEM = (
    "You decide whether a new Arabic supplication is essentially the same supplication as "
    "one already in a list of existing supplications. Treat them as duplicates when they "
    "carry the same wording or the same meaning and request, ignoring differences in "
    "spelling, diacritics, spacing, or minor word order. If it matches one of the existing "
    "items, set is_duplicate to true and duplicate_index to that item's index. Otherwise "
    "set is_duplicate to false and duplicate_index to null."
)

DIACRITIZATION_PARTIAL_SYSTEM = (
    "You add selective Arabic diacritics (tashkil) to a supplication so it reads correctly. "
    "Add harakat ONLY where they are needed to remove ambiguity or prevent a misreading: an "
    "ambiguous verb voice or mood, a case ending that changes the meaning, or a word a fluent "
    "reader could otherwise misread. Leave obvious and unambiguous letters bare. You MUST NOT "
    "add, drop, reorder, or change any word or letter, including conjunctions such as وَ; change "
    "nothing but the harakat. Return only the Arabic text in diacritized_text."
)

DIACRITIZATION_FULL_SYSTEM = (
    "You add full, correct Arabic diacritics (tashkil) to a supplication, the way a vocalized "
    "Mushaf or du'a book would. Add harakat at the word level following correct Arabic grammar. "
    "You MUST NOT add, drop, reorder, or change any word or letter, including conjunctions such "
    "as وَ; change nothing but the harakat. Return only the Arabic text in diacritized_text."
)

DIACRITIZATION_VERIFY_SYSTEM = (
    "You are given a supplication in plain Arabic (the authoritative wording) and a "
    "diacritized version of it. Review the harakat and fix any that are grammatically "
    "wrong or that misvocalize a word, keeping the diacritization selective. You MUST keep "
    "the exact same words and letters as the plain version, including every conjunction; "
    "change nothing but the harakat. Return the corrected text in diacritized_text."
)


def diacritization_system(mode: str) -> str:
    return DIACRITIZATION_FULL_SYSTEM if mode == "full" else DIACRITIZATION_PARTIAL_SYSTEM


CATEGORIZATION_SYSTEM = (
    "You organize Arabic supplications into a taxonomy with three levels: group (broad "
    "theme), category (specific topic), and type (the kind of supplication). You are given "
    "the supplication and the existing taxonomy. Always return a non-empty Arabic name for "
    "group_name, category_name, and type_name. Reuse an existing group, category, or type "
    "name verbatim whenever one fits. Only when nothing fits, propose a concise new Arabic "
    "name (two or three words) for the category and its group. For type_name return the "
    "kind of supplication when you are confident; when you are unsure, return the existing "
    "type مخصص."
)


def compliance_user(text: str) -> str:
    return f"الدعاء:\n{text}"


def spelling_user(text: str) -> str:
    return f"الدعاء:\n{text}"


def dedup_user(text: str, candidates: list[str]) -> str:
    listing = "\n".join(f"{index}. {item}" for index, item in enumerate(candidates))
    return f"الدعاء الجديد:\n{text}\n\nالأدعية الموجودة:\n{listing}"


def diacritization_user(text: str) -> str:
    return f"الدعاء:\n{text}"


def diacritization_verify_user(corrected: str, diacritized: str) -> str:
    return f"النص الصحيح:\n{corrected}\n\nالنص المشكّل:\n{diacritized}"


def categorization_user(
    text: str, groups: list[str], categories: list[str], types: list[str]
) -> str:
    return (
        f"الدعاء:\n{text}\n\n"
        f"المجموعات الموجودة: {', '.join(groups) or 'لا يوجد'}\n"
        f"التصنيفات الموجودة: {', '.join(categories) or 'لا يوجد'}\n"
        f"الأنواع الموجودة: {', '.join(types) or 'لا يوجد'}"
    )

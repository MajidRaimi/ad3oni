_AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

_WEEKDAYS = {
    0: "الأحد",
    7: "الأحد",
    1: "الإثنين",
    2: "الثلاثاء",
    3: "الأربعاء",
    4: "الخميس",
    5: "الجمعة",
    6: "السبت",
}

_TIMEZONE_CITIES = {
    "Asia/Riyadh": "مكة",
    "Asia/Dubai": "دبي",
    "Asia/Qatar": "الدوحة",
    "Asia/Kuwait": "الكويت",
    "Asia/Bahrain": "المنامة",
    "Asia/Muscat": "مسقط",
    "Asia/Baghdad": "بغداد",
    "Asia/Amman": "عمّان",
    "Asia/Beirut": "بيروت",
    "Asia/Damascus": "دمشق",
    "Asia/Jerusalem": "القدس",
    "Asia/Aden": "عدن",
    "Africa/Cairo": "القاهرة",
    "Africa/Khartoum": "الخرطوم",
    "Africa/Casablanca": "الدار البيضاء",
    "Africa/Tunis": "تونس",
    "Africa/Algiers": "الجزائر",
    "Africa/Tripoli": "طرابلس",
    "Africa/Nouakchott": "نواكشوط",
    "Africa/Mogadishu": "مقديشو",
}


def _ar(number: int) -> str:
    return str(number).translate(_AR_DIGITS)


def _ar2(number: int) -> str:
    return f"{number:02d}".translate(_AR_DIGITS)


def _clock(minute: int, hour: int) -> str:
    if minute == 0 and hour == 0:
        return "منتصف الليل"
    if minute == 0 and hour == 12:
        return "ظهرًا"
    period = "صباحًا" if hour < 12 else ("ظهرًا" if hour == 12 else "مساءً")
    hour12 = hour % 12 or 12
    clock = _ar(hour12) if minute == 0 else f"{_ar(hour12)}:{_ar2(minute)}"
    return f"{clock} {period}"


def _time_phrase(minute: int, hours: list[int]) -> str:
    if len(hours) == 1:
        clock = _clock(minute, hours[0])
        return clock if clock in ("منتصف الليل", "ظهرًا") else f"الساعة {clock}"
    return "الساعة " + " و".join(_clock(minute, hour) for hour in hours)


def describe_cron_ar(cron: str) -> str | None:
    parts = cron.split()
    if len(parts) != 5:
        return None
    minute_field, hour_field, dom_field, month_field, dow_field = parts
    if month_field != "*" or not minute_field.isdigit():
        return None

    minute = int(minute_field)
    if minute > 59:
        return None
    try:
        hours = [int(value) for value in hour_field.split(",")]
    except ValueError:
        return None
    if any(hour > 23 for hour in hours):
        return None

    time_phrase = _time_phrase(minute, hours)

    if dom_field == "*" and dow_field == "*":
        day_phrase = "كل يوم"
    elif dom_field == "*":
        try:
            days = [int(value) for value in dow_field.split(",")]
        except ValueError:
            return None
        names = [_WEEKDAYS.get(day) for day in days]
        if any(name is None for name in names):
            return None
        if len(names) == 1 and names[0] is not None:
            day_phrase = f"كل {names[0].removeprefix('ال')}"
        else:
            day_phrase = "أيام " + " و".join(name for name in names if name)
    elif dow_field == "*" and dom_field.isdigit():
        day_phrase = f"يوم {_ar(int(dom_field))} من كل شهر"
    else:
        return None

    return f"{day_phrase} {time_phrase}"


def timezone_label_ar(timezone: str) -> str:
    city = _TIMEZONE_CITIES.get(timezone)
    if city:
        return f"بتوقيت {city}"
    tail = timezone.split("/")[-1].replace("_", " ")
    return f"بتوقيت {tail}"


def content_label_ar(content_type: str, category_display: str | None) -> str:
    if content_type == "daily":
        return "دعاء اليوم"
    if content_type == "category" and category_display:
        return f"دعاء من تصنيف {category_display}"
    return "دعاء عشوائي"

def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def quote(value: str) -> str:
    return f'"{escape(value)}"'


def combine(*clauses: str | None) -> str:
    return " && ".join(clause for clause in clauses if clause)

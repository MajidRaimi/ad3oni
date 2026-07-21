X_SESSION = "ad3oni:x:session"
X_LAST_POST = "ad3oni:x:last_post"

MAX_POST_LENGTH = 280


def posted_key(day: str) -> str:
    return f"ad3oni:x:posted:{day}"

X_SESSION = "ad3oni:x:session"
X_LAST_POST = "ad3oni:x:last_post"

HOME_URL = "https://x.com/home"
COMPOSE_URL = "https://x.com/compose/post"
PROFILE_URL = "https://x.com/{handle}"

EDITOR = '[data-testid="tweetTextarea_0"]'
SUBMIT = '[data-testid="tweetButton"]'
PROFILE_LINK = '[data-testid="AppTabBar_Profile_Link"]'
TWEET_TEXT = '[data-testid="tweetText"]'

MAX_POST_LENGTH = 280

_USER_DATA_DIR = "/tmp/ad3oni-x-profile"

# Mecca-time [start_hour, end_hour) windows. Each day one random minute inside
# each window is chosen, so the three daily posts are spread and non-uniform.
POST_WINDOWS: tuple[tuple[int, int], ...] = ((5, 9), (12, 16), (18, 22))
GRACE_MINUTES = 9
SLOT_TTL_SECONDS = 60 * 60 * 48
PICK_TRIES = 6


def plan_key(day: str) -> str:
    return f"ad3oni:x:plan:{day}"


def slot_posted_key(day: str, slot: int) -> str:
    return f"ad3oni:x:posted:{day}:{slot}"


def posted_prayers_key(day: str) -> str:
    return f"ad3oni:x:posted_prayers:{day}"

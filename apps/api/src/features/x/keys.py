X_SESSION = "ad3oni:x:session"
X_LAST_POST = "ad3oni:x:last_post"

HOME_URL = "https://x.com/home"
COMPOSE_URL = "https://x.com/compose/post"
PROFILE_URL = "https://x.com/{handle}"

EDITOR = '[data-testid="tweetTextarea_0"]'
SUBMIT = '[data-testid="tweetButton"]'
ACCOUNT_SWITCHER = '[data-testid="SideNav_AccountSwitcher_Button"]'
TWEET_TEXT = '[data-testid="tweetText"]'

MAX_POST_LENGTH = 280

_USER_DATA_DIR = "/tmp/ad3oni-x-profile"
_UA_PROBE_DIR = "/tmp/ad3oni-x-ua-probe"


def posted_key(day: str) -> str:
    return f"ad3oni:x:posted:{day}"

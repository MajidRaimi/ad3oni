import json
import os
from pathlib import Path

_OUTPUT = Path(__file__).resolve().parent.parent / "x-session.json"

_INSTRUCTIONS = """
Build an X session from the browser you are already logged into.

Nothing here talks to X, so it cannot trigger a login restriction.

  1. Open https://x.com in your normal browser, signed in as the posting account.
  2. Open DevTools (cmd+alt+i) -> Application -> Storage -> Cookies -> https://x.com
  3. Copy the values of these two cookies:

       auth_token
       ct0

  4. Run:

       X_AUTH_TOKEN=... X_CT0=... uv run python -m scripts.build_x_session

Treat both values as passwords. Anyone holding them is logged in as you.
"""


def main() -> None:
    auth_token = os.environ.get("X_AUTH_TOKEN", "").strip()
    ct0 = os.environ.get("X_CT0", "").strip()

    if not auth_token or not ct0:
        print(_INSTRUCTIONS)
        raise SystemExit(1)

    cookies = {"auth_token": auth_token, "ct0": ct0}
    _OUTPUT.write_text(json.dumps(cookies), encoding="utf-8")

    print(f"wrote {_OUTPUT}")
    print("\nNext:")
    print("  1. Verify it works:  uv run python -m scripts.verify_x_session")
    print("  2. Put the contents in X_SESSION_STATE, sync to Infisical")
    print(f"  3. rm {_OUTPUT}")


if __name__ == "__main__":
    main()

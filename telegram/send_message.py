import os
import sys
from pathlib import Path

import requests
try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None


def main() -> int:
    # Load telegram/.env (same directory) if present.
    if load_dotenv is not None:
        dotenv_path = Path(__file__).resolve().with_name(".env")
        load_dotenv(dotenv_path=dotenv_path)

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    parse_mode = os.getenv("TELEGRAM_PARSE_MODE", "HTML")

    if not bot_token:
        print("Missing TELEGRAM_BOT_TOKEN. Check telegram/.env.")
        return 1
    if not chat_id:
        print("Missing TELEGRAM_CHAT_ID. Check telegram/.env.")
        return 1

    text = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not text:
        text = "Telegram test message (from Python requests)."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    # Don't inherit system proxy settings (HTTP_PROXY/HTTPS_PROXY/ALL_PROXY).
    session = requests.Session()
    session.trust_env = False

    try:
        resp = session.post(url, json=payload, timeout=20)
    except Exception as e:
        print(f"Request failed: {e}")
        return 1

    if 200 <= resp.status_code < 300:
        print("Message sent.")
        return 0

    print(f"Send failed: {resp.status_code}")
    try:
        print(resp.text)
    except Exception:
        pass
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

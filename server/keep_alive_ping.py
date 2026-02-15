#!/usr/bin/env python3
"""Keep-alive ping script for Render cron jobs.

Pings the configured health endpoint with retries and fails non-2xx responses.
"""

from __future__ import annotations

import os
import sys
import time
from urllib import error, request

TARGET_URL = os.getenv("PING_TARGET_URL", "https://findyourcity.onrender.com/api/health")
TIMEOUT_SECONDS = int(os.getenv("PING_TIMEOUT_SECONDS", "15"))
RETRIES = int(os.getenv("PING_RETRIES", "3"))
RETRY_DELAY_SECONDS = int(os.getenv("PING_RETRY_DELAY_SECONDS", "3"))


def ping_once(url: str, timeout: int) -> tuple[bool, str]:
    req = request.Request(
        url,
        headers={"User-Agent": "FindYourCityKeepAlive/1.0 (+render-cron)"},
    )

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            if 200 <= status < 300:
                return True, f"HTTP {status}"
            return False, f"HTTP {status}"
    except error.HTTPError as exc:
        return False, f"HTTPError {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    print(f"[keep-alive] target={TARGET_URL} retries={RETRIES} timeout={TIMEOUT_SECONDS}s")

    for attempt in range(1, RETRIES + 1):
        ok, detail = ping_once(TARGET_URL, TIMEOUT_SECONDS)
        if ok:
            print(f"[keep-alive] success attempt={attempt} detail={detail}")
            return 0

        print(f"[keep-alive] failed attempt={attempt} detail={detail}")
        if attempt < RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    print("[keep-alive] giving up after retries")
    return 1


if __name__ == "__main__":
    sys.exit(main())

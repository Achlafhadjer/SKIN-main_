"""Simple E2E smoke test for the running Docker stack.

Usage:
    python scripts/smoke_test_stack.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request


def get_json(url: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace")
            if response.status != 200:
                return False, f"{url} -> HTTP {response.status}"
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {"raw": body[:200]}
            return True, f"{url} -> OK {data}"
    except urllib.error.URLError as exc:
        return False, f"{url} -> ERROR {exc}"


def main() -> int:
    checks = [
        "http://localhost/auth/health",
        "http://localhost/api/v1/health",
        "http://localhost/ml/api/health",
        "http://localhost:8500/v1/status/leader",
        "http://localhost:15672/api/overview",
    ]

    failed = False
    for url in checks:
        ok, msg = get_json(url)
        print(msg)
        failed = failed or (not ok)

    if failed:
        print("\nSmoke test: FAILED")
        return 1
    print("\nSmoke test: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

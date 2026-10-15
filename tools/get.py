"""CLI helper: get.py

Usage:
  python get.py api ongleo022-tech <1|2|3>

Behavior:
- If a local API server is running at http://127.0.0.1:8000, this script will try
  to fetch the endpoint /api/ongleo022-tech/<id> and print the JSON response.
- Otherwise it prints the profile JSON locally.

Profiles:
  1 -> 2GB profile (depth 16)
  2 -> 4GB profile (depth 18)
  3 -> 8GB profile (depth 20)
"""

from __future__ import annotations

import sys
import json
import urllib.request
import urllib.error
from typing import Dict

PROFILES: Dict[str, Dict] = {
    "1": {
        "profile": "2GB",
        "depth": 16,
        "threads": 1,
        "transposition_table_mb": 24,
        "max_time_s": 4.0,
        "eval_sensitivity": 2.0,
    },
    "2": {
        "profile": "4GB",
        "depth": 18,
        "threads": 1,
        "transposition_table_mb": 64,
        "max_time_s": 5.0,
        "eval_sensitivity": 2.0,
    },
    "3": {
        "profile": "8GB",
        "depth": 20,
        "threads": 2,
        "transposition_table_mb": 256,
        "max_time_s": 10.0,
        "eval_sensitivity": 2.0,
    },
}

API_BASE = "http://127.0.0.1:8000"


def print_usage():
    print("Usage: python get.py api ongleo022-tech <1|2|3>")


def fetch_remote(profile_id: str) -> Dict:
    url = f"{API_BASE}/api/ongleo022-tech/{profile_id}"
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.URLError:
        raise


def main(argv):
    if len(argv) < 4:
        print_usage()
        return 2

    cmd, resource, owner, profile_id = argv[1], argv[2], argv[3], (argv[4] if len(argv) > 4 else None)

    # support both "get.py api ongleo022-tech 1" and "get.py api ongleo022-tech 1 extra"
    # If user passed only three args, shift
    if profile_id is None:
        # argv[3] is profile in this variant
        profile_id = argv[3]
        resource = argv[2]
        owner = argv[1]
        # But we require the pattern: api ongleo022-tech <id>
        # fallback to simple check below

    # Normalize expected pattern: get.py api ongleo022-tech <id>
    # We'll accept calls like: get.py api ongleo022-tech 1
    if cmd != "get" and cmd != "python" and cmd != "./get.py":
        # user may call with python get.py ... so ignore
        pass

    if len(argv) >= 4 and argv[1] == "api" and argv[2] == "ongleo022-tech":
        pid = argv[3]
    elif len(argv) >= 5 and argv[1] == "get" and argv[2] == "api" and argv[3] == "ongleo022-tech":
        pid = argv[4]
    else:
        # try to be permissive: accept last argument as profile id
        pid = argv[-1]

    if pid not in PROFILES:
        print("Profile must be 1, 2 or 3. Example: get.py api ongleo022-tech 1")
        return 2

    # Try remote first
    try:
        data = fetch_remote(pid)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0
    except Exception:
        # Remote not available — print local profile
        profile = PROFILES[pid].copy()
        profile["source"] = "local"
        print(json.dumps(profile, indent=2, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env bash
# Run the arena tournament (Unix)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR/.."
cd "$REPO_ROOT"
python3 -m pip install -r requirements.txt
python3 tools/arena.py --games 50 --k 16 "$@"

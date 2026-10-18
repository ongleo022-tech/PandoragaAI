"""Pandoraga profile wrapper for 2GB devices.

This profile is intentionally a thin wrapper around the shared engine core.
It only configures the low-memory parameters and exposes a CLI demo.
"""

from __future__ import annotations

import sys

from pandoraga.core_engine import create_engine_for_profile, Board


PROFILE_NAME = "2GB"


def main() -> None:
    engine = create_engine_for_profile("2gb", ram_gb=2.0)
    board = Board.initial_board()
    print("Pandoraga Omega - 2GB profile")
    print(engine.search(board, side_to_move="w").message)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"--help", "-h"}:
        print("Usage: python Pandoraga_2GB.py")
    else:
        main()

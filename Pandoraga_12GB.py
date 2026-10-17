"""Pandoraga Omega - 12GB profile (ported & improved from Pandoraga_8GB.py).

This file preserves the original UI/CLI structure from the 8GB profile while
increasing memory/threads/search parameters for machines with ~12 GB RAM.
It also keeps the interactive demo and the same user-facing messages.
"""

from __future__ import annotations

import math
import random
import time
import sys

try:
    import psutil
except Exception:
    psutil = None

# Attempt to keep the same structure and names as the 8GB profile but tuned for 12GB
PROFILE_LABEL = "12GB"

# Tuned constants (higher than 8GB profile)
PROFILE_MAX_DEPTH = 24
PROFILE_TT_MB = 512
PROFILE_THREADS = 4
PROFILE_EVAL_SENSITIVITY = 2.5
PROFILE_MAX_TIME = 15.0
PROFILE_MIN_TIME = 1.0

# Fallbacks and thresholds
DEFAULT_DEPTH = PROFILE_MAX_DEPTH
DEFAULT_TT_MB = PROFILE_TT_MB
DEFAULT_THREADS = PROFILE_THREADS


def detect_ram_gb() -> float:
    """Detect total system RAM in GB; fallback to /proc/meminfo or conservative default."""
    try:
        if psutil is None:
            raise Exception("psutil not available")
        mem = psutil.virtual_memory()
        return round(mem.total / (1024 ** 3), 1)
    except Exception:
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        parts = line.split()
                        kb = int(parts[1])
                        return round(kb / 1024.0 / 1024.0, 1)
        except Exception:
            pass
    return 4.0


class EngineState:
    def __init__(self) -> None:
        self.depth = DEFAULT_DEPTH
        self.tt_mb = DEFAULT_TT_MB
        self.threads = DEFAULT_THREADS
        self.eval_sensitivity = PROFILE_EVAL_SENSITIVITY
        self.max_time = PROFILE_MAX_TIME
        self.min_time = PROFILE_MIN_TIME


def apply_profile_scaling(state: EngineState) -> EngineState:
    """Scale the 12GB profile down when the host has less RAM, preserving safe minima."""
    ram = detect_ram_gb()

    state.depth = PROFILE_MAX_DEPTH
    state.tt_mb = PROFILE_TT_MB
    state.threads = PROFILE_THREADS
    state.max_time = PROFILE_MAX_TIME
    state.min_time = PROFILE_MIN_TIME
    state.eval_sensitivity = PROFILE_EVAL_SENSITIVITY

    if ram < 12.0:
        ratio = max(0.5, ram / 12.0)
        # Transposition table scales linearly but with a safe floor
        state.tt_mb = max(64, int(state.tt_mb * ratio))
        # Depth scales sublinearly to avoid extreme drops
        state.depth = max(6, int(state.depth * (0.8 * ratio + 0.2)))
        # Threads scale but keep at least 1
        state.threads = max(1, int(max(1, round(state.threads * (0.5 + 0.5 * ratio)))))
        # Time per move scales conservatively
        state.max_time = max(0.5, state.max_time * (0.6 + 0.4 * ratio))
        state.min_time = max(0.1, state.min_time * (0.6 + 0.4 * ratio))
        state.eval_sensitivity = max(0.8, state.eval_sensitivity * (0.8 + 0.2 * ratio))

    return state


def auto_tune_for_board(state: EngineState, board_stats: dict) -> EngineState:
    """Small heuristic tuner based on board statistics (material, complexity).

    board_stats keys (optional):
      - material_balance (int)
      - complexity (float)
    """
    material = board_stats.get("material_balance", 0)
    if abs(material) > 250:
        state.depth = max(4, state.depth - 2)

    complexity = board_stats.get("complexity", 1.0)
    if complexity > 1.7:
        state.max_time = min(60.0, state.max_time * 1.25)

    return state


def build_state() -> EngineState:
    s = EngineState()
    s = apply_profile_scaling(s)
    return s


# --- CLI / demo UI preserved from 8GB profile ---
def print_profile_summary(state: EngineState) -> None:
    print("\n" + "=" * 60)
    print(f"Pandoraga Omega - {PROFILE_LABEL} profile")
    print("=" * 60)
    print(f"Detected RAM: {detect_ram_gb()} GB")
    print(f"Search depth target: {state.depth}")
    print(f"TT size (MB): {state.tt_mb}")
    print(f"Threads: {state.threads}")
    print(f"Eval sensitivity: {state.eval_sensitivity}")
    print(f"Max time/move: {state.max_time}")
    print(f"Min time/move: {state.min_time}")
    print("=" * 60)


def demo_run(state: EngineState, moves: int = 5) -> None:
    """A small deterministic-ish demo to show how parameters affect decision time.
    Not a real search — a placeholder to exercise timings and state adjustments.
    """
    random.seed(0)
    for i in range(moves):
        board_stats = {"material_balance": random.randint(-300, 300), "complexity": random.uniform(0.5, 2.5)}
        s = auto_tune_for_board(state, board_stats)
        think_time = min( max(0.01, s.max_time * (0.1 + 0.02 * (s.depth / PROFILE_MAX_DEPTH))),  s.max_time )
        print(f"Move {i+1}: material={board_stats['material_balance']}, complexity={board_stats['complexity']:.2f} -> think_time={think_time:.2f}s (depth={s.depth})")
        time.sleep(0.01)


def main_cli() -> None:
    state = build_state()
    print_profile_summary(state)
    print("Options:\n 1) Run demo moves\n 2) Show profile\n 3) Exit")
    try:
        choice = input("Choice: ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if choice == "1":
        demo_run(state, moves=8)
    elif choice == "2":
        print_profile_summary(state)
    else:
        print("Goodbye")


if __name__ == "__main__":
    # preserve original 8GB behavior: allow running as demo launcher
    try:
        main_cli()
    except Exception as exc:
        print("Error running Pandoraga_12GB demo:", exc)
        raise

"""Pandoraga Omega - 12GB-optimized MAX profile.

This profile is tuned for machines with up to ~12 GB of RAM and favors
maximum practical playing strength while staying within the memory budget.

Key choices for 12GB devices:
- Search depth target: 24 (higher depth for stronger play)
- Transposition table (TT) size: 512 MB
- Threads: 4 (if available)
- Evaluation sensitivity: 2.5 (slightly more sensitive)
- Max time per move: 15.0s (auto-managed)
- Min time per move: 1.0s

This file is based on the Pandoraga_8GB.py profile and adjusted for
larger available memory / CPU resources.
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

# PROFILE CONSTANTS for 12GB
PROFILE_12GB_MAX_DEPTH = 24
PROFILE_12GB_TT_MB = 512
PROFILE_12GB_THREADS = 4
PROFILE_12GB_EVAL_SENSITIVITY = 2.5
PROFILE_12GB_MAX_TIME = 15.0
PROFILE_12GB_MIN_TIME = 1.0


def detect_ram_gb() -> float:
    """Attempt to detect total system RAM in GB; fall back to heuristic if not available."""
    try:
        if psutil is None:
            raise Exception("psutil not available")
        mem = psutil.virtual_memory()
        return round(mem.total / (1024 ** 3), 1)
    except Exception:
        # best-effort fallback: try /proc/meminfo on Linux
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        parts = line.split()
                        # kB -> GB
                        kb = int(parts[1])
                        return round(kb / 1024.0 / 1024.0, 1)
        except Exception:
            pass
    # default conservative value
    return 4.0


class EngineState:
    def __init__(self):
        self.current_depth = PROFILE_12GB_MAX_DEPTH
        self.current_tt_mb = PROFILE_12GB_TT_MB
        self.threads = PROFILE_12GB_THREADS
        self.eval_sensitivity = PROFILE_12GB_EVAL_SENSITIVITY
        self.max_time = PROFILE_12GB_MAX_TIME
        self.min_time = PROFILE_12GB_MIN_TIME
        self.transposition_table_mb = PROFILE_12GB_TT_MB


def apply_device_profile(state: EngineState) -> EngineState:
    """Apply device-dependent settings; if the host has less RAM than 12GB,
    the profile will scale down to stay safe."""
    ram = detect_ram_gb()

    # start from defaults above, then scale down if needed
    state.current_depth = PROFILE_12GB_MAX_DEPTH
    state.transposition_table_mb = PROFILE_12GB_TT_MB
    state.threads = PROFILE_12GB_THREADS
    state.eval_sensitivity = PROFILE_12GB_EVAL_SENSITIVITY
    state.max_time = PROFILE_12GB_MAX_TIME
    state.min_time = PROFILE_12GB_MIN_TIME

    if ram < 12.0:
        # scale down proportionally to available RAM (linear scaling), but keep safe minima
        ratio = max(0.5, ram / 12.0)
        state.transposition_table_mb = max(64, int(state.transposition_table_mb * ratio))
        state.current_depth = max(6, int(state.current_depth * (0.8 * ratio + 0.2)))
        state.threads = max(1, int(state.threads * (0.5 + 0.5 * ratio)))
        state.max_time = max(0.5, state.max_time * (0.6 + 0.4 * ratio))
        state.min_time = max(0.1, state.min_time * (0.6 + 0.4 * ratio))
        state.eval_sensitivity = max(0.8, state.eval_sensitivity * (0.8 + 0.2 * ratio))

    return state


def auto_adjust_parameters(state: EngineState, board_stats: dict) -> EngineState:
    """A simple example of auto-adjusting search allocation using board statistics.
    board_stats can include keys like 'material_balance', 'phase', etc. This is
    intentionally small and conservative.
    """
    # Example: if material imbalance is large, reduce search depth slightly
    material = board_stats.get("material_balance", 0)
    if abs(material) > 200:
        state.current_depth = max(4, state.current_depth - 2)
    # If complex middlegame (many pieces), allow a bit more time
    complexity = board_stats.get("complexity", 1.0)
    if complexity > 1.5:
        state.max_time = min(60.0, state.max_time * 1.25)
    return state


def build_default_state() -> EngineState:
    state = EngineState()
    state = apply_device_profile(state)
    return state


if __name__ == "__main__":
    # quick demo of profile application
    state = build_default_state()
    print("Pandoraga - 12GB optimized profile")
    print(f"Detected RAM: {detect_ram_gb()} GB")
    print(f"Depth: {state.current_depth}")
    print(f"TT size (MB): {state.transposition_table_mb}")
    print(f"Threads: {state.threads}")
    print(f"Eval sensitivity: {state.eval_sensitivity}")
    print(f"Max time/move: {state.max_time}")
    print(f"Min time/move: {state.min_time}")

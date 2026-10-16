# -*- coding: utf-8 -*-
"""
elo_tournament.py

Simulate 1v1 matches between the three Pandoraga builds (2GB, 4GB, 8GB)
and compute resulting Elo changes. The script runs three matchups in sequence:

  1) 2GB vs 4GB
  2) 4GB vs 8GB
  3) 2GB vs 8GB

By default each matchup runs N games (default 100). Outcomes are simulated
probabilistically from an estimated Elo derived from each engine's profile
(depth + search_efficiency). If the real engine modules are importable, the
script will instantiate them and derive dynamic metrics; otherwise it falls
back to static profile values.

Usage:
  python tools/elo_tournament.py [--games N] [--seed S] [--k K]

Examples:
  python tools/elo_tournament.py --games 200

Note: This is a simulator (the current Pandoraga builds are lightweight
placeholders). The script models game outcomes using Elo probabilities and
reports final Elo and match statistics.
"""

from __future__ import annotations

import importlib
import random
import argparse
from dataclasses import dataclass
from typing import Tuple, Optional

# Default static profiles (fallback if modules/classes are not importable)
STATIC_PROFILES = {
    "2": {"name": "2GB", "depth": 16, "tt_mb": 24, "threads": 1, "max_time_s": 4.0, "search_eff": 0.80},
    "4": {"name": "4GB", "depth": 18, "tt_mb": 64, "threads": 1, "max_time_s": 5.0, "search_eff": 0.85},
    "8": {"name": "8GB", "depth": 20, "tt_mb": 256, "threads": 2, "max_time_s": 10.0, "search_eff": 0.90},
}

# Map profile ids to module names and class names used in the repo
MODULE_MAP = {
    "2": ("Pandoraga_2GB", "Pandoraga2GB"),
    "4": ("Pandoraga", "Pandoraga4GB"),
    "8": ("Pandoraga_8GB", "Pandoraga8GB"),
}

@dataclass
class EngineProfile:
    id: str
    name: str
    depth: int
    tt_mb: int
    threads: int
    max_time_s: float
    search_eff: float
    est_elo: float


def try_load_dynamic_profile(pid: str) -> Optional[EngineProfile]:
    """Try to import the engine module and instantiate it to read dynamic metrics.
    Returns None on failure so the caller will use STATIC_PROFILES.
    """
    mapping = MODULE_MAP.get(pid)
    if not mapping:
        return None
    modname, clsname = mapping
    try:
        mod = importlib.import_module(modname)
        cls = getattr(mod, clsname)
        # instantiate with a small available_time to avoid long sleeps
        engine = cls(available_time=1.0)
        # Some engine classes expose these attributes
        depth = getattr(engine, "current_depth", getattr(engine, "depth", None)) or getattr(engine, "current_depth", 0)
        tt_mb = getattr(engine, "transposition_table_mb", None) or getattr(engine, "tt_mb", STATIC_PROFILES[pid]["tt_mb"])
        threads = getattr(engine, "threads", STATIC_PROFILES[pid]["threads"])
        max_time_s = getattr(engine, "current_time", getattr(engine, "max_time_s", STATIC_PROFILES[pid]["max_time_s"]))
        search_eff = getattr(engine, "search_efficiency", STATIC_PROFILES[pid]["search_eff"]) or STATIC_PROFILES[pid]["search_eff"]
        # Derive estimated Elo from depth + search_efficiency
        est_elo = derive_elo_from(depth, search_eff)
        return EngineProfile(pid, STATIC_PROFILES[pid]["name"], int(depth), int(tt_mb), int(threads), float(max_time_s), float(search_eff), float(est_elo))
    except Exception:
        return None


def derive_elo_from(depth: int, search_eff: float) -> float:
    """Heuristic mapping from (depth, search_efficiency) → estimated Elo.
    This is a simple linear heuristic chosen for simulation purposes.
    """
    # Base Elo by depth: 16->1600, 18->1900, 20->2200 (approx)
    base = 100 * depth
    # Adjust base to map 16->1600, 18->1800 etc. We'll subtract a small offset
    # to place values in a reasonable bracket.
    base = depth * 100
    # search_eff adjustment: center around 0.8
    adj = (search_eff - 0.8) * 500.0
    elo = base + adj
    # Clamp to reasonable range
    if elo < 1000:
        elo = 1000.0
    if elo > 3000:
        elo = 3000.0
    return elo


def get_profile(pid: str) -> EngineProfile:
    dyn = try_load_dynamic_profile(pid)
    if dyn:
        return dyn
    s = STATIC_PROFILES.get(pid)
    if not s:
        raise ValueError(f"Unknown profile id {pid}")
    elo = derive_elo_from(s["depth"], s["search_eff"])
    return EngineProfile(pid, s["name"], s["depth"], s["tt_mb"], s["threads"], s["max_time_s"], s["search_eff"], elo)


def elo_expected(r_a: float, r_b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((r_b - r_a) / 400.0))


def simulate_games(profile_a: EngineProfile, profile_b: EngineProfile, games: int = 100, draw_prob: float = 0.08, kfactor: float = 16, verbose: bool = False) -> Tuple[float, float, dict]:
    """Simulate `games` games between A and B. Return final Elo for A,B and stats."""
    ra = profile_a.est_elo
    rb = profile_b.est_elo
    stats = {"a_wins": 0, "b_wins": 0, "draws": 0}
    for i in range(games):
        p_a = elo_expected(ra, rb)
        # account for draw probability: split remaining mass
        r = random.random()
        if r < draw_prob:
            score_a = 0.5
            stats["draws"] += 1
        else:
            # effective win probabilites scaled to (1-draw_prob)
            win_threshold = p_a
            if random.random() < win_threshold:
                score_a = 1.0
                stats["a_wins"] += 1
            else:
                score_a = 0.0
                stats["b_wins"] += 1
        # Update Elo ratings iteratively (simple Elo update)
        expected_a = elo_expected(ra, rb)
        expected_b = 1.0 - expected_a
        ra = ra + kfactor * (score_a - expected_a)
        rb = rb + kfactor * ((1.0 - score_a) - expected_b)
        if verbose and (i + 1) % 50 == 0:
            print(f"After {i+1} games: RA={ra:.1f} RB={rb:.1f}  (wins A:{stats['a_wins']} B:{stats['b_wins']} D:{stats['draws']})")
    return ra, rb, stats


def run_sequence(games: int, seed: Optional[int], k: float):
    if seed is not None:
        random.seed(seed)
    # Initial profiles
    p2 = get_profile("2")
    p4 = get_profile("4")
    p8 = get_profile("8")

    print("Initial estimated Elos:")
    print(f"  2GB ({p2.name}): {p2.est_elo:.1f}")
    print(f"  4GB ({p4.name}): {p4.est_elo:.1f}")
    print(f"  8GB ({p8.name}): {p8.est_elo:.1f}")
    print()

    results = {}

    # 1) 2GB vs 4GB
    print(f"Running {games} games: 2GB vs 4GB...")
    ra, rb, stats = simulate_games(p2, p4, games=games, draw_prob=0.08, kfactor=k)
    print(f"Results 2GB vs 4GB -> final Elo: 2GB={ra:.1f}, 4GB={rb:.1f}  (A wins:{stats['a_wins']} B wins:{stats['b_wins']} draws:{stats['draws']})")
    results['2_vs_4'] = {'2gb': ra, '4gb': rb, 'stats': stats}

    # Update local profiles with new Elos for next match
    p2.est_elo = ra
    p4.est_elo = rb

    # 2) 4GB vs 8GB
    print(f"\nRunning {games} games: 4GB vs 8GB...")
    ra, rb, stats = simulate_games(p4, p8, games=games, draw_prob=0.08, kfactor=k)
    print(f"Results 4GB vs 8GB -> final Elo: 4GB={ra:.1f}, 8GB={rb:.1f}  (A wins:{stats['a_wins']} B wins:{stats['b_wins']} draws:{stats['draws']})")
    results['4_vs_8'] = {'4gb': ra, '8gb': rb, 'stats': stats}

    # Update
    p4.est_elo = ra
    p8.est_elo = rb

    # 3) 2GB vs 8GB (use updated Elos from previous matches)
    print(f"\nRunning {games} games: 2GB vs 8GB...")
    ra, rb, stats = simulate_games(p2, p8, games=games, draw_prob=0.08, kfactor=k)
    print(f"Results 2GB vs 8GB -> final Elo: 2GB={ra:.1f}, 8GB={rb:.1f}  (A wins:{stats['a_wins']} B wins:{stats['b_wins']} draws:{stats['draws']})")
    results['2_vs_8'] = {'2gb': ra, '8gb': rb, 'stats': stats}

    print("\nFinal estimated Elos after sequence:")
    print(f"  2GB: {p2.est_elo:.1f}")
    print(f"  4GB: {p4.est_elo:.1f}")
    print(f"  8GB: {p8.est_elo:.1f}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Simulate Elo tournament between 2/4/8GB engine builds")
    parser.add_argument("--games", type=int, default=100, help="Number of games per matchup (default 100)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--k", type=float, default=16.0, help="Elo K-factor per game (default 16)")
    args = parser.parse_args()

    run_sequence(games=args.games, seed=args.seed, k=args.k)


if __name__ == "__main__":
    main()

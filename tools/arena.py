# -*- coding: utf-8 -*-
"""
arena.py

Real-ish 1v1 simulation arena for the three Pandoraga builds.

This script creates actual chess games using the python-chess library and a
very lightweight "engine policy" built from the evaluation function already
present in the three builds. It does NOT implement a full minimax search at
16/18/20 depth, but it does give a real game engine environment, real legal
moves, and a deterministic evaluation-based battle between the three build
profiles.

Features:
- 2GB vs 4GB
- 4GB vs 8GB
- 2GB vs 8GB
- real valid chess moves via python-chess
- Elo updates after each finished game
- optional K-factor and random seed
- configurable number of games per matchup
- automatically swaps colors to reduce first-player bias

Usage:
  python arena.py --games 20 --k 16 --seed 7

Install:
  pip install python-chess
"""

from __future__ import annotations

import argparse
import importlib
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import chess


STATIC_PROFILES = {
    "2": {"name": "2GB", "depth": 16, "tt_mb": 24, "threads": 1, "max_time_s": 4.0, "search_eff": 0.80},
    "4": {"name": "4GB", "depth": 18, "tt_mb": 64, "threads": 1, "max_time_s": 5.0, "search_eff": 0.85},
    "8": {"name": "8GB", "depth": 20, "tt_mb": 256, "threads": 2, "max_time_s": 10.0, "search_eff": 0.90},
}

ENGINE_MAP = {
    "2": ("Pandoraga_2GB", "Pandoraga2GB"),
    "4": ("Pandoraga", "Pandoraga4GB"),
    "8": ("Pandoraga_8GB", "Pandoraga8GB"),
}


def derive_elo_from(depth: int, search_eff: float) -> float:
    # Reasonable initial rating distribution for 2/4/8GB builds
    base = depth * 100
    adjustment = (search_eff - 0.8) * 500
    elo = base + adjustment
    if elo < 1200:
        elo = 1200
    if elo > 2600:
        elo = 2600
    return elo


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


def load_profile(pid: str) -> EngineProfile:
    info = STATIC_PROFILES[pid]
    # Try dynamic read from engine classes if possible
    mod_name, cls_name = ENGINE_MAP[pid]
    try:
        mod = importlib.import_module(mod_name)
        cls = getattr(mod, cls_name)
        engine = cls(available_time=1.0)
        depth = getattr(engine, "current_depth", None) or info["depth"]
        tt_mb = getattr(engine, "transposition_table_mb", None) or info["tt_mb"]
        threads = getattr(engine, "threads", info["threads"])
        time_cap = getattr(engine, "current_time", info["max_time_s"])
        search_eff = getattr(engine, "search_efficiency", info["search_eff"]) or info["search_eff"]
        est_elo = derive_elo_from(int(depth), float(search_eff))
        return EngineProfile(pid, info["name"], int(depth), int(tt_mb), int(threads), float(time_cap), float(search_eff), float(est_elo))
    except Exception:
        est_elo = derive_elo_from(info["depth"], info["search_eff"])
        return EngineProfile(pid, info["name"], info["depth"], info["tt_mb"], info["threads"], info["max_time_s"], info["search_eff"], est_elo)


def elo_expected(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


def update_elo(ra: float, rb: float, score_a: float, k: float) -> Tuple[float, float]:
    ea = elo_expected(ra, rb)
    eb = 1.0 - ea
    ra = ra + k * (score_a - ea)
    rb = rb + k * ((1.0 - score_a) - eb)
    return ra, rb


def board_to_engine_dict(board: chess.Board) -> Dict[str, str]:
    # Minimal representation used in the Pandoraga implementations
    # The classes expect a dict with piece codes, like {'e2': 'P', 'e4': 'P'}
    # We preserve a simple mapping from squares to piece symbols.
    out: Dict[str, str] = {}
    for sq, piece in board.piece_map().items():
        name = chess.square_name(sq)
        symbol = piece.symbol()
        out[name] = symbol
    return out


def choose_move(board: chess.Board, engine: object, side: chess.Color) -> chess.Move:
    """Choose a legal move by using the engine's evaluation heuristic.

    Different engine classes expose evaluate_position(board) or evaluate(board).
    We build a list of legal moves, attach a simple evaluation score per move,
    and choose the one with the best evaluation for the side to move.
    """
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        raise ValueError("No legal move available")

    evaluate_fn = None
    for name in ("evaluate_position", "evaluate"):
        if hasattr(engine, name):
            evaluate_fn = getattr(engine, name)
            break
    if evaluate_fn is None:
        # Fallback: random legal move, but still legal
        return random.choice(list(legal_moves))

    # Determine best evaluation score for the side to move.
    best_move = legal_moves[0]
    best_score = None

    for move in legal_moves:
        b2 = board.copy()
        b2.push(move)
        pos = board_to_engine_dict(b2)
        score = evaluate_fn(pos)
        # For the side to move, we want the move with best score for that side.
        # Because engine evaluate returns score as if white is positive, we adapt for black.
        if side == chess.WHITE:
            val = score
        else:
            val = -score
        if best_score is None or val > best_score:
            best_score = val
            best_move = move
    return best_move


def evaluate_game(engine_white: object, engine_black: object, max_moves: int = 200) -> Tuple[Optional[chess.Color], str]:
    """Play a real chess game using evaluation-based move selection.
    Returns (winner_color, reason) where winner_color is chess.WHITE, chess.BLACK or None for draw.
    """
    board = chess.Board()
    for _ in range(max_moves):
        if board.is_checkmate():
            winner = not board.turn
            return winner, "checkmate"
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return None, "draw"
        if board.turn == chess.WHITE:
            mv = choose_move(board, engine_white, chess.WHITE)
        else:
            mv = choose_move(board, engine_black, chess.BLACK)
        board.push(mv)

        if board.is_checkmate():
            winner = not board.turn
            return winner, "checkmate"
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return None, "draw"

    return None, "max_moves"


def load_engine_for_profile(pid: str, available_time: float = 1.0):
    mod_name, cls_name = ENGINE_MAP[pid]
    mod = importlib.import_module(mod_name)
    cls = getattr(mod, cls_name)
    return cls(available_time=available_time)


def run_matchup(a_pid: str, b_pid: str, games: int, k_factor: float, seed: Optional[int]) -> Dict[str, float]:
    if seed is not None:
        random.seed(seed)

    # Base Elo ratings using profile estimates
    pa = load_profile(a_pid)
    pb = load_profile(b_pid)
    ra = pa.est_elo
    rb = pb.est_elo

    stats = {"a_wins": 0, "b_wins": 0, "draws": 0}

    for idx in range(games):
        # Alternate colors across games to reduce first-player bias
        if idx % 2 == 0:
            white_pid, black_pid = a_pid, b_pid
        else:
            white_pid, black_pid = b_pid, a_pid

        # Load fresh engines for each game
        engine_white = load_engine_for_profile(white_pid, available_time=1.0)
        engine_black = load_engine_for_profile(black_pid, available_time=1.0)

        winner, reason = evaluate_game(engine_white, engine_black, max_moves=200)

        # Determine score for A side in this game
        if winner is None:
            score_a = 0.5
            stats["draws"] += 1
        elif (white_pid == a_pid and winner == chess.WHITE) or (black_pid == a_pid and winner == chess.BLACK):
            score_a = 1.0
            stats["a_wins"] += 1
        else:
            score_a = 0.0
            stats["b_wins"] += 1

        ra, rb = update_elo(ra, rb, score_a, k_factor)

    return {
        "a_pid": a_pid,
        "b_pid": b_pid,
        "a_elo": ra,
        "b_elo": rb,
        "a_wins": stats["a_wins"],
        "b_wins": stats["b_wins"],
        "draws": stats["draws"],
    }


def run_tournament(games: int, k_factor: float, seed: Optional[int]) -> None:
    print("Pandoraga 1v1 arena — real legal-move simulation")
    print(f"Games per matchup: {games}")
    print(f"Elo K-factor: {k_factor}")
    if seed is not None:
        print(f"Random seed: {seed}")
    print("\nMatchups: 2GB vs 4GB, 4GB vs 8GB, 2GB vs 8GB\n")

    # 1) 2GB vs 4GB
    result_2v4 = run_matchup("2", "4", games=games, k_factor=k_factor, seed=seed)
    print("[1] 2GB vs 4GB")
    print(result_2v4)
    print()

    # 2) 4GB vs 8GB
    result_4v8 = run_matchup("4", "8", games=games, k_factor=k_factor, seed=seed)
    print("[2] 4GB vs 8GB")
    print(result_4v8)
    print()

    # 3) 2GB vs 8GB
    result_2v8 = run_matchup("2", "8", games=games, k_factor=k_factor, seed=seed)
    print("[3] 2GB vs 8GB")
    print(result_2v8)
    print()

    print("Summary:")
    print(f"2GB vs 4GB -> 2GB Elo={result_2v4['a_elo']:.1f}, 4GB Elo={result_2v4['b_elo']:.1f}")
    print(f"4GB vs 8GB -> 4GB Elo={result_4v8['a_elo']:.1f}, 8GB Elo={result_4v8['b_elo']:.1f}")
    print(f"2GB vs 8GB -> 2GB Elo={result_2v8['a_elo']:.1f}, 8GB Elo={result_2v8['b_elo']:.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an Elo tournament between 2GB / 4GB / 8GB Pandoraga builds")
    parser.add_argument("--games", type=int, default=20, help="Games per matchup (default: 20)")
    parser.add_argument("--k", type=float, default=16.0, help="Elo K-factor (default: 16)")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    args = parser.parse_args()
    run_tournament(games=args.games, k_factor=args.k, seed=args.seed)

"""Pandoraga core engine.

This module contains the actual engine logic used by the Pandoraga profiles.
It is intentionally structured as a real engine core so the profiles remain thin
wrappers that only set memory/time/search thresholds.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Simple board model
# ---------------------------------------------------------------------------

FILES = "abcdefgh"
RANKS = "12345678"

PIECE_VALUES = {
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 20000,
    "p": -100,
    "n": -320,
    "b": -330,
    "r": -500,
    "q": -900,
    "k": -20000,
}

PIECE_TO_CHAR = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}


@dataclass
class Move:
    from_sq: str
    to_sq: str
    piece: str
    captured: Optional[str] = None
    promotion: Optional[str] = None
    score: int = 0

    def as_tuple(self) -> Tuple[str, str, str, Optional[str], Optional[str]]:
        return (self.from_sq, self.to_sq, self.piece, self.captured, self.promotion)

    def __str__(self) -> str:
        promo = f"={self.promotion}" if self.promotion else ""
        capture = "x" if self.captured else "-"
        return f"{self.from_sq}{capture}{self.to_sq}{promo}"


@dataclass
class SearchConfig:
    max_depth: int = 6
    tt_size_mb: int = 64
    threads: int = 1
    eval_sensitivity: float = 1.0
    max_time: float = 2.0
    min_time: float = 0.25
    aspiration_window: float = 32.0
    enable_mt: bool = False
    use_pvs: bool = True
    use_tt: bool = True
    use_null_move: bool = True
    feature_flags: Dict[str, bool] = field(default_factory=dict)


@dataclass
class EngineState:
    profile_name: str
    max_depth: int
    tt_size_mb: int
    threads: int
    eval_sensitivity: float
    max_time: float
    min_time: float
    cache_hits: int = 0
    cache_misses: int = 0
    nodes: int = 0
    last_move: Optional[str] = None
    message: str = ""


class TranspositionTable:
    def __init__(self, size_mb: int = 64):
        self.size_mb = size_mb
        self.capacity = max(512, size_mb * 1024)
        self._table: Dict[str, Tuple[int, int, int, int]] = {}

    def lookup(self, key: str) -> Optional[Tuple[int, int, int, int]]:
        return self._table.get(key)

    def store(self, key: str, value: Tuple[int, int, int, int]) -> None:
        if len(self._table) >= self.capacity:
            # Simple pruning: drop older entries by keeping the most recent state.
            for old_key in list(self._table)[: max(1, self.capacity // 10)]:
                self._table.pop(old_key, None)
        self._table[key] = value


class Board:
    """Minimal board representation for engine testing and search.

    This model stores piece placement as a dictionary keyed by square names,
    e.g. 'e2': 'P', 'e7': 'p'. It intentionally keeps the board light-weight and
    convenient for search experiments.
    """

    def __init__(self, position: Optional[Dict[str, str]] = None):
        self.position: Dict[str, str] = dict(position or {})

    @classmethod
    def initial_board(cls) -> "Board":
        pos = {}
        for file in FILES:
            pos[f"{file}2"] = "P"
            pos[f"{file}7"] = "p"
        for piece, squares in {
            "R": ["a1", "h1"],
            "N": ["b1", "g1"],
            "B": ["c1", "f1"],
            "Q": ["d1"],
            "K": ["e1"],
            "r": ["a8", "h8"],
            "n": ["b8", "g8"],
            "b": ["c8", "f8"],
            "q": ["d8"],
            "k": ["e8"],
        }.items():
            for sq in squares:
                pos[sq] = piece
        return cls(pos)

    def copy(self) -> "Board":
        return Board(dict(self.position))

    def square_to_coords(self, square: str) -> Tuple[int, int]:
        file_char = square[0]
        rank_char = square[-1]
        file_idx = FILES.index(file_char)
        rank_idx = int(rank_char) - 1
        return file_idx, rank_idx

    def coords_to_square(self, file_idx: int, rank_idx: int) -> str:
        return f"{FILES[file_idx]}{rank_idx + 1}"

    def is_empty(self, square: str) -> bool:
        return square not in self.position or self.position[square] == ""

    def piece_at(self, square: str) -> Optional[str]:
        return self.position.get(square)

    def set_piece(self, square: str, piece: Optional[str]) -> None:
        if piece is None:
            self.position.pop(square, None)
        else:
            self.position[square] = piece

    def material_balance(self) -> int:
        total = 0
        for piece in self.position.values():
            total += PIECE_VALUES.get(piece, 0)
        return total

    def generate_pseudo_moves(self, side_to_move: str) -> List[Move]:
        """Generate a broad, legal-ish set of pseudo moves.

        This is intentionally lightweight: it supports pawns, knights, bishops,
        rooks, queens and kings with basic movement rules. It does not attempt a
        full legal-move generator with pinned pieces or check legality, but it is
        sufficient for search tuning and demonstration.
        """
        moves: List[Move] = []
        for square, piece in self.position.items():
            if piece == "":
                continue
            is_white = piece.isupper()
            if side_to_move == "w" and not is_white:
                continue
            if side_to_move == "b" and is_white:
                continue
            file_idx, rank_idx = self.square_to_coords(square)
            if piece.upper() == "P":
                direction = 1 if is_white else -1
                target_rank = rank_idx + direction
                if 0 <= target_rank < 8:
                    target_sq = self.coords_to_square(file_idx, target_rank)
                    if self.is_empty(target_sq):
                        moves.append(Move(square, target_sq, piece))
                        if (is_white and rank_idx == 1) or ((not is_white) and rank_idx == 6):
                            double_rank = rank_idx + 2 * direction
                            if 0 <= double_rank < 8:
                                double_sq = self.coords_to_square(file_idx, double_rank)
                                if self.is_empty(double_sq):
                                    moves.append(Move(square, double_sq, piece))
                for delta in (-1, 1):
                    new_file = file_idx + delta
                    new_rank = rank_idx + direction
                    if 0 <= new_file < 8 and 0 <= new_rank < 8:
                        target_sq = self.coords_to_square(new_file, new_rank)
                        occupant = self.piece_at(target_sq)
                        if occupant and occupant.isupper() != is_white:
                            moves.append(Move(square, target_sq, piece, captured=occupant))
            elif piece.upper() == "N":
                for df, dr in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                    nf = file_idx + df
                    nr = rank_idx + dr
                    if 0 <= nf < 8 and 0 <= nr < 8:
                        target_sq = self.coords_to_square(nf, nr)
                        occupant = self.piece_at(target_sq)
                        if occupant is None or occupant.isupper() != is_white:
                            moves.append(Move(square, target_sq, piece, captured=occupant))
            elif piece.upper() in {"B", "R", "Q"}:
                directions = []
                if piece.upper() in {"B", "Q"}:
                    directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                if piece.upper() in {"R", "Q"}:
                    directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for df, dr in directions:
                    nf = file_idx + df
                    nr = rank_idx + dr
                    while 0 <= nf < 8 and 0 <= nr < 8:
                        target_sq = self.coords_to_square(nf, nr)
                        occupant = self.piece_at(target_sq)
                        if occupant is None:
                            moves.append(Move(square, target_sq, piece))
                        else:
                            if occupant.isupper() != is_white:
                                moves.append(Move(square, target_sq, piece, captured=occupant))
                            break
                        nf += df
                        nr += dr
            elif piece.upper() == "K":
                for df in (-1, 0, 1):
                    for dr in (-1, 0, 1):
                        if df == 0 and dr == 0:
                            continue
                        nf = file_idx + df
                        nr = rank_idx + dr
                        if 0 <= nf < 8 and 0 <= nr < 8:
                            target_sq = self.coords_to_square(nf, nr)
                            occupant = self.piece_at(target_sq)
                            if occupant is None or occupant.isupper() != is_white:
                                moves.append(Move(square, target_sq, piece, captured=occupant))
        return moves

    def apply_move(self, move: Move) -> "Board":
        new_board = self.copy()
        piece = new_board.position.pop(move.from_sq)
        if move.captured:
            new_board.position.pop(move.to_sq, None)
        if move.promotion:
            piece = move.promotion if piece.isupper() else move.promotion.lower()
        new_board.position[move.to_sq] = piece
        return new_board

    def terminal_score(self, side_to_move: str) -> int:
        # Tiny heuristic for evaluation. Purely for search and testing.
        return 0 if side_to_move in {"w", "b"} else 0

    def __str__(self) -> str:
        lines = []
        for rank in range(8, 0, -1):
            row = []
            for file in FILES:
                sq = f"{file}{rank}"
                piece = self.position.get(sq)
                row.append(PIECE_TO_CHAR.get(piece, ".") if piece else ".")
            lines.append(" ".join(row))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def evaluate_board(board: Board, side_to_move: str, config: SearchConfig) -> int:
    """Material and mobility based evaluation."""
    score = 0
    for piece in board.position.values():
        score += PIECE_VALUES.get(piece, 0)
    mobility = len(board.generate_pseudo_moves(side_to_move))
    score += mobility * 2
    score = int(score * config.eval_sensitivity)
    return score


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def order_moves(moves: Iterable[Move], board: Board, side_to_move: str) -> List[Move]:
    ordered = list(moves)
    for move in ordered:
        if move.captured:
            move.score += PIECE_VALUES.get(move.captured, 0) - PIECE_VALUES.get(move.piece, 0) // 10
        if move.promotion:
            move.score += PIECE_VALUES.get(move.promotion, 0)
    ordered.sort(key=lambda x: x.score, reverse=True)
    return ordered


class PandoragaEngine:
    def __init__(self, profile_name: str = "default", config: Optional[SearchConfig] = None):
        self.profile_name = profile_name
        self.config = config or SearchConfig()
        self.tt = TranspositionTable(self.config.tt_size_mb)
        self.history: List[str] = []
        self.nodes = 0

    def set_config(self, config: SearchConfig) -> None:
        self.config = config
        self.tt = TranspositionTable(self.config.tt_size_mb)

    def _key_for_board(self, board: Board, side_to_move: str, depth: int) -> str:
        pieces = tuple(sorted(board.position.items()))
        return f"{side_to_move}:{depth}:{pieces}"

    def _negamax(self, board: Board, depth: int, alpha: int, beta: int, side_to_move: str) -> int:
        self.nodes += 1
        if depth == 0:
            return evaluate_board(board, side_to_move, self.config)

        key = self._key_for_board(board, side_to_move, depth)
        if self.config.use_tt:
            cached = self.tt.lookup(key)
            if cached is not None:
                return cached[0]

        legal_moves = order_moves(board.generate_pseudo_moves(side_to_move), board, side_to_move)
        if not legal_moves:
            return -100000 + (self.config.max_depth - depth)

        best_score = -10**9
        for move in legal_moves:
            next_board = board.apply_move(move)
            score = -self._negamax(next_board, depth - 1, -beta, -alpha, "b" if side_to_move == "w" else "w")
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        if self.config.use_tt:
            self.tt.store(key, (best_score, alpha, beta, depth))
        return best_score

    def choose_move(self, board: Board, side_to_move: str = "w") -> Optional[Move]:
        legal_moves = board.generate_pseudo_moves(side_to_move)
        if not legal_moves:
            return None
        ordered = order_moves(legal_moves, board, side_to_move)
        best_move = ordered[0]
        best_score = -10**9
        alpha = -10**9
        beta = 10**9
        for move in ordered:
            next_board = board.apply_move(move)
            score = -self._negamax(next_board, self.config.max_depth - 1, -beta, -alpha, "b" if side_to_move == "w" else "w")
            if score > best_score:
                best_score = score
                best_move = move
        self.history.append(str(best_move))
        return best_move

    def search(self, board: Board, side_to_move: str = "w") -> EngineState:
        start = time.perf_counter()
        move = self.choose_move(board, side_to_move)
        elapsed = time.perf_counter() - start
        state = EngineState(
            profile_name=self.profile_name,
            max_depth=self.config.max_depth,
            tt_size_mb=self.config.tt_size_mb,
            threads=self.config.threads,
            eval_sensitivity=self.config.eval_sensitivity,
            max_time=self.config.max_time,
            min_time=self.config.min_time,
            cache_hits=0,
            cache_misses=0,
            nodes=self.nodes,
            last_move=str(move) if move else None,
            message=f"Searched {self.nodes} nodes in {elapsed:.3f}s",
        )
        return state


def create_engine_for_profile(profile_name: str, ram_gb: float = 8.0) -> PandoragaEngine:
    config = SearchConfig()
    profile_name = profile_name.lower()

    if profile_name == "2gb":
        config.max_depth = 16
        config.tt_size_mb = 24
        config.threads = 1
        config.eval_sensitivity = 2.0
        config.max_time = 4.0
        config.min_time = 0.4
    elif profile_name == "8gb":
        config.max_depth = 20
        config.tt_size_mb = 256
        config.threads = 2
        config.eval_sensitivity = 2.0
        config.max_time = 10.0
        config.min_time = 0.6
    elif profile_name == "12gb":
        config.max_depth = 24
        config.tt_size_mb = 512
        config.threads = 4
        config.eval_sensitivity = 2.5
        config.max_time = 15.0
        config.min_time = 1.0
    else:
        config.max_depth = 18
        config.tt_size_mb = 128
        config.threads = 2
        config.eval_sensitivity = 1.8
        config.max_time = 6.0
        config.min_time = 0.8

    if ram_gb < 8.0 and profile_name in {"8gb", "12gb"}:
        config.max_depth = max(8, config.max_depth - 4)
        config.tt_size_mb = max(32, config.tt_size_mb // 2)
        config.threads = 1

    return PandoragaEngine(profile_name=profile_name, config=config)


if __name__ == "__main__":
    board = Board.initial_board()
    engine = create_engine_for_profile("12gb")
    move = engine.choose_move(board, side_to_move="w")
    print("Best move:", move)
    state = engine.search(board, side_to_move="w")
    print(state.message)

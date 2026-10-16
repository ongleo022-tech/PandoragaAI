from __future__ import annotations

import importlib
import os
import traceback
from typing import Any, Dict, Tuple

import chess
from flask import Flask, jsonify, request

app = Flask(__name__)

PROFILE_META: Dict[str, Dict[str, Any]] = {
    "2": {
        "profile": "2GB",
        "depth": 16,
        "threads": 1,
        "transposition_table_mb": 24,
        "max_time_s": 4.0,
        "eval_sensitivity": 2.0,
    },
    "4": {
        "profile": "4GB",
        "depth": 18,
        "threads": 1,
        "transposition_table_mb": 64,
        "max_time_s": 5.0,
        "eval_sensitivity": 2.0,
    },
    "8": {
        "profile": "8GB",
        "depth": 20,
        "threads": 2,
        "transposition_table_mb": 256,
        "max_time_s": 10.0,
        "eval_sensitivity": 2.0,
    },
}

ENGINE_MAP = {
    "2": ("Pandoraga_2GB", "AutoAdaptiveEngine2GB"),
    "4": ("Pandoraga", "AutoAdaptiveEngine4GB"),
    "8": ("Pandoraga_8GB", "AutoAdaptiveEngine8GB"),
}


def load_engine(profile_id: str, available_time: float = 1.0):
    module_name, class_name = ENGINE_MAP.get(profile_id, (None, None))
    if not module_name or not class_name:
        raise ValueError(f"Unknown profile id: {profile_id}")

    module = importlib.import_module(module_name)
    engine_cls = getattr(module, class_name)
    return engine_cls(available_time=available_time)


def board_to_engine_dict(board: chess.Board) -> Dict[str, str]:
    payload: Dict[str, str] = {}
    for square, piece in board.piece_map().items():
        payload[chess.square_name(square)] = piece.symbol()
    return payload


def get_score_for_move(engine: Any, board: chess.Board, move: chess.Move) -> float:
    next_board = board.copy()
    next_board.push(move)
    board_dict = board_to_engine_dict(next_board)

    # Try the most relevant methods in priority order.
    for method_name in ("evaluate_position", "evaluate"):
        fn = getattr(engine, method_name, None)
        if callable(fn):
            try:
                score = float(fn(board_dict))
                return score if board.turn == chess.WHITE else -score
            except TypeError:
                try:
                    score = float(fn(next_board))
                    return score if board.turn == chess.WHITE else -score
                except Exception:
                    continue
            except Exception:
                continue

    # Fallback: simple material heuristic approximating a standard engine evaluation.
    piece_values = {
        "P": 1.0,
        "N": 3.2,
        "B": 3.3,
        "R": 5.1,
        "Q": 9.0,
        "K": 0.0,
        "p": -1.0,
        "n": -3.2,
        "b": -3.3,
        "r": -5.1,
        "q": -9.0,
        "k": 0.0,
    }
    score = 0.0
    for piece in next_board.piece_map().values():
        symbol = piece.symbol()
        score += piece_values.get(symbol, 0.0)
    return score if board.turn == chess.WHITE else -score


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Pandoraga API"})


@app.route("/api/ongleo022-tech/<profile_id>", methods=["GET"])
def get_profile(profile_id: str):
    profile = PROFILE_META.get(profile_id)
    if not profile:
        return jsonify({"error": "profile not found"}), 404
    return jsonify(profile)


@app.route("/api/ongleo022-tech/<profile_id>/move", methods=["POST"])
def get_best_move(profile_id: str):
    data = request.get_json(silent=True) or {}
    fen = data.get("fen")
    time_s = float(data.get("time_s", 1.0))

    if not fen:
        return jsonify({"error": "fen required"}), 400

    try:
        board = chess.Board(fen)
    except ValueError as exc:
        return jsonify({"error": f"invalid fen: {exc}"}), 400

    if board.is_game_over():
        return jsonify({"status": "game_over", "best_move": None, "fen": board.fen()}), 200

    try:
        engine = load_engine(profile_id, available_time=time_s)
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": f"failed to load engine: {exc}", "trace": traceback.format_exc()}), 500

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return jsonify({"status": "no_legal_moves", "best_move": None, "fen": board.fen()}), 200

    best_move: chess.Move | None = None
    best_score: float | None = None

    for move in legal_moves:
        score = get_score_for_move(engine, board, move)
        if best_score is None or score > best_score:
            best_score = score
            best_move = move

    if best_move is None:
        return jsonify({"status": "no_best_move", "best_move": None, "fen": board.fen()}), 200

    return jsonify(
        {
            "status": "ok",
            "profile": PROFILE_META.get(profile_id, {}).get("profile", profile_id),
            "best_move": best_move.uci(),
            "uci": best_move.uci(),
            "evaluation": round(float(best_score), 4),
            "fen": board.fen(),
            "engine_time_s": round(float(time_s), 3),
        }
    )


@app.route("/api/ongleo022-tech/<profile_id>/search", methods=["POST"])
def get_search(profile_id: str):
    data = request.get_json(silent=True) or {}
    fen = data.get("fen")
    time_s = float(data.get("time_s", 1.0))
    if not fen:
        return jsonify({"error": "fen required"}), 400

    try:
        board = chess.Board(fen)
    except ValueError as exc:
        return jsonify({"error": f"invalid fen: {exc}"}), 400

    move_result = get_best_move(profile_id)
    # Reuse the same logic but in a search-friendly response format.
    if hasattr(move_result, "get_json"):
        payload = move_result.get_json()
    else:
        payload = move_result

    # The route above may return a Flask response; not used directly; but the response is assembled in a single endpoint.
    # Recompute so the response is consistent.
    try:
        engine = load_engine(profile_id, available_time=time_s)
    except Exception as exc:
        return jsonify({"error": f"failed to load engine: {exc}"}), 500

    legal = list(board.legal_moves)
    if not legal:
        return jsonify({"status": "no_legal_moves", "best_move": None, "fen": board.fen()}), 200

    best_move = None
    best_score = None
    for move in legal:
        score = get_score_for_move(engine, board, move)
        if best_score is None or score > best_score:
            best_score = score
            best_move = move

    return jsonify(
        {
            "status": "ok",
            "profile": PROFILE_META.get(profile_id, {}).get("profile", profile_id),
            "best_move": best_move.uci() if best_move else None,
            "fen": board.fen(),
            "time_s": round(time_s, 3),
            "evaluation": round(float(best_score), 4) if best_score is not None else 0.0,
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)

"""Pandoraga Omega - Full Adaptation Chess Engine.

This file provides the project skeleton used for an experimental Python chess engine.
It includes the requested depth constants and a minimal Tkinter interface that allows
changing the maximum search depth up to 18.
"""

from __future__ import annotations

import math
from typing import Optional

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # pragma: no cover
    tk = None
    ttk = None


AUTO_MAX_DEPTH = 18
MAX_DEPTH = 18
DEFAULT_TIME_PER_MOVE = 2.0


class PandoragaEngine:
    """Minimal chess-engine foundation used for experimentation.

    The class intentionally stays lightweight and readable: it exposes a search-depth
    configuration and a simple material-based evaluation logic. It can later be
    expanded with full legal-move generation, alpha-beta pruning and move ordering.
    """

    def __init__(self, max_depth: int = AUTO_MAX_DEPTH):
        self.max_depth = max(1, min(max_depth, MAX_DEPTH))

    def evaluate_position(self, board: dict) -> float:
        """Provide a simple material evaluation placeholder.

        This function is intentionally lightweight. It returns a basic score based on
        the piece count in the board dictionary. A real chess engine would replace this
        with positional evaluation, mobility evaluation, king safety, endgame handling,
        etc.
        """
        score = 0.0
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

        for square, piece in board.items():
            if piece in piece_values:
                score += piece_values[piece]

        return score

    def best_move(self, board: dict) -> Optional[str]:
        """Return the next best move placeholder.

        A full chess engine would search legal moves recursively. This placeholder is
        intentionally simple and suitable as a project scaffold.
        """
        if not board:
            return None
        return next(iter(board.keys()))

    def search(self, board: dict) -> float:
        """Search placeholder using the configured maximum depth."""
        return self.evaluate_position(board) * (1.0 / max(1, self.max_depth))


class PandoragaApp:
    """Tkinter launcher for the engine.

    The interface contains a depth slider and status labels. This keeps the app usable
    on Windows while making it easy to configure the maximum search depth up to 18.
    """

    def __init__(self, root: tk.Tk):
        if tk is None:
            raise RuntimeError("tkinter is not available in this Python environment.")

        self.root = root
        self.root.title("Pandoraga Omega - Full Adaptation")
        self.root.geometry("620x240")
        self.root.resizable(False, False)

        self.engine = PandoragaEngine(AUTO_MAX_DEPTH)
        self.selected_depth = tk.IntVar(value=AUTO_MAX_DEPTH)

        ttk.Label(
            root,
            text="Pandoraga Omega",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(18, 8))

        ttk.Label(
            root,
            text="Depth configuration",
            font=("Segoe UI", 10),
        ).pack()

        ttk.Scale(
            root,
            from_=1,
            to=MAX_DEPTH,
            variable=self.selected_depth,
            orient="horizontal",
            length=420,
            command=self._on_depth_change,
        ).pack(pady=8)

        self.depth_label = ttk.Label(root, text=f"Current depth: {AUTO_MAX_DEPTH}")
        self.depth_label.pack(pady=(0, 4))

        self.status_label = ttk.Label(
            root,
            text="Engine ready. Search depth is configured for experimentation.",
            wraplength=500,
            justify="center",
        )
        self.status_label.pack(pady=8)

        ttk.Button(root, text="Run engine", command=self.run_engine).pack(pady=(8, 12))

    def _on_depth_change(self, *_):
        value = int(self.selected_depth.get())
        self.engine.max_depth = max(1, min(value, MAX_DEPTH))
        self.depth_label.config(text=f"Current depth: {self.engine.max_depth}")
        self.status_label.config(
            text=(
                "Depth updated. The engine is configured for a search up to "
                f"{self.engine.max_depth}."
            )
        )

    def run_engine(self):
        self.status_label.config(
            text=(
                "Pandoraga Omega is ready. Search depth: "
                f"{self.engine.max_depth}. "
                "A full chess engine can be expanded from this foundation."
            )
        )


def main() -> None:
    if tk is None:
        print("Pandoraga Omega")
        print(f"AUTO_MAX_DEPTH = {AUTO_MAX_DEPTH}")
        print(f"MAX_DEPTH = {MAX_DEPTH}")
        print("Tkinter is not available in this environment; no GUI will be displayed.")
        return

    root = tk.Tk()
    app = PandoragaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Minimax Adversarial Search Agent with Alpha-Beta Pruning.
Implements:
1. Standard Minimax (zero-sum game tree search)
2. Alpha-Beta Pruning (branch elimination)
3. Move Ordering optimization (center-first traversal)
4. Telemetry tracking (nodes visited, cutoffs, elapsed time)
"""
from __future__ import annotations
import math
import time
from typing import Tuple, Optional

from agents.base_agent import Agent
from agents.heuristic import score_position
from game.board import Board
from game.constants import (
    OPTIMAL_COLUMN_ORDER,
)


class MinimaxAgent(Agent):
    """
    Adversarial Search Agent using Minimax with optional Alpha-Beta Pruning.
    """

    def __init__(
        self,
        name: str = "Minimax AI",
        piece: int = 2,
        depth: int = 4,
        use_pruning: bool = True,
        order_moves: bool = True,
    ) -> None:
        super().__init__(name, piece)
        self.depth = depth
        self.use_pruning = use_pruning
        self.order_moves = order_moves

        # Telemetry metrics updated per move
        self.nodes_visited = 0
        self.pruning_cutoffs = 0
        self.last_search_time = 0.0

    def _get_ordered_moves(self, board: Board) -> list[int]:
        """
        Return valid moves ordered to maximize early alpha-beta cutoffs.
        Examining the center column first yields the strongest baseline
        moves early, tightening [alpha, beta] faster.
        """
        valid_moves = set(board.get_valid_locations())
        if self.order_moves:
            return [c for c in OPTIMAL_COLUMN_ORDER if c in valid_moves]
        return list(valid_moves)

    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        is_maximizing: bool,
    ) -> Tuple[Optional[int], float]:
        """
        Recursive Minimax / Alpha-Beta algorithm.
        Returns (best_column, best_score).
        """
        self.nodes_visited += 1

        is_term, winner = board.is_terminal()
        if is_term:
            if winner == self.piece:
                # Prioritize faster wins: higher score for remaining depth
                return None, 1_000_000.0 + depth
            elif winner == self.opponent_piece:
                # Prioritize delayed losses: lower score for earlier losses
                return None, -1_000_000.0 - depth
            else:
                # Draw
                return None, 0.0

        if depth == 0:
            # Leaf node reached: evaluate position using static heuristic
            return None, float(score_position(board, self.piece))

        valid_moves = self._get_ordered_moves(board)

        if is_maximizing:
            max_eval = -math.inf
            best_col = valid_moves[0]

            for col in valid_moves:
                row = board.drop_piece(col, self.piece)
                _, current_eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.undo_move(col, row)

                if current_eval > max_eval:
                    max_eval = current_eval
                    best_col = col

                if self.use_pruning:
                    alpha = max(alpha, max_eval)
                    if beta <= alpha:
                        self.pruning_cutoffs += 1
                        break  # Beta cutoff: Minimizer would avoid this branch

            return best_col, max_eval

        else:  # Minimizing player (Adversary)
            min_eval = math.inf
            best_col = valid_moves[0]

            for col in valid_moves:
                row = board.drop_piece(col, self.opponent_piece)
                _, current_eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.undo_move(col, row)

                if current_eval < min_eval:
                    min_eval = current_eval
                    best_col = col

                if self.use_pruning:
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        self.pruning_cutoffs += 1
                        break  # Alpha cutoff: Maximizer would avoid this branch

            return best_col, min_eval

    def get_move(self, board: Board) -> int:
        """
        Select the optimal column for the current board state.
        Resets and records search telemetry.
        """
        self.nodes_visited = 0
        self.pruning_cutoffs = 0
        start_time = time.perf_counter()

        col, score = self._minimax(
            board=board,
            depth=self.depth,
            alpha=-math.inf,
            beta=math.inf,
            is_maximizing=True,
        )

        self.last_search_time = time.perf_counter() - start_time

        if col is None:
            # Fallback if already terminal or single move
            valid = board.get_valid_locations()
            return valid[0] if valid else 0

        return col

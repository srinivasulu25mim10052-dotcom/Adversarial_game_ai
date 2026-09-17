"""
Monte Carlo Tree Search (MCTS) Agent for Connect Four.
Implements the 4 classic phases of MCTS with Upper Confidence Bounds for Trees (UCT):
1. Selection (UCT)
2. Expansion
3. Simulation (Rollout)
4. Backpropagation
"""
from __future__ import annotations
import math
import random
import time
from typing import Optional, List

from agents.base_agent import Agent
from game.board import Board


class MCTSNode:
    """A node in the Monte Carlo Tree Search graph."""

    def __init__(
        self,
        board: Board,
        parent: Optional[MCTSNode] = None,
        move: Optional[int] = None,
        player_who_moved: int = 1,
    ) -> None:
        self.board = board
        self.parent = parent
        self.move = move
        self.player_who_moved = player_who_moved

        self.children: dict[int, MCTSNode] = {}
        self.visits = 0
        self.wins = 0.0  # From perspective of player_who_moved
        self.untried_moves: List[int] = board.get_valid_locations()

    @property
    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    @property
    def is_terminal(self) -> bool:
        is_term, _ = self.board.is_terminal()
        return is_term

    def best_child_uct(self, exploration_weight: float = 1.414) -> MCTSNode:
        """Select child with highest UCT (Upper Confidence Bound for Trees)."""
        best_score = -math.inf
        best_child = None

        log_parent_visits = math.log(self.visits)

        for child in self.children.values():
            exploitation = child.wins / child.visits
            exploration = exploration_weight * math.sqrt(log_parent_visits / child.visits)
            uct_value = exploitation + exploration

            if uct_value > best_score:
                best_score = uct_value
                best_child = child

        if best_child is None:
            raise RuntimeError("No children to select from in UCT.")
        return best_child


class MCTSAgent(Agent):
    """
    Monte Carlo Tree Search Agent.
    Learns state values through stochastic simulation rather than static heuristic evaluation.
    """

    def __init__(
        self,
        name: str = "MCTS Agent",
        piece: int = 2,
        iterations: int = 400,
        exploration_weight: float = 1.414,
        max_rollout_depth: int = 30,
    ) -> None:
        super().__init__(name, piece)
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        self.max_rollout_depth = max_rollout_depth
        self.last_search_time = 0.0

    def get_move(self, board: Board) -> int:
        start_time = time.perf_counter()

        valid_moves = board.get_valid_locations()
        if len(valid_moves) == 1:
            return valid_moves[0]

        # Root node represents the current board before our move
        root = MCTSNode(
            board=board.clone(),
            parent=None,
            move=None,
            player_who_moved=self.opponent_piece,
        )

        for _ in range(self.iterations):
            node = root

            # 1. Selection: descend tree until non-fully-expanded or terminal node
            while not node.is_terminal and node.is_fully_expanded:
                node = node.best_child_uct(self.exploration_weight)

            # 2. Expansion: expand an untried move if not terminal
            if not node.is_terminal and node.untried_moves:
                move = node.untried_moves.pop()
                next_player = 1 if node.player_who_moved == 2 else 2

                next_board = node.board.clone()
                next_board.drop_piece(move, next_player)

                child_node = MCTSNode(
                    board=next_board,
                    parent=node,
                    move=move,
                    player_who_moved=next_player,
                )
                node.children[move] = child_node
                node = child_node

            # 3. Simulation / Rollout: simulate random game until terminal or max depth
            winner = self._simulate(node.board.clone(), node.player_who_moved)

            # 4. Backpropagation: propagate result up to root
            curr: Optional[MCTSNode] = node
            while curr is not None:
                curr.visits += 1
                if winner is not None:
                    if winner == curr.player_who_moved:
                        curr.wins += 1.0
                    else:
                        curr.wins += 0.0
                else:
                    # Draw
                    curr.wins += 0.5
                curr = curr.parent

        self.last_search_time = time.perf_counter() - start_time

        # Robust Child: choose the move that received the most visits
        best_move = max(root.children.items(), key=lambda item: item[1].visits)[0]
        return best_move

    def _simulate(self, sim_board: Board, last_player: int) -> Optional[int]:
        """Fast rollout simulation to game end or cutoff."""
        curr_player = 1 if last_player == 2 else 2
        moves_made = 0

        while moves_made < self.max_rollout_depth:
            is_term, winner = sim_board.is_terminal()
            if is_term:
                return winner

            moves = sim_board.get_valid_locations()
            if not moves:
                return None  # Draw

            # Quick check for immediate winning move in rollout (light rollout policy)
            winning_move = None
            for m in moves:
                row = sim_board.drop_piece(m, curr_player)
                if sim_board.is_winning_move(curr_player):
                    winning_move = m
                    sim_board.undo_move(m, row)
                    break
                sim_board.undo_move(m, row)

            if winning_move is not None:
                sim_board.drop_piece(winning_move, curr_player)
                return curr_player

            chosen_move = random.choice(moves)
            sim_board.drop_piece(chosen_move, curr_player)
            curr_player = 1 if curr_player == 2 else 2
            moves_made += 1

        is_term, winner = sim_board.is_terminal()
        return winner

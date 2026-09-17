"""Unit tests for Minimax and Alpha-Beta search correctness and efficiency."""
import unittest
import math

from game.board import Board
from game.constants import PLAYER_PIECE, AI_PIECE
from agents.minimax_agent import MinimaxAgent


class TestSearch(unittest.TestCase):

    def test_immediate_win_detection(self):
        """AI must seize an immediate horizontal win at depth 1."""
        board = Board()
        # AI has pieces at (0, 0), (0, 1), (0, 2)
        board.drop_piece(0, AI_PIECE)
        board.drop_piece(1, AI_PIECE)
        board.drop_piece(2, AI_PIECE)

        agent = MinimaxAgent(depth=1, use_pruning=True)
        move = agent.get_move(board)

        # Winning move is column 3
        self.assertEqual(move, 3)

    def test_horizontal_block_detection(self):
        """AI must block the opponent's single open-ended horizontal threat."""
        board = Board()
        # Left boundary is capped by an AI piece at col 0
        board.drop_piece(0, AI_PIECE)
        # Player has 3-in-a-row at cols 1, 2, 3
        board.drop_piece(1, PLAYER_PIECE)
        board.drop_piece(2, PLAYER_PIECE)
        board.drop_piece(3, PLAYER_PIECE)

        agent = MinimaxAgent(depth=2, use_pruning=True)
        move = agent.get_move(board)

        # AI must play col 4 to prevent Player from completing 4-in-a-row on next turn
        self.assertEqual(move, 4)

    def test_vertical_block_detection(self):
        """AI must block an opponent's vertical 3-in-a-row threat by dropping on top."""
        board = Board()
        # Player has 3 pieces stacked in column 5
        board.drop_piece(5, PLAYER_PIECE)
        board.drop_piece(5, PLAYER_PIECE)
        board.drop_piece(5, PLAYER_PIECE)

        agent = MinimaxAgent(depth=2, use_pruning=True)
        move = agent.get_move(board)

        # AI must block column 5
        self.assertEqual(move, 5)

    def test_vertical_win_detection(self):
        """AI must stack on top to complete a vertical 4-in-a-row."""
        board = Board()
        board.drop_piece(4, AI_PIECE)
        board.drop_piece(4, AI_PIECE)
        board.drop_piece(4, AI_PIECE)

        agent = MinimaxAgent(depth=1, use_pruning=True)
        move = agent.get_move(board)

        self.assertEqual(move, 4)

    def test_alpha_beta_pruning_equivalence_and_speedup(self):
        """
        Minimax without pruning vs with Alpha-Beta pruning:
        Both must evaluate to the EXACT SAME optimal decision,
        but Alpha-Beta must visit substantially fewer nodes.
        """
        board = Board()
        # Seed board with a realistic mid-game state
        board.drop_piece(3, PLAYER_PIECE)
        board.drop_piece(3, AI_PIECE)
        board.drop_piece(2, PLAYER_PIECE)
        board.drop_piece(4, AI_PIECE)

        depth = 4
        pure_agent = MinimaxAgent(depth=depth, use_pruning=False, order_moves=False)
        pruned_agent = MinimaxAgent(depth=depth, use_pruning=True, order_moves=False)
        ordered_agent = MinimaxAgent(depth=depth, use_pruning=True, order_moves=True)

        pure_move = pure_agent.get_move(board)
        pure_nodes = pure_agent.nodes_visited

        pruned_move = pruned_agent.get_move(board)
        pruned_nodes = pruned_agent.nodes_visited

        ordered_move = ordered_agent.get_move(board)
        ordered_nodes = ordered_agent.nodes_visited

        # Decisions must be equally optimal
        self.assertEqual(pure_move, pruned_move)

        # Alpha-Beta MUST prune branches
        self.assertLess(pruned_nodes, pure_nodes)
        self.assertGreater(pruned_agent.pruning_cutoffs, 0)

        # Move ordering should prune even more aggressively
        self.assertLessEqual(ordered_nodes, pruned_nodes)


if __name__ == "__main__":
    unittest.main()

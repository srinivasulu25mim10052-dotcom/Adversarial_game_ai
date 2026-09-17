"""Unit tests for Connect Four board logic and terminal checks."""
import unittest
import numpy as np

from game.board import Board
from game.constants import (
    ROW_COUNT,
    COLUMN_COUNT,
    PLAYER_PIECE,
    AI_PIECE,
    EMPTY,
)


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_is_empty(self):
        self.assertTrue(np.all(self.board.grid == EMPTY))
        self.assertEqual(len(self.board.get_valid_locations()), COLUMN_COUNT)

    def test_drop_piece_and_gravity(self):
        # Drop into col 0: should land on row 0
        r1 = self.board.drop_piece(0, PLAYER_PIECE)
        self.assertEqual(r1, 0)
        self.assertEqual(self.board.grid[0, 0], PLAYER_PIECE)

        # Drop again into col 0: should land on row 1
        r2 = self.board.drop_piece(0, AI_PIECE)
        self.assertEqual(r2, 1)
        self.assertEqual(self.board.grid[1, 0], AI_PIECE)

    def test_column_overflow(self):
        for _ in range(ROW_COUNT):
            self.board.drop_piece(2, PLAYER_PIECE)

        self.assertFalse(self.board.is_valid_location(2))
        self.assertNotIn(2, self.board.get_valid_locations())

        with self.assertRaises(ValueError):
            self.board.drop_piece(2, PLAYER_PIECE)

    def test_undo_move(self):
        row = self.board.drop_piece(3, PLAYER_PIECE)
        self.assertEqual(self.board.grid[row, 3], PLAYER_PIECE)
        self.board.undo_move(3, row)
        self.assertEqual(self.board.grid[row, 3], EMPTY)

    def test_horizontal_win(self):
        # 4 in a row across columns 1, 2, 3, 4 on bottom row
        for c in range(1, 5):
            self.board.drop_piece(c, PLAYER_PIECE)

        self.assertTrue(self.board.is_winning_move(PLAYER_PIECE))
        self.assertFalse(self.board.is_winning_move(AI_PIECE))
        is_term, winner = self.board.is_terminal()
        self.assertTrue(is_term)
        self.assertEqual(winner, PLAYER_PIECE)

    def test_vertical_win(self):
        for _ in range(4):
            self.board.drop_piece(4, AI_PIECE)

        self.assertTrue(self.board.is_winning_move(AI_PIECE))
        is_term, winner = self.board.is_terminal()
        self.assertTrue(is_term)
        self.assertEqual(winner, AI_PIECE)

    def test_positive_diagonal_win(self):
        # Create positive diagonal:
        # Col 0: P
        # Col 1: A, P
        # Col 2: A, A, P
        # Col 3: A, A, A, P
        self.board.drop_piece(0, PLAYER_PIECE)

        self.board.drop_piece(1, AI_PIECE)
        self.board.drop_piece(1, PLAYER_PIECE)

        self.board.drop_piece(2, AI_PIECE)
        self.board.drop_piece(2, AI_PIECE)
        self.board.drop_piece(2, PLAYER_PIECE)

        self.board.drop_piece(3, AI_PIECE)
        self.board.drop_piece(3, AI_PIECE)
        self.board.drop_piece(3, AI_PIECE)
        self.board.drop_piece(3, PLAYER_PIECE)

        self.assertTrue(self.board.is_winning_move(PLAYER_PIECE))

    def test_negative_diagonal_win(self):
        # Create negative diagonal (\)
        # Col 0: A, A, A, P
        # Col 1: A, A, P
        # Col 2: A, P
        # Col 3: P
        for _ in range(3):
            self.board.drop_piece(0, AI_PIECE)
        self.board.drop_piece(0, PLAYER_PIECE)

        for _ in range(2):
            self.board.drop_piece(1, AI_PIECE)
        self.board.drop_piece(1, PLAYER_PIECE)

        self.board.drop_piece(2, AI_PIECE)
        self.board.drop_piece(2, PLAYER_PIECE)

        self.board.drop_piece(3, PLAYER_PIECE)

        self.assertTrue(self.board.is_winning_move(PLAYER_PIECE))


if __name__ == "__main__":
    unittest.main()

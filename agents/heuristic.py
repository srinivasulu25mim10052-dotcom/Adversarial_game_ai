
from typing import Sequence
import numpy as np
from game.board import Board
from game.constants import (
    ROW_COUNT,
    COLUMN_COUNT,
    EMPTY,
    WINDOW_LENGTH,
)


def evaluate_window(window: Sequence[int], piece: int, opponent: int) -> int:
    score = 0
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent)

    if piece_count == 4:
        score += 10000
    elif piece_count == 3 and empty_count == 1:
        score += 100
    elif piece_count == 2 and empty_count == 2:
        score += 10


    if opp_count == 3 and empty_count == 1:
        score -= 150
    elif opp_count == 2 and empty_count == 2:
        score -= 10

    return score


def score_position(board: Board, piece: int) -> int:
   
    score = 0
    opponent = 1 if piece == 2 else 2
    grid = board.grid

    center_array = [int(v) for v in grid[:, COLUMN_COUNT // 2]]
    center_count = center_array.count(piece)
    opp_center_count = center_array.count(opponent)
    score += (center_count - opp_center_count) * 6

     for c in [COLUMN_COUNT // 2 - 1, COLUMN_COUNT // 2 + 1]:
        col_array = [int(v) for v in grid[:, c]]
        score += (col_array.count(piece) - col_array.count(opponent)) * 3

     for r in range(ROW_COUNT):
        row_array = [int(v) for v in grid[r, :]]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece, opponent)

    for c in range(COLUMN_COUNT):
        col_array = [int(v) for v in grid[:, c]]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece, opponent)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [grid[r + i, c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece, opponent)
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [grid[r - i, c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece, opponent)

    return score

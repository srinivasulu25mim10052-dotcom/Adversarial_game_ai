
from __future__ import annotations
import numpy as np
from typing import Optional

from game.constants import (
    ROW_COUNT,
    COLUMN_COUNT,
    EMPTY,
    PLAYER_PIECE,
    AI_PIECE,
    SYMBOL_EMPTY,
    SYMBOL_PLAYER1,
    SYMBOL_PLAYER2,
)

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


class Board:
    def __init__(self, grid: Optional[np.ndarray] = None) -> None:
        if grid is not None:
            self.grid = grid.copy()
        else:
            self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=np.int8)

    def is_valid_location(self, col: int) -> bool:
        """Check if dropping a piece into column `col` is legal."""
        return 0 <= col < COLUMN_COUNT and self.grid[ROW_COUNT - 1, col] == EMPTY

    def get_valid_locations(self) -> list[int]:
      return [c for c in range(COLUMN_COUNT) if self.grid[ROW_COUNT - 1, c] == EMPTY]

    def get_next_open_row(self, col: int) -> Optional[int]:
        for r in range(ROW_COUNT):
            if self.grid[r, col] == EMPTY:
                return r
        return None

    def drop_piece(self, col: int, piece: int) -> int:
       row = self.get_next_open_row(col)
        if row is None:
            raise ValueError(f"Column {col} is full or invalid.")
        self.grid[row, col] = piece
        return row

    def undo_move(self, col: int, row: int) -> None:
      self.grid[row, col] = EMPTY

    def is_winning_move(self, piece: int) -> bool:
       for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if (
                    self.grid[r, c] == piece
                    and self.grid[r, c + 1] == piece
                    and self.grid[r, c + 2] == piece
                    and self.grid[r, c + 3] == piece
                ):
                    return True
     for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                    self.grid[r, c] == piece
                    and self.grid[r + 1, c] == piece
                    and self.grid[r + 2, c] == piece
                    and self.grid[r + 3, c] == piece
                ):
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                    self.grid[r, c] == piece
                    and self.grid[r + 1, c + 1] == piece
                    and self.grid[r + 2, c + 2] == piece
                    and self.grid[r + 3, c + 3] == piece
                ):
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                    self.grid[r, c] == piece
                    and self.grid[r - 1, c + 1] == piece
                    and self.grid[r - 2, c + 2] == piece
                    and self.grid[r - 3, c + 3] == piece
                ):
                    return True

        return False

    def is_terminal(self) -> tuple[bool, Optional[int]]:
       
        if self.is_winning_move(PLAYER_PIECE):
            return True, PLAYER_PIECE
        if self.is_winning_move(AI_PIECE):
            return True, AI_PIECE
        if len(self.get_valid_locations()) == 0:
            return True, None  # Draw
        return False, None

    def clone(self) -> Board:
   
        return Board(self.grid)

    def render(self, use_color: bool = True) -> str:
      
        sep = "+---" * COLUMN_COUNT + "+"
        lines = [sep]

        for r in range(ROW_COUNT - 1, -1, -1):
            row_str = "|"
            for c in range(COLUMN_COUNT):
                val = self.grid[r, c]
                if val == PLAYER_PIECE:
                    symbol = SYMBOL_PLAYER1
                    if use_color and HAS_COLORAMA:
                        symbol = f"{Fore.YELLOW}{Style.BRIGHT}{symbol}{Style.RESET_ALL}"
                elif val == AI_PIECE:
                    symbol = SYMBOL_PLAYER2
                    if use_color and HAS_COLORAMA:
                        symbol = f"{Fore.RED}{Style.BRIGHT}{symbol}{Style.RESET_ALL}"
                else:
                    symbol = SYMBOL_EMPTY
                row_str += f" {symbol} |"
            lines.append(row_str)
            lines.append(sep)

        col_headers = "  " + "   ".join(str(c + 1) for c in range(COLUMN_COUNT))
        lines.append(col_headers)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.render(use_color=False)

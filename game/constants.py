"""Game constants and configuration for Connect Four."""

# Board dimensions
ROW_COUNT: int = 6
COLUMN_COUNT: int = 7
WINDOW_LENGTH: int = 4

# Piece representations
EMPTY: int = 0
PLAYER_PIECE: int = 1  # Player 1 (Human or Yellow)
AI_PIECE: int = 2      # Player 2 (AI or Red)

# Bulletproof ASCII symbols for Windows & universal console compatibility
SYMBOL_EMPTY: str = "."
SYMBOL_PLAYER1: str = "O"
SYMBOL_PLAYER2: str = "X"

# Column order prioritizing the center for optimal alpha-beta search cutoffs
# Center column (col 3) is part of 13 possible 4-in-a-row winning alignments.
OPTIMAL_COLUMN_ORDER: list[int] = [3, 2, 4, 1, 5, 0, 6]

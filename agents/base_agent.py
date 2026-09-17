"""Abstract Base Class for Connect Four Agents."""
from abc import ABC, abstractmethod
from game.board import Board


class Agent(ABC):
    """Base interface that all Connect Four AI/Human players must implement."""

    def __init__(self, name: str, piece: int) -> None:
        self.name = name
        self.piece = piece

    @property
    def opponent_piece(self) -> int:
        """Return the piece constant of the adversary."""
        return 1 if self.piece == 2 else 2

    @abstractmethod
    def get_move(self, board: Board) -> int:
        """
        Evaluate the current board state and return the chosen column (0 to 6).
        """
        pass

    def __str__(self) -> str:
        return f"{self.name} (Piece: {'O' if self.piece == 1 else 'X'})"

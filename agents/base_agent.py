
from abc import ABC, abstractmethod
from game.board import Board


class Agent(ABC):
 
    def __init__(self, name: str, piece: int) -> None:
        self.name = name
        self.piece = piece

    @property
    def opponent_piece(self) -> int:
      
        return 1 if self.piece == 2 else 2

    @abstractmethod
    def get_move(self, board: Board) -> int:
        pass

    def __str__(self) -> str:
        return f"{self.name} (Piece: {'O' if self.piece == 1 else 'X'})"

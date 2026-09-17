
import random
from agents.base_agent import Agent
from game.board import Board


class RandomAgent(Agent):
  

    def __init__(self, name: str = "Random Baseline", piece: int = 1) -> None:
        super().__init__(name, piece)

    def get_move(self, board: Board) -> int:
        valid_locations = board.get_valid_locations()
        if not valid_locations:
            raise RuntimeError("No valid moves available.")
        return random.choice(valid_locations)

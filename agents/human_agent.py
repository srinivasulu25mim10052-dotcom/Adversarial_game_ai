"""Human Agent for interactive terminal play."""
from agents.base_agent import Agent
from game.board import Board
from game.constants import COLUMN_COUNT


class HumanAgent(Agent):
    """Prompts human player for input via console."""

    def __init__(self, name: str = "Human Player", piece: int = 1) -> None:
        super().__init__(name, piece)

    def get_move(self, board: Board) -> int:
        valid_locations = board.get_valid_locations()
        while True:
            try:
                user_input = input(f"[{self.name}] Enter column (1-{COLUMN_COUNT}): ").strip()
                if user_input.lower() in ["q", "quit", "exit"]:
                    print("Game aborted by user.")
                    exit(0)
                col_1indexed = int(user_input)
                col = col_1indexed - 1
                if col in valid_locations:
                    return col
                else:
                    if 0 <= col < COLUMN_COUNT:
                        print(f"Column {col_1indexed} is full! Choose another column.")
                    else:
                        print(f"Invalid column! Must be between 1 and {COLUMN_COUNT}.")
            except ValueError:
                print(f"Invalid input! Please enter an integer between 1 and {COLUMN_COUNT}.")

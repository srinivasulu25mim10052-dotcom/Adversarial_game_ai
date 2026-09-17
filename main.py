
import sys
import time
from game.board import Board
from game.constants import (
    PLAYER_PIECE,
    AI_PIECE,
)
from agents.human_agent import HumanAgent
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent
from agents.base_agent import Agent
from benchmark import run_search_comparison, run_tournament


def print_banner() -> None:
    print(r"""
============================================================
       CONNECT FOUR : CLASSICAL AI & ADVERSARIAL SEARCH     
============================================================
    Algorithms: Minimax with Alpha-Beta Pruning & MCTS
    Piece representations: [O] Player 1  |  [X] Player 2
============================================================
""")


def play_terminal_game(player1: Agent, player2: Agent) -> None:
   
    board = Board()
    current_agent, waiting_agent = player1, player2

    print(f"\nMatch Start: {player1.name} (O) vs {player2.name} (X)")
    print("=" * 60)
    print(board.render(use_color=True))

    turn = 1
    while True:
        print(f"\n--- Turn {turn}: {current_agent.name} ({'O' if current_agent.piece == 1 else 'X'})'s turn ---")

        start_time = time.perf_counter()
        chosen_col = current_agent.get_move(board)
        elapsed = time.perf_counter() - start_time

        row = board.drop_piece(chosen_col, current_agent.piece)

       
        telemetry = f"placed piece in column {chosen_col + 1} (took {elapsed:.3f}s)"
        if isinstance(current_agent, MinimaxAgent):
            telemetry += f" | {current_agent.nodes_visited} nodes visited | {current_agent.pruning_cutoffs} cutoffs"
        print(f"[{current_agent.name}] {telemetry}")

        print(board.render(use_color=True))

        is_term, winner = board.is_terminal()
        if is_term:
            print("\n" + "=" * 60)
            if winner == PLAYER_PIECE:
                print(f"*** GAME OVER: {player1.name} (O) WINS! ***")
            elif winner == AI_PIECE:
                print(f"*** GAME OVER: {player2.name} (X) WINS! ***")
            else:
                print("*** GAME OVER: DRAW (Board Full)! ***")
            print("=" * 60)
            break

        current_agent, waiting_agent = waiting_agent, current_agent
        turn += 1


def main_menu() -> None:
    while True:
        print_banner()
        print("1. [RECOMMENDED] Launch Graphical Window (Pygame GUI)")
        print("2. Play Human vs. Minimax AI (Terminal / Console)")
        print("3. Play Human vs. Monte Carlo Tree Search (MCTS) AI (Terminal)")
        print("4. Watch AI vs. AI Exhibition Match (Alpha-Beta vs. MCTS)")
        print("5. Run Search Performance Benchmark (Minimax vs. Alpha-Beta)")
        print("6. Run Tournament Evaluation")
        print("7. Exit")
        print("-" * 60)

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            print("\nLaunching Graphical Window...")
            try:
                import gui_game
                gui_game.run_gui()
            except Exception as e:
                print(f"Error launching GUI: {e}")

        elif choice == "2":
            print("\nSelect Minimax Difficulty:")
            print("  1. Easy   (Depth 2 - Fast, tactical)")
            print("  2. Medium (Depth 4 - Solid strategy, looks 4 moves ahead)")
            print("  3. Hard   (Depth 6 - Near unbeatable tactical foresight)")
            diff_choice = input("Select difficulty (1-3, default 2): ").strip() or "2"
            depth = 2 if diff_choice == "1" else (6 if diff_choice == "3" else 4)

            p1 = HumanAgent("Human", piece=PLAYER_PIECE)
            p2 = MinimaxAgent(f"Minimax (Depth {depth})", piece=AI_PIECE, depth=depth)
            play_terminal_game(p1, p2)

        elif choice == "3":
            p1 = HumanAgent("Human", piece=PLAYER_PIECE)
            p2 = MCTSAgent("MCTS AI (400 rollouts)", piece=AI_PIECE, iterations=400)
            play_terminal_game(p1, p2)

        elif choice == "4":
            print("\nStarting AI Exhibition: Minimax (Depth 4) vs MCTS (200 rollouts)...")
            p1 = MinimaxAgent("Alpha-Beta (Depth 4)", piece=PLAYER_PIECE, depth=4)
            p2 = MCTSAgent("MCTS (200 rollouts)", piece=AI_PIECE, iterations=200)
            play_terminal_game(p1, p2)

        elif choice == "5":
            run_search_comparison()

        elif choice == "6":
            print("\nConfiguring Tournament...")
            p1 = MinimaxAgent("Alpha-Beta (Depth 4)", depth=4)
            p2 = MCTSAgent("MCTS (150 rollouts)", iterations=150)
            run_tournament(p1, p2, rounds=2)

        elif choice in ["7", "q", "quit", "exit"]:
            print("Thank you for playing! Goodbye.")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    main_menu()

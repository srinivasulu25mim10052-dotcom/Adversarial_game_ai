"""
Adversarial Search Benchmark and Tournament Evaluation.
Empirically demonstrates:
1. Pure Minimax vs. Alpha-Beta Pruning vs. Move Ordering node counts and runtimes.
2. Head-to-head match win-rates between agents (Minimax, MCTS, Random).
"""
import time
from game.board import Board
from game.constants import PLAYER_PIECE, AI_PIECE
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent
from agents.base_agent import Agent


def run_search_comparison() -> None:
    """Compare search performance across depths and algorithm variants."""
    print("=" * 80)
    print("SEARCH PERFORMANCE BENCHMARK: MINIMAX VS ALPHA-BETA VS MOVE ORDERING")
    print("=" * 80)

    # Set up a representative mid-game board position
    board = Board()
    board.drop_piece(3, PLAYER_PIECE)
    board.drop_piece(3, AI_PIECE)
    board.drop_piece(2, PLAYER_PIECE)
    board.drop_piece(4, AI_PIECE)
    board.drop_piece(1, PLAYER_PIECE)
    board.drop_piece(5, AI_PIECE)

    header = f"{'Depth':<6} | {'Algorithm':<28} | {'Nodes':<10} | {'Cutoffs':<8} | {'Time (ms)':<10} | {'Node Reduction':<14}"
    print(header)
    print("-" * len(header))

    for depth in range(1, 6):
        # 1. Pure Minimax (no pruning)
        pure = MinimaxAgent(depth=depth, use_pruning=False, order_moves=False)
        t0 = time.perf_counter()
        move_pure = pure.get_move(board)
        t_pure = (time.perf_counter() - t0) * 1000

        # 2. Alpha-Beta without move ordering
        ab = MinimaxAgent(depth=depth, use_pruning=True, order_moves=False)
        t0 = time.perf_counter()
        move_ab = ab.get_move(board)
        t_ab = (time.perf_counter() - t0) * 1000

        # 3. Alpha-Beta with center move ordering
        ab_opt = MinimaxAgent(depth=depth, use_pruning=True, order_moves=True)
        t0 = time.perf_counter()
        move_opt = ab_opt.get_move(board)
        t_opt = (time.perf_counter() - t0) * 1000

        red_ab = ((pure.nodes_visited - ab.nodes_visited) / pure.nodes_visited) * 100
        red_opt = ((pure.nodes_visited - ab_opt.nodes_visited) / pure.nodes_visited) * 100

        print(f"{depth:<6} | {'Pure Minimax':<28} | {pure.nodes_visited:<10} | {'-':<8} | {t_pure:>9.2f} | {'Baseline':<14}")
        print(f"{'':<6} | {'Alpha-Beta (Unordered)':<28} | {ab.nodes_visited:<10} | {ab.pruning_cutoffs:<8} | {t_ab:>9.2f} | {f'{red_ab:.1f}%':<14}")
        print(f"{'':<6} | {'Alpha-Beta + Move Ordering':<28} | {ab_opt.nodes_visited:<10} | {ab_opt.pruning_cutoffs:<8} | {t_opt:>9.2f} | {f'{red_opt:.1f}%':<14}")
        print("-" * len(header))


def play_match(agent1: Agent, agent2: Agent, verbose: bool = False) -> int | None:
    """
    Simulate a single match between two agents.
    Returns winning piece (1 or 2) or None if draw.
    """
    board = Board()
    current_agent, other_agent = agent1, agent2

    while True:
        move = current_agent.get_move(board)
        board.drop_piece(move, current_agent.piece)

        if verbose:
            print(f"\n{current_agent.name} played column {move + 1}:")
            print(board.render(use_color=False))

        is_term, winner = board.is_terminal()
        if is_term:
            return winner

        current_agent, other_agent = other_agent, current_agent


def run_tournament(agent1: Agent, agent2: Agent, rounds: int = 4) -> None:
    """Run a series of matches alternating starting player."""
    print("=" * 80)
    print(f"TOURNAMENT: {agent1.name} vs {agent2.name} ({rounds} games)")
    print("=" * 80)

    wins_a1 = 0
    wins_a2 = 0
    draws = 0

    for i in range(rounds):
        # Alternate who plays first (Piece 1 goes first)
        if i % 2 == 0:
            a1 = agent1
            a1.piece = PLAYER_PIECE
            a2 = agent2
            a2.piece = AI_PIECE
            first_name = a1.name
            winner = play_match(a1, a2)
        else:
            a2 = agent2
            a2.piece = PLAYER_PIECE
            a1 = agent1
            a1.piece = AI_PIECE
            first_name = a2.name
            winner = play_match(a2, a1)

        result_str = "Draw"
        if winner == a1.piece:
            wins_a1 += 1
            result_str = f"{a1.name} Won"
        elif winner == a2.piece:
            wins_a2 += 1
            result_str = f"{a2.name} Won"
        else:
            draws += 1

        print(f"Game {i+1:02d} | First Move: {first_name:<20} | Result: {result_str}")

    print("-" * 80)
    print(f"Final Score: {agent1.name}: {wins_a1} | {agent2.name}: {wins_a2} | Draws: {draws}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_search_comparison()
    print("\nRunning Agent Tournament...")
    run_tournament(
        agent1=MinimaxAgent("Alpha-Beta (Depth 4)", depth=4),
        agent2=RandomAgent("Random Baseline"),
        rounds=4,
    )

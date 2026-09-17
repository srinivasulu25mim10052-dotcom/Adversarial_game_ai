
import sys
import math
import pygame

from game.board import Board
from game.constants import (
    ROW_COUNT,
    COLUMN_COUNT,
    PLAYER_PIECE,
    AI_PIECE,
)
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent


SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 8)
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)


COLOR_BG = (18, 22, 34)
COLOR_BOARD = (30, 85, 185)
COLOR_EMPTY = (26, 32, 48)
COLOR_PLAYER = (255, 210, 30)       
COLOR_AI = (235, 60, 60)           
COLOR_TEXT = (245, 245, 250)
COLOR_PANEL = (25, 30, 45)
COLOR_WIN_HIGHLIGHT = (50, 205, 50)


def draw_board(screen: pygame.Surface, board: Board, font_status: pygame.font.Font, status_msg: str, sub_msg: str) -> None:

    screen.fill(COLOR_BG)

   
    top_panel = pygame.Rect(0, 0, WIDTH, SQUARE_SIZE)
    pygame.draw.rect(screen, COLOR_PANEL, top_panel)
    pygame.draw.line(screen, (50, 60, 80), (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 2)

    status_surf = font_status.render(status_msg, True, COLOR_TEXT)
    screen.blit(status_surf, (20, 16))

    font_sub = pygame.font.SysFont("segoeui", 18)
    sub_surf = font_sub.render(sub_msg, True, (170, 180, 200))
    screen.blit(sub_surf, (20, 56))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
          
            rect = pygame.Rect(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, COLOR_BOARD, rect)

            
            center_x = int(c * SQUARE_SIZE + SQUARE_SIZE / 2)
            center_y = int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)

           
            grid_row = (ROW_COUNT - 1) - r
            piece = board.grid[grid_row, c]

            if piece == PLAYER_PIECE:
                pygame.draw.circle(screen, COLOR_PLAYER, (center_x, center_y), RADIUS)
                pygame.draw.circle(screen, (200, 160, 20), (center_x, center_y), RADIUS, 3)
            elif piece == AI_PIECE:
                pygame.draw.circle(screen, COLOR_AI, (center_x, center_y), RADIUS)
                pygame.draw.circle(screen, (180, 30, 30), (center_x, center_y), RADIUS, 3)
            else:
                pygame.draw.circle(screen, COLOR_EMPTY, (center_x, center_y), RADIUS)
                pygame.draw.circle(screen, (20, 25, 38), (center_x, center_y), RADIUS, 2)

    pygame.display.update()


def run_gui() -> None:
    """Main Pygame execution loop."""
    pygame.init()
    pygame.display.set_caption("Connect Four AI - Adversarial Search (Minimax)")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    font_status = pygame.font.SysFont("segoeui", 26, bold=True)

    difficulty_levels = {
        pygame.K_1: (2, "Easy (Depth 2)"),
        pygame.K_2: (4, "Medium (Depth 4)"),
        pygame.K_3: (6, "Hard (Depth 6)"),
    }
    current_depth = 4
    current_diff_name = "Medium (Depth 4)"

    board = Board()
    ai_agent = MinimaxAgent(f"Minimax ({current_diff_name})", piece=AI_PIECE, depth=current_depth)

    game_over = False
    winner_text = ""
    status_msg = "Your Turn (Yellow)"
    sub_msg = f"AI: {current_diff_name} | Keys [1]=Easy [2]=Med [3]=Hard | [R]=Restart"

    draw_board(screen, board, font_status, status_msg, sub_msg)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key in difficulty_levels:
                    current_depth, current_diff_name = difficulty_levels[event.key]
                    ai_agent = MinimaxAgent(f"Minimax ({current_diff_name})", piece=AI_PIECE, depth=current_depth)
                    sub_msg = f"Difficulty changed to {current_diff_name}! [R]=Restart"
                    draw_board(screen, board, font_status, status_msg, sub_msg)

                elif event.key == pygame.K_r:
            
                    board = Board()
                    game_over = False
                    status_msg = "Your Turn (Yellow)"
                    sub_msg = f"AI: {current_diff_name} | Keys [1]=Easy [2]=Med [3]=Hard | [R]=Restart"
                    draw_board(screen, board, font_status, status_msg, sub_msg)

            elif event.type == pygame.MOUSEMOTION:
                if not game_over:
                    posx = event.pos[0]
             
                    top_panel = pygame.Rect(0, 0, WIDTH, SQUARE_SIZE)
                    pygame.draw.rect(screen, COLOR_PANEL, top_panel)
                    pygame.draw.line(screen, (50, 60, 80), (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 2)

                    status_surf = font_status.render(status_msg, True, COLOR_TEXT)
                    screen.blit(status_surf, (20, 16))

                    font_sub = pygame.font.SysFont("segoeui", 18)
                    sub_surf = font_sub.render(sub_msg, True, (170, 180, 200))
                    screen.blit(sub_surf, (20, 56))

                    hover_col = int(math.floor(posx / SQUARE_SIZE))
                    if 0 <= hover_col < COLUMN_COUNT and board.is_valid_location(hover_col):
                        hover_center_x = int(hover_col * SQUARE_SIZE + SQUARE_SIZE / 2)
                        pygame.draw.circle(screen, COLOR_PLAYER, (hover_center_x, SQUARE_SIZE // 2), RADIUS - 4)

                    pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    board = Board()
                    game_over = False
                    status_msg = "Your Turn (Yellow)"
                    sub_msg = f"AI: {current_diff_name} | Keys [1]=Easy [2]=Med [3]=Hard | [R]=Restart"
                    draw_board(screen, board, font_status, status_msg, sub_msg)
                    continue

                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if board.is_valid_location(col):
                       board.drop_piece(col, PLAYER_PIECE)
                    is_term, winner = board.is_terminal()

                    if is_term:
                        game_over = True
                        if winner == PLAYER_PIECE:
                            status_msg = "VICTORY! You Beat the AI! 🎉"
                        else:
                            status_msg = "GAME OVER: Draw! 🤝"
                        sub_msg = "Click anywhere or press [R] to Play Again"
                        draw_board(screen, board, font_status, status_msg, sub_msg)
                        continue

                    status_msg = f"AI Thinking... ({current_diff_name})"
                    sub_msg = "Running Minimax with Alpha-Beta Pruning..."
                    draw_board(screen, board, font_status, status_msg, sub_msg)
                    pygame.event.pump()

                  
                    ai_col = ai_agent.get_move(board)
                    board.drop_piece(ai_col, AI_PIECE)

                    telemetry_info = (
                        f"AI played Col {ai_col + 1} ({ai_agent.last_search_time:.3f}s) | "
                        f"{ai_agent.nodes_visited} nodes | {ai_agent.pruning_cutoffs} cutoffs"
                    )

                    is_term, winner = board.is_terminal()
                    if is_term:
                        game_over = True
                        if winner == AI_PIECE:
                            status_msg = "AI WINS! 🤖"
                        else:
                            status_msg = "GAME OVER: Draw! 🤝"
                        sub_msg = f"{telemetry_info} | Click to Restart"
                    else:
                        status_msg = "Your Turn (Yellow)"
                        sub_msg = telemetry_info

                    draw_board(screen, board, font_status, status_msg, sub_msg)

        clock.tick(60)


if __name__ == "__main__":
    run_gui()

"""
Play as Victor in an interactive zero-knowledge proof of a Sudoku solution.

See the argparse description for more.

The inspiration for this game was another interactive Sudoku prover: https://manishearth.github.io/sudoku-zkp/zkp.html
"""

import argparse
import logging
import random

import pygame
import sys
from typing import Tuple
from local.sudoku import Board
from local.graph import Mapping

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (50, 205, 50)
BLUE = (0, 0, 255)


def draw_grid():
    """
    Draw the Sudoku grid (without values).
    """
    # Columns
    for x in range(board_x_min, board_x_max, cell_visual_width):
        pygame.draw.line(window, BLACK, (x, board_y_min), (x, board_y_max))
    # Rows
    for y in range(board_y_min, board_y_max, cell_visual_width):
        pygame.draw.line(window, BLACK, (board_x_min, y), (board_x_max, y))
    # Boxes
    for x in range(board_x_min, board_x_max, cell_visual_width * dim):
        pygame.draw.line(window, BLACK, (x, board_y_min), (x, board_y_max), width=3)
    for y in range(board_y_min, board_y_max, cell_visual_width * dim):
        pygame.draw.line(window, BLACK, (board_x_min, y), (board_x_max, y), width=3)


def draw_public_solution():
    """
    Draw the value of the public solution.
    """
    for row in range(dim_sq):
        for col in range(dim_sq):
            value = public_solution[row][col]
            if value != 0:
                cell_text = font.render(str(value), True, BLACK)
                cell_x_min = board_x_min + col * cell_visual_width
                cell_y_min = board_y_min + row * cell_visual_width
                cell_rect = cell_text.get_rect(center=(cell_x_min + cell_visual_width // 2, cell_y_min + cell_visual_width // 2))
                window.blit(cell_text, cell_rect)


def inside_board(x: int, y: int) -> bool:
    """
    Check whether the coordinates are inside the board.

    :param x: x coordinate
    :param y: y coordinate
    :return: is inside the board
    """
    return board_x_min <= x < board_x_max and board_y_min <= y < board_y_max


def inside_accept(x: int, y: int) -> bool:
    """
    Check whether the coordinates are inside the accept button.

    :param x: x coordinate
    :param y: y coordinate
    :return: is inside the accept button
    """
    return accept_x_min <= x < accept_x_max and accept_y_min <= y < accept_y_max


def inside_reject(x: int, y: int) -> bool:
    """
    Check whether the coordinates are inside the accept button

    :param x: x coordinate
    :param y: y coordinate
    :return: is inside the reject button
    """
    return reject_x_min <= x < reject_x_max and reject_y_min <= y < reject_y_max


def get_selection(x: int, y: int, selection_mode: str) -> Tuple[int, int]:
    """
    Return the area that the player selected.

    :param x: selected x coordinate
    :param y: selected y coordinate
    :param selection_mode: row, column, box, preset
    :return: selected row and selected column
    """
    row, col = (y - board_y_min) // cell_visual_width, (x - board_x_min) // cell_visual_width

    if selection_mode == "row" or selection_mode == "column":
        return row, col
    elif selection_mode == "box":
        box_row = (row // dim) * dim
        box_col = (col // dim) * dim
        return box_row, box_col
    elif selection_mode == "presets":
        return 0, 0  # Default
    else:
        raise ValueError(f"Unknown selection mode: {selection_mode}")


def highlight_selection(row: int, col: int, selection_mode: str):
    """
    Highlight the area that the player selected.

    :param row: selected row
    :param col: selected column
    :param selection_mode: row, column, box, presets
    """
    if selection_mode == "row":
        x0 = board_x_min
        y0 = board_y_min + row * cell_visual_width
        x_offset = board_visual_width
        y_offset = cell_visual_width
    elif selection_mode == "column":
        x0 = board_x_min + col * cell_visual_width
        y0 = board_y_min
        x_offset = cell_visual_width
        y_offset = board_visual_width
    elif selection_mode == "box":
        start_row, start_col = (row // dim) * dim, (col // dim) * dim
        x0 = board_x_min + start_col * cell_visual_width
        y0 = board_y_min + start_row * cell_visual_width
        x_offset = cell_visual_width * dim
        y_offset = cell_visual_width * dim
    elif selection_mode == "presets":
        x0 = board_x_min
        y0 = board_y_min
        x_offset = board_visual_width
        y_offset = board_visual_width
    else:
        raise ValueError(f"Unknown selection mode: {selection_mode}")

    pygame.draw.rect(window, RED, (x0, y0, x_offset, y_offset))


def reveal_partial_solution(row: int, col: int, selection_mode: str):
    """
    Update the public solution based on the area that the player selected.

    The values in the secret solution are randomly shuffled (permuted).

    The selected area is revealed while everything else is hidden.

    :param col: selected column
    :param row: selected row
    :param selection_mode: row, column, box, presents
    """
    global public_solution
    secret_mapping = Mapping.shuffle_list(list(range(1, dim_sq + 1)))
    logging.debug(f"Secret mapping {secret_mapping}")
    public_solution = Board.blank(dim)

    if selection_mode == "row":
        for col in range(dim_sq):
            public_solution[row][col] = secret_mapping[secret_solution[row][col]]
    elif selection_mode == "column":
        for row in range(dim_sq):
            public_solution[row][col] = secret_mapping[secret_solution[row][col]]
    elif selection_mode == "box":
        for row_offset in range(dim):
            for col_offset in range(dim):
                public_solution[row + row_offset][col + col_offset] = secret_mapping[secret_solution[row + row_offset][col + col_offset]]
    elif selection_mode == "presets":
        for row in range(dim_sq):
            for col in range(dim_sq):
                if public_presets[row][col] > 0:
                    public_solution[row][col] = secret_mapping[secret_solution[row][col]]


def verify_partial_solution(row: int, col: int, selection_mode: str) -> bool:
    """
    Verify that the revealed partial solution is valid.

    :param row: selected row
    :param col: selected column
    :param selection_mode: row, column, box, presents
    :return: partial solution is valid
    """
    if selection_mode == "row":
        columns = [public_solution[row][col] for col in range(dim_sq)]
        logging.info(f"Checking row {columns}")
        return public_solution.verify_area(columns)
    elif selection_mode == "column":
        rows = [public_solution[row][col] for row in range(dim_sq)]
        logging.info(f"Checking column {rows}")
        return public_solution.verify_area(rows)
    elif selection_mode == "box":
        box = [public_solution[row + row_offset][col + col_offset] for row_offset in range(dim) for col_offset in range(dim)]
        logging.info(f"Checking box {box}")
        return public_solution.verify_area(box)
    elif selection_mode == "presets":
        shuffled_values = [public_solution[row][col] for row in range(dim_sq) for col in range(dim_sq) if public_solution[row][col] > 0]
        return public_presets.verify_shuffling(iter(shuffled_values))
    else:
        raise ValueError(f"Unknown selection mode: {selection_mode}")


def player_wins(accept: bool) -> bool:
    """
    Check whether the player wins.

    The player wins by accepting a correct solution or by rejecting a false solution.
    The player loses otherwise (accepting a false solution or rejecting a correct one).

    :param accept: player accepted the solution
    :return: player wins
    """
    return accept == honest


def run_game():
    """
    Run the game loop until the player quits.

    Requires the global variables to be set beforehand for configuration.
    """
    round_number = 1
    selection_mode = "row"
    game_state = "playing"

    while True:
        window.fill(WHITE)
        x, y = pygame.mouse.get_pos()
        row, col = get_selection(x, y, selection_mode)

        for event in pygame.event.get():
            # Always allow player to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Disable other controls when game is over
            if game_state == "win" or game_state == "lose":
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selection_mode = "row"
                elif event.key == pygame.K_2:
                    selection_mode = "column"
                elif event.key == pygame.K_3:
                    selection_mode = "box"
                elif event.key == pygame.K_4:
                    selection_mode = "presets"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if inside_accept(x, y) or inside_reject(x, y):
                    if inside_accept(x, y):
                        accept = True
                    else:
                        accept = False

                    if player_wins(accept):
                        game_state = "win"
                    else:
                        game_state = "lose"
                elif inside_board(x, y):
                    reveal_partial_solution(row, col, selection_mode)

                    if not verify_partial_solution(row, col, selection_mode):
                        game_state = "win"
                    else:
                        round_number += 1

        if game_state == "win":
            text = font.render(f"You win! You took {round_number} rounds.", True, BLUE)
            text_rect = text.get_rect(center=(screen_x_max // 2, screen_y_max // 2))
            window.blit(text, text_rect)
        elif game_state == "lose":
            text = font.render(f"You lose! You took {round_number} rounds.", True, RED)
            text_rect = text.get_rect(center=(screen_x_max // 2, screen_y_max // 2))
            window.blit(text, text_rect)
        else:
            # Board
            if inside_board(x, y):
                highlight_selection(row, col, selection_mode)

            draw_grid()
            draw_public_solution()

            # Round text
            round_text = font.render(f"Round: {round_number}", True, BLACK)
            round_rect = round_text.get_rect(left=text_margin, centery=board_y_min // 2)
            window.blit(round_text, round_rect)

            # Accept button
            pygame.draw.rect(window, GREEN, (accept_x_min, accept_y_min, button_x_length, button_y_length))
            accept_text = font.render("Accept", True, BLACK)
            accept_rect = accept_text.get_rect(left=accept_x_min + text_margin, centery=board_y_min // 2)
            window.blit(accept_text, accept_rect)

            # Reject button
            pygame.draw.rect(window, RED, (reject_x_min, reject_y_min, button_x_length, button_y_length))
            reject_text = font.render("Reject", True, BLACK)
            reject_rect = reject_text.get_rect(left=reject_x_min + text_margin, centery=board_y_min // 2)
            window.blit(reject_text, reject_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interactive zero-knowledge proof of a Sudoku solution.",
        epilog="""
        Play the side of Victor.
        Does Peggy know a valid solution? Be warned, she might be lying!
        Check a few rows, columns, boxes or the presets to increase your confidence that she is honest (use keys 1 to 4 plus mouse).
        You win immediately if Peggy reveals an inconsistent solution.
        Accept or reject when you feel ready. Were you correct? How many rounds did you take?
        You win if you made the correct decision. Otherwise you lose.
        Try to use as few rounds as possible.
        """
    )
    parser.add_argument("--dim", type=int, default=3,
                        help="Base size of the Sudoku puzzle: number of cells alongside a box")
    parser.add_argument("--debug", action="store_true", help="Show debug information (secret information)")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Sudoku problem

    dim = args.dim
    dim_sq = dim ** 2

    honest = random.choice([True, False])
    secret_solution = Board.random(dim).solve()

    if not honest:
        secret_solution.falsify(1)

    public_presets = secret_solution.to_puzzle()
    public_solution = public_presets  # Presets stay constant while the (partial) solution keeps changing

    # Visual board

    cell_visual_width = 50
    board_visual_width = cell_visual_width * dim_sq

    board_x_min = 0
    board_x_max = board_x_min + board_visual_width
    board_y_min = 50
    board_y_max = board_y_min + board_visual_width

    screen_x_max = board_x_max
    screen_y_max = board_y_max

    # Visual buttons

    text_margin = 10
    button_x_length = 100
    button_y_length = 40

    accept_x_min = screen_x_max - button_x_length - text_margin - button_x_length - text_margin
    accept_y_min = board_y_min // 2 - button_y_length // 2
    accept_x_max = accept_x_min + button_x_length
    accept_y_max = accept_y_min + button_y_length

    reject_x_min = screen_x_max - button_x_length - text_margin
    reject_y_min = board_y_min // 2 - button_y_length // 2
    reject_x_max = reject_x_min + button_x_length
    reject_y_max = reject_y_min + button_y_length

    # Pygame initialization

    pygame.init()
    window = pygame.display.set_mode((screen_x_max, screen_y_max))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    run_game()

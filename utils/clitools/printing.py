"""
game_printing.py 
Author: Robert Pal
Updated: 2025-08-14

This module contains all game related display and print functions for Command Line Applications.
"""

import shutil
from itertools import chain
from time import sleep
from utils.clitools.console import clear_screen, delay_effect
from utils.game_options import GameOptions
from utils.strings import connect4_strings, other_strings, solitaire_strings, tictactoe_strings
from utils.square import Square
from typing import Union

# ==== For enhanced effects, like ASCII string centering and box display of game information ===
def surround_string(strings: list[str], border_symbol: str, offset: int = 0) -> list[str]:
    """
    Creates a bordered box display around any mulit-line text and centers it with padding around the text, which is used for scoreboards or other messages. 
    Border must use a string with no default setting. Offset is defaulted to 0 for minimum padding in the the box.
    """
    # Split each string from list on '\n' if it has one; otherwise, keep the string as a single element by wrapping it in a list.
    # Use itertools.chain.from_iterable to flatten the resulting list of lists into a single string, which is then wrapped in a list of strings, which
    # each line in the text is a single element in the list.
    string_list = list(chain.from_iterable(
        string.split("\n") if "\n" in string else [string] for string in strings)
        )
    # Find the longest line from string list and build a border using the border_symbol, padded by offset on both sides if not set to 0.
    border = border_symbol * (len(max(string_list, key=len)) + 2 * offset)
    # Make complete list with top border, centered line of text matching the border length, and bottom border
    output_list = [border, *[string.center(len(border)) for string in string_list], border]
    # Add side border_symbols to each line, join lines with newlines, and add spacing above and below for final list
    return ["\n" + "\n".join([border_symbol + string + border_symbol for string in output_list]) + "\n"]


def center_display_string(list_of_strings: list[str], terminal_width: int) -> str:
    """Centers a multi-line string of ASCII art from a list within the terminal width to adjust for difficult line spacing in passed string."""
    centered_lines = []
    for line in list_of_strings:
        centered_lines.append(line.center(terminal_width))
    return "\n".join(centered_lines)

# ==== Functions for general board creation and display ====
def board_translator(game_board: list[list[Union[int, str]]]) -> list[list[Square]]:
    """Converts raw board data from Tic Tac Toe or Connect4 into Square Enum values for command line dispaly using dictionary mapping of marker values."""
    marker_mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y}
    return [[marker_mapping[cell] for cell in row] for row in game_board]


def print_board(game_board: list[list[Union[int, str]]], game_name: str, delay_rate: float=0.000175) -> None:
    """Prints the game board using the Square strings with optional delay effect. Translate Board Object data of type string and int to string of Square Enum data type."""
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    
    translated_board = board_translator(game_board)
    
    if game_name == 'TicTacToe':
        delay_effect([create_board_tictactoe(game_board=translated_board, line=tictactoe_strings["boardline"])],
                     delay=delay_rate, word_flush=False) # Use default delay for Tic Tac Toe
    elif game_name == 'Connect4':
        delay_effect([create_board_connect4(game_board=translated_board, line=connect4_strings["boardline"])],
                     delay=0, word_flush=False) # No delay for Connect Four since it uses dropping effect
        print(connect4_strings["boardline"])
        print(connect4_strings["boardlabels"])

# ==== Functions for creating Tic Tac Toe Board for display ====
def create_row_tictactoe(row: list[list[Square]], border_symbol: str="*") -> str:
    """Returns a formatted string of a single board row of Tic Tac Toe with grid border lines for inside grid walls. Default symbol is '*'"""
    return "\n".join([
        border_symbol.join(line).center(shutil.get_terminal_size().columns - 1)
        for line in zip(*row)
    ])


def create_board_tictactoe(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the entire centred Tic Tac Toe board by building the board row by row."""
    return f"\n{line.center(shutil.get_terminal_size().columns - 1)}\n".join(
        [create_row_tictactoe([square.value for square in row]) for row in game_board])

# ==== Functions for creating Connect 4  Board for display ====
def create_row_connect4(row: list[list[Square]], border_symbol: str="|") -> str:
    """Returns a formatted string of a single board row for Connect 4 with grid border lines for inside grid walls. Default symbol is'|'"""
    return "\n".join([
        border_symbol.join(line)
        for line in zip(*row)
    ] )


def create_board_connect4(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the entire Connect 4 board for by building the board row by row."""
    return f"\n{line}\n".join(
        [create_row_connect4([square.value for square in row]) for row in game_board])

# ==== Functions for specific for Connect 4 board display ====
def print_board_dropping_effect(board_states: list[list[list[Union[int, str]]]], sleep_delay: float=0.075, top_spacing: int=3):
    """Prints the Connect 4 Board with animation that simulates a dropping effect. Sleep delay can control the speed of the dropping piece. Optional top spacing."""
    for board_state in board_states:
        print("\n" * top_spacing)
        print_board(board_state, "Connect4")
        sleep(sleep_delay)
        clear_screen()


def print_board_with_spacing(game_board: list[list[Union[int, str]]], top_spacing=3):
        """For printing the Connect 4 board with space on top and clear screen. Displays single use board state of current game."""
        clear_screen()
        print("\n" * top_spacing)
        print_board(game_board=game_board, game_name="Connect4")

# ==== Functions for game messaging ====
def print_winner_info(name: str, marker: str, win_type: str, win_index: int) -> None:
    """Displays the information of the winner of the game using the winner attributes."""
    if all(info is None for info in (name, marker, win_type)):
        draw_string = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"
        delay_effect(surround_string([draw_string], "#", 9), 0.00075, False)
    else:
        winner_string = f"\nWinner winner chicken dinner. {name} is the winner.\n{marker.upper()} wins in"
        win_type_dict = {
            "row": f"row {win_index + 1}.",
            "column": f"column {win_index + 1}.",
            "right_diagonal": "the right diagonal.",
            "left_diagonal": "the left diagonal."
        }
        winner_string = f"{winner_string} {win_type_dict[win_type]}\n"
        delay_effect(surround_string([winner_string], "#", 9), 0.00075, False)


def print_scoreboard(player_list: list[str], border_symbol: str="#") -> None:
    """Shows the player statistics for the game."""
    delay_effect(surround_string(player_list, border_symbol, 25), 0.00075, False)


def print_computer_thinking(name: str="Computer", time_delay: int=1.5) -> None:
    """Prints thinking message with time delay to simulate the computer thinking"""
    print(f"\n{name} is now thinking.")
    print()
    sleep(time_delay)


def print_game_over(winner_mark: str):
    """Displays a flashing end of game messages when a winner is found."""
    print()
    clear_screen()
    columns = shutil.get_terminal_size().columns
    for i in range(5):
        if i % 2 == 0:
            print(center_display_string(other_strings["gameover"], columns))
        else:
            print(center_display_string(other_strings[winner_mark], columns))
        # sys.stdout.flush()
        sleep(0.45)
        clear_screen()
        sleep(0.45)
    print()

# ==== Functions for menu printing and game start up welcome messaging ====
def print_menu_screen(delay: float=0.025):
    """Displays a menu of game options centered in the terminal screen. Allows for new games to be added to menu with Enums in the GameOptions."""
    clear_screen()
    columns, rows = shutil.get_terminal_size()
    # Dynamically allow for more game options using game_options ENUM, which stores the game options numerically via a string
    MENU_OPTIONS = {
        GameOptions.TIC_TAC_TOE.value: "Tic Tac Toe", # game_option "1"
        GameOptions.CONNECT_FOUR.value: "Connect 4",  # game_option "2"
        GameOptions.SOLITAIRE.value: "Solitaire"      # game_option "3"
    }
    # ==== For displaying properly indented game options ====
    menu_text = "Welcome to Simple Games.\n\n"
    for key, value in MENU_OPTIONS.items():
        menu_text += f"    {key}. {value}\n"
    horizontal_pos = (columns - len(max(menu_text.splitlines(), key=len))) // 2 # Centre left to right relative to the longest line in the menu_text (the first line)  
    vertical_pos = (rows - menu_text.count('\n') - 1) // 2 # Centre top to bottom relative to the total number of lines in te the menu_text
    print('\n' * vertical_pos, end='') # Start printing menu_text after adding the appropriate number of new lines as calculated in vertical_pos
    for line in menu_text.splitlines():
        print(' ' * horizontal_pos, end="") # Start printing menu_text after adding the appropriate number of spaces as calculated in horizontal_pos
        delay_effect([line], delay) # Use delay)_effect for typewriter printing effect


def print_start_game(game_name: str):
    """Prints the welcome message and introduction for each game."""
    if game_name not in {'TicTacToe', 'Connect4', 'Solitaire'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4' or 'Solitaire'.")
    if game_name == 'TicTacToe':
        string_dict = tictactoe_strings
    elif game_name == 'Connect4':
        string_dict = connect4_strings
    else:
        string_dict = solitaire_strings
    print(string_dict["welcome"])
    delay_effect([string_dict["intro"]])

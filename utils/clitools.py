"""
clitools.py 
Author: Robert Pal
Updated: 2025-08-01

This module contains helper functrions for Command Line Applications.
"""
import os
import shutil
from time import sleep
from itertools import chain
from utils.game_options import GameOptions
from utils.square import Square
from utils.strings import tictactoe_strings, connect4_strings, solitaire_strings, other_strings
from typing import Union, Optional

def clear_screen():
    """Clears all printed input on terminal screen for display purposes."""
    os.system('cls' if os.name == 'nt' else 'clear')

def delay_effect(strings: list[str], delay: float = 0.015, word_flush: bool = True) -> None:
    """Creates the effect of printing line by line or character by character."""
    # Used for testing to speed up output
    # if delay != 0:
    #     delay = 0  
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)

def print_menu_screen(delay: float=0.025):
    """Displays a menu of game options centered in the terminal screen. Allow for new games to be added dynamically."""
    clear_screen()
    # set_console_window_size(100, 40)
    columns, rows = os.get_terminal_size()

    MENU_OPTIONS = {
        GameOptions.TIC_TAC_TOE.value: "Tic Tac Toe",
        GameOptions.CONNECT_FOUR.value: "Connect 4",
        GameOptions.SOLITAIRE.value: "Solitaire"
    }

    # create menu options dynmically as more games are added
    menu_text = "Welcome to Simple Games.\n\n"
    for key, value in MENU_OPTIONS.items():
        menu_text += f"    {key}. {value}\n"

    horizontal_pos = (columns - len(max(menu_text.splitlines(), key=len))) // 2
    vertical_pos = (rows - menu_text.count('\n') - 1) // 2

    # centre the menu in the command line screen
    print('\n' * vertical_pos, end='')
    for line in menu_text.splitlines():
        print(' ' * horizontal_pos, end="")
        delay_effect([line], delay)

def menu_select(valid_selections):
    print()
    columns, _ = os.get_terminal_size()
    prompt = "Select the game you want to play: "
    error = "Please only select a game from the available options."

    horizontal_pos = (columns - len(prompt)) // 2
    blank_space = ' ' * horizontal_pos

    while True:
        print(blank_space + prompt, end="")
        choice = input().strip()

        if choice in valid_selections:
            break
        print('\n' + blank_space, end="")
        print(error)  
        print('\n' + blank_space, end="")
        sleep(1)
        clear_screen()
        print_menu_screen(delay=0)
        print()
    
    clear_screen()
    print('\n' * 15)
    print(blank_space + " " * 15 + "GAME LOADING")
    sleep(2)
    clear_screen()

    return choice

def set_console_window_size(width: float, height: float) -> None:
    """Sets the console window size to fit the board better for both Windows."""
    os.system('cls||clear')
    if os.name == 'nt':
        os.system(f'mode con: cols={width} lines={height}')
    else:
        os.system(f'printf "\033[8;{height};{width}t"')

def surround_string(strings: list[str], symbol: str, offset: int = 0) -> list[str]:
    """Creates a bordered display around text, used for scoreboards."""
    string_list = list(chain.from_iterable(
        string.split("\n") if "\n" in string else [string] for string in strings))
    border = symbol * (len(max(string_list, key=len)) + 2 * offset)
    output_list = [border, *[string.center(len(border)) for string in string_list], border]
    return ["\n" + "\n".join([symbol + string + symbol for string in output_list]) + "\n"]

def board_translator(game_board: list[list[Union[int, str]]]) -> list[list[Square]]:
    """Converts raw board data into Square enum values."""
    marker_mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y}
    return [[marker_mapping[cell] for cell in row] for row in game_board]

# Functions for creating Tic Tac Toe Board for display
def create_row_tictactoe(row: list[list[Square]]) -> str:
    """Returns a formatted string of a single board row."""
    return "\n".join([
        "*".join(line).center(os.get_terminal_size().columns - 1)
        for line in zip(*row)
    ])

def create_board_tictactoe(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the board."""
    return f"\n{line.center(os.get_terminal_size().columns - 1)}\n".join(
        [create_row_tictactoe([square.value for square in row]) for row in game_board])

# Functions for creating Connect 4  Board for display
def create_row_connect4(row: list[list[Square]]) -> str:
    """Returns a formatted string of a single board row."""
    return "\n".join([
        "|".join(line)
        for line in zip(*row)
    ] ) 

def create_board_connect4(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the board."""
    return f"\n{line}\n".join(
        [create_row_connect4([square.value for square in row]) for row in game_board])


def print_board(game_board: list[list[Union[int, str]]], game_name: str, delay_rate: float=0.000095) -> None:
    """Prints the game board with a slight delay effect."""
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    # translate string or int based board to Enum class full list board for printing
    translated_board = board_translator(game_board)
    if game_name == 'TicTacToe':
        delay_effect([create_board_tictactoe(game_board=translated_board, line=tictactoe_strings["boardline"])], 
                     delay=delay_rate, word_flush=False) # Use default delay for Tic Tac Toe
    elif game_name == 'Connect4':
        delay_effect([create_board_connect4(game_board=translated_board, line=connect4_strings["boardline"])], 
                     delay=0, word_flush=False) # No delay for Connect Four
        print(connect4_strings["boardline"])
        print(connect4_strings["boardlabels"])

def print_start_game(game_name: str):
    """Prints the welcome message and introduction."""
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

def center_display_string(list_of_strings: str, terminal_width: int) -> str:
    """Centers a multi-line string of ASCII art from a list within the terminal width."""
    centered_lines = []
    for line in list_of_strings:
        centered_lines.append(line.center(terminal_width))
        
    return "\n".join(centered_lines)


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

def get_player_names() -> tuple[str, str]:
    """Gets names for two players."""
    name_one = input("\nPlease enter the name for Player one or press enter: ")
    name_two = input("\nPlease enter the name for Player two or press enter: ")
    return name_one, name_two

def get_player_name() -> str:
    """Gets name for a single player."""
    return input("\nPlease enter the name for Player one or press enter: ")

def one_player() -> bool:
    """Sets the game to one or two players."""
    valid_input = {'1', '2', 'one', 'two'}
    while True:
        one_player_choice = input("How many players? One or two: ").lower()
        if one_player_choice in valid_input:
            return one_player_choice in ['1', 'one']
        print('\nOnly one or two players are allowed.\n')

def play_again() -> bool:
    """Gets valid input from user for and asks the user if they want to play again."""
    error_message = "\nInvalid input. Please enter 'yes' or 'no'."
    while True:
        play_again = input("\nWould you like to play again? Enter yes or no: ").lower().strip()
        if play_again in {'yes', 'y'}:
            return True
        elif play_again in {'no', 'n'}:
            delay_effect(["\nGame session complete.\n\nThanks for playing. See you in the next session.\n"])
            return False
        else:
            print(error_message)

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

def print_first_player(name: str) -> None:
    """Prints who plays first and their marker."""
    delay_effect([f'\n{name} plays first.'])
    input('\nPress Enter to start the game.')

def print_player_turn_prompt_tictactoe(name: str) -> None:
    """Prints the prompt for the player's turn."""
    delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])

def print_player_turn_prompt_connect4(name: str) -> None:
    """Prints the prompt for the player's turn."""
    delay_effect([f"\nIt is {name}'s turn. Select the column you want to drop your piece in.\n"])

def print_square_occupied_prompt(name: str) -> None:
    """Prints a prompt when the selected square is occupied."""
    print("\nThe square is already occupied. Select another square.")
    delay_effect([f"\nIt is {name}'s turn again. Select a free square.\n"])

def print_current_move(name: str, row: int, column: int) -> None:
    """Prints the last move made by the player."""
    delay_effect([
        f"\n{name} played the square in row {row + 1} and column {column + 1}.\n"
    ])

def print_scoreboard(player_list) -> None:
    """Shows the player statistics for the game."""
    delay_effect(
        surround_string([str(player) for player in player_list], "#", 25),
        0.00075, False
    )

def print_computer_thinking(name: str="Computer", time_delay: int=1.5) -> None:
    """Prints thinking message with time delay to simulate the computer thinking"""
    print(f"{name} is now thinking.")
    print()
    sleep(time_delay)

def prompt_int(value: str) -> int:
    """Gets a valid integer input (1-3) for row/column."""
    valid_input = {1, 2, 3}
    while True:
        try:
            input_value = int(input(f"Enter the {value}: "))
            if input_value in valid_input:
                return input_value - 1  # Needed for 0-based index
            print(f"\nYou must enter 1, 2, or 3 only for the {value}.\n")
        except ValueError:
            print("\nYou must enter a number. Try again.\n")

def prompt_move() -> tuple[int, int]:
    """Gets a valid row and column input from the player."""
    row = prompt_int('row')
    column = prompt_int('column')
    return row, column

def prompt_column_move():
    """Gets a valid column input from player."""
    valid_input = {i + 1 for i in range(7)}
    while True:
        try:
            input_value = int(input(f"Enter the column: "))
            if input_value in valid_input:
                return input_value - 1  # Needed for 0-based index
            print(f"\nYou must enter a free column from 1 to 7 only.\n")
        except ValueError:
            print("\nYou must enter a number. Try again.\n")
def select_klondike_draw_number():
    valid_input = ["1", "3"]
    while True:
        klondike_value = input("\nSelect the number of cards per draw: 1 or 3: ")
        if klondike_value in valid_input:
            if klondike_value == "1":
                print("\nYou are playing in easy mode with one card per draw.")
            else:
                print("\nYou are playing in hard mode with three cards per draw.")
            print(input("\nPress ENTER or RETRUN to start the game."))
            clear_screen()
            return int(klondike_value)
        else:
            print("Please type only 1 or 3.")

def select_difficulty_level(game_name: str) -> Optional[bool]:
    """Updates the difficulty level boolean when playing against the computer."""
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    if game_name == "TicTacToe":
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind, 2) Normal, 3) Impossible: "
    else:
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind or 2) Basic: "
    valid_input = ['1', 'easy', '2', 'intermediate', '3', 'hard']
    while True:
        level_of_difficulty = input(difficulty_choices).lower()
        if level_of_difficulty in valid_input[:2]:
            delay_effect(["\nYou are playing against the computer in easy mode."])
            return None
        elif level_of_difficulty in valid_input[2:4]:
            delay_effect(["\nYou are playing against the computer in intermediate mode." ])
            return False
        elif level_of_difficulty in valid_input[4:]:
            if game_name == "Connect4":
                print("\nThis option is not currently avaliable for Connect 4. Please select again")
            else:
                delay_effect(["\nYou are playing against the computer in hard mode."])
                return True
        else:
            print(
                "\nPlease select a valid option or press the corresponding number only.")
            
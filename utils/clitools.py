import os
from time import sleep
from itertools import chain
from utils.square import Square
from typing import Union, Optional

# Constants
WELCOME = "default"
INTRO = "default"
GAMEOVER = "go"
ONE = "one"
TWO = "two"

def set_console_window_size(width: float, height: float) -> None:
    """Sets the console window size to fit the board better."""
    os.system('cls||clear')
    if os.name == 'nt':
        os.system(f'mode con: cols={width} lines={height}')
    else:
        os.system(f'printf "\033[8;{height};{width}t"')

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('clear||cls')

def delay_effect(strings: list[str], delay: float = 0.025, word_flush: bool = True) -> None:
    """Creates the effect of printing characters or lines with a delay."""
    # if delay != 0:
    #     delay = 0  # Used for testing to speed up output
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)

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

# def create_row(row: list[list[Square]]) -> str:
#     """Returns a formatted string of a single board row."""
#     return "\n".join([
#         "*".join(line).center(os.get_terminal_size().columns - 1)
#         for line in zip(*row)
#     ])

# def create_board(game_board: list[list[Union[int, str]]], line: str) -> str:
#     """Returns a formatted string representation of the board."""
#     return f"\n{line.center(os.get_terminal_size().columns - 1)}\n".join(
#         [create_row([square.value for square in row]) for row in game_board])


def create_row(row: list[list[Square]]) -> str:
    """Returns a formatted string of a single board row with proper centering."""
    
    # Determine the width of the longest square in the row
    max_width = max(len(line) for line in zip(*row))

    # Ensure each square is consistently padded to match the max width in the row
    return "\n".join([
        "*".join(line).center(max_width)
        for line in zip(*row)
    ])
    # Center the row based on the terminal width
    # return row_str.center(os.get_terminal_size().columns - 1)

def create_board(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the board."""
    
    # Create all rows first, ensuring consistency
    board_rows = [create_row([square.value for square in row]) for row in game_board]
    # board_rows = [create_row(row) for row in game_board]
    
    # Get terminal width for centering
    terminal_width = os.get_terminal_size().columns - 1
    
    # Join rows with a centered separator
    return f"\n{line.center(terminal_width)}\n".join(board_rows)


def print_board(game_board: list[list[Union[int, str]]], line: str) -> None:
    """Prints the game board with a slight delay effect."""
    translated_board = board_translator(game_board)
    delay_effect([create_board(translated_board, line)], 0.00075, False)

def print_start_game(welcome: str, intro: str):
    """Prints the welcome message and introduction."""
    print(welcome)
    delay_effect([intro])

def print_game_over(gameover: str):
    """Displays a flashing 'Game Over' message."""
    print()
    clear_screen()
    for _ in range(5):
        print(gameover.center(os.get_terminal_size().columns - 1), end='\r')
        sleep(0.75)
        clear_screen()
        sleep(0.5)
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

def print_player_turn_prompt(name: str) -> None:
    """Prints the prompt for the player's turn."""
    delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])

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

def select_difficulty_level() -> Optional[bool]:
    """Updates the difficulty level boolean when playing against the computer."""
    valid_input = ['1', 'easy', '2', 'intermediate', '3', 'hard']
    while True:
        level_of_difficulty = input(
            "\nSelect the level of difficult for the AI: Easy, Intermediate or Hard: "
        ).lower()
        if level_of_difficulty in valid_input[:2]:
            delay_effect(
                ["\nYou are playing against the computer in easy mode."])
            return None
        elif level_of_difficulty in valid_input[2:4]:
            delay_effect([
                "\nYou are playing against the computer in intermediate mode."
            ])
            return False
        elif level_of_difficulty in valid_input[4:]:
            delay_effect(
                ["\nYou are playing against the computer in hard mode."])
            return True
        else:
            print(
                "\nThere is only easy, intermediate or hard mode.\nPlease select '1' for easy, '2' for "
                "intermediate or '3' for hard.")


# import os
# from time import sleep
# from itertools import chain
# from utils.square import Square
# from typing import Union

# class GameCLI:
#     WELCOME = "default"
#     INTRO = "default"
#     GAMEOVER = "go"
#     ONE = "one"
#     TWO = "two"

#     @staticmethod
#     def set_console_window_size(width: float, height: float) -> None:
#         """Sets the console window size to fit the board better."""
#         os.system('cls||clear')
#         if os.name == 'nt':
#             os.system(f'mode con: cols={width} lines={height}')
#         else:
#             os.system(f'printf "\033[8;{height};{width}t"')

#     @staticmethod
#     def clear_screen() -> None:
#         """Clears the terminal screen."""
#         os.system('clear||cls')

#     @staticmethod
#     def delay_effect(strings: list[str], delay: float = 0.025, word_flush: bool = True) -> None:
#         """Creates the effect of printing characters or lines with a delay."""
#         if delay != 0:
#             delay = 0  # Used for testing to speed up output
#         for string in strings:
#             for char in string:
#                 print(char, end='', flush=word_flush)
#                 sleep(delay)
#             print()
#             sleep(delay)

#     @staticmethod
#     def surround_string(strings: list[str], symbol: str, offset: int = 0) -> list[str]:
#         """Creates a bordered display around text, used for scoreboards."""
#         string_list = list(chain.from_iterable(
#             string.split("\n") if "\n" in string else [string] for string in strings))
#         border = symbol * (len(max(string_list, key=len)) + 2 * offset)
#         output_list = [border, *[string.center(len(border)) for string in string_list], border]
#         return ["\n" + "\n".join([symbol + string + symbol for string in output_list]) + "\n"]

#     @staticmethod
#     def board_translator(game_board: list[list[Union[int, str]]]) -> list[list[Square]]:
#         """Converts raw board data into Square enum values."""
#         marker_mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y}
#         return [[marker_mapping[cell] for cell in row] for row in game_board]

#     @staticmethod
#     def create_row(row: list[list[Square]]) -> str:
#         """Returns a formatted string of a single board row."""
#         return "\n".join([
#             "*".join(line).center(os.get_terminal_size().columns - 1)
#             for line in zip(*row)
#         ])

#     @staticmethod
#     def create_board(game_board: list[list[Union[int, str]]], line: str) -> str:
#         """Returns a formatted string representation of the board."""
#         return f"\n{line.center(os.get_terminal_size().columns - 1)}\n".join(
#             [GameCLI.create_row([square.value for square in row]) for row in game_board])

#     @staticmethod
#     def print_board(game_board: list[list[Union[int, str]]], line: str) -> None:
#         """Prints the game board with a slight delay effect."""
#         translated_board = GameCLI.board_translator(game_board)
#         GameCLI.delay_effect([GameCLI.create_board(translated_board, line)], 0.00075, False)

#     @staticmethod
#     def print_start_game():
#         """Prints the welcome message and introduction."""
#         print(cls.WELCOME)
#         GameCLI.delay_effect([GameCLI.INTRO])

#     @staticmethod
#     def print_game_over():
#         """Displays a flashing 'Game Over' message."""
#         print()
#         GameCLI.clear_screen()
#         for _ in range(5):
#             print(GameCLI.GAMEOVER.center(os.get_terminal_size().columns - 1), end='\r')
#             sleep(0.75)
#             GameCLI.clear_screen()
#             sleep(0.5)
#         print()

#     @staticmethod
#     def get_player_names() -> tuple[str, str]:
#         """Gets names for two players."""
#         name_one = input("\nPlease enter the name for Player one or press enter: ")
#         name_two = input("\nPlease enter the name for Player two or press enter: ")
#         return name_one, name_two

#     @staticmethod
#     def get_player_name() -> str:
#         """Gets name for a single player."""
#         return input("\nPlease enter the name for Player one or press enter: ")

#     @staticmethod
#     def one_player() -> bool:
#         """Sets the game to one or two players."""
#         valid_input = {'1', '2', 'one', 'two'}
#         while True:
#             one_player_choice = input("How many players? One or two: ").lower()
#             if one_player_choice in valid_input:
#                 return one_player_choice in ['1', 'one']
#             print('\nOnly one or two players are allowed.\n')

#     @staticmethod
#     def print_winner_info(name: str, marker: str, win_type: str, win_index: int) -> None:
#         """Displays the information of the winner of the game using the winner attributes."""
#         if all(info is None for info in (name, marker, win_type)):
#             draw_string = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"
#             GameCLI.delay_effect(GameCLI.surround_string([draw_string], "#", 9), 0.00075, False)
#         else:
#             winner_string = f"\nWinner winner chicken dinner. {name} is the winner.\n{marker.upper()} wins in"
#             win_type_dict = {
#                 "row": f"row {win_index + 1}.",
#                 "column": f"column {win_index + 1}.",
#                 "right_diagonal": "the right diagonal.",
#                 "left_diagonal": "the left diagonal."
#             }
#             winner_string = f"{winner_string} {win_type_dict[win_type]}\n"
#             GameCLI.delay_effect(GameCLI.surround_string([winner_string], "#", 9), 0.00075, False)

#     @staticmethod
#     def print_first_player(name: str) -> None:
#         """Prints who plays first and their marker."""
#         GameCLI.delay_effect([f'\n{name} plays first.'])
#         input('\nPress Enter to start the game.')

#     @staticmethod
#     def print_player_turn_prompt(name: str) -> None:
#         """Prints the prompt for the player's turn."""
#         GameCLI.delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])

#     @staticmethod
#     def print_square_occupied_prompt(name: str) -> None:
#         """Prints a prompt when the selected square is occupied."""
#         print("\nThe square is already occupied. Select another square.")
#         GameCLI.delay_effect([f"\nIt is {name}'s turn again. Select a free square.\n"])

#     @staticmethod
#     def print_current_move(name: str, row: int, column: int) -> None:
#         """Prints the last move made by the player."""
#         GameCLI.delay_effect([
#             f"\n{name} played the square in row {row + 1} and column {column + 1}.\n"
#         ])

#     @staticmethod
#     def print_scoreboard(player_list) -> None:
#         """Shows the player statistics for the game."""
#         GameCLI.delay_effect(
#             GameCLI.surround_string([str(player) for player in player_list], "#", 25),
#             0.00075, False
#         )

#     @staticmethod
#     def prompt_int(value: str) -> int:
#         """Gets a valid integer input (1-3) for row/column."""
#         valid_input = {1, 2, 3}
#         while True:
#             try:
#                 input_value = int(input(f"Enter the {value}: "))
#                 if input_value in valid_input:
#                     return input_value - 1  # Needed for 0-based index
#                 print(f"\nYou must enter 1, 2, or 3 only for the {value}.\n")
#             except ValueError:
#                 print("\nYou must enter a number. Try again.\n")

#     @staticmethod
#     def prompt_move() -> tuple[int, int]:
#         """Gets a valid row and column input from the player."""
#         row = GameCLI.prompt_int('row')
#         column = GameCLI.prompt_int('column')
#         return row, column

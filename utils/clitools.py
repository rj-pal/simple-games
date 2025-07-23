import os
from time import sleep
from itertools import chain
from utils.game_options import GameOptions
from utils.square import Square
from utils.strings import tictactoe_strings, connect4_strings, other_strings
from typing import Union, Optional


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# def delay_effect(lines, delay=0.025):
#     for line in lines:
#         for char in line:
#             print(char, end='', flush=True)
#             sleep(delay)
#         print()

def print_menu_screen(delay=0.025):
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
        delay_effect([error])  
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




# def print_menu_screen(delay=0.025):
#     clear_screen()
#     # Get terminal size
#     columns, rows = os.get_terminal_size()

#     # Text to print
#     menu_text = """Welcome to Simple Games.
    
#     1. Tic Tac Toe
#     2. Connect 4
#     3. Solitaire"""

#     # Calculate horizontal and vertical positions for getting the centre of the terminal 
#     horizontal_pos = (columns - len(max(menu_text.splitlines(), key=len))) // 2
#     vertical_pos = (rows - menu_text.count('\n') - 1) // 2

#     # Print empty lines to center the text vertically
#     for _ in range(vertical_pos):
#         print()

#     # Print the text, center it horizontally
#     for line in menu_text.splitlines():
#         print(' ' * horizontal_pos, end="")
#         delay_effect([line], delay)

# def menu_select(valid_selections):
#     print()
#     # Get terminal size
#     columns, _ = os.get_terminal_size()

#     # Text to display as the prompt
#     prompt = "Select the game you want to play: "
#     error = "Please only select a game from the available options." 
#     new_screen = "Press enter to select again."

#     # Calculate horizontal position and create blank space string
#     horizontal_pos = (columns - len(prompt)) // 2
#     blank_space = ' ' * horizontal_pos

#     # Print the prompt centered horizontally

#     print(blank_space + prompt, end="")
    
#     choice = input()

#     while choice not in valid_selections:
#         print()
#         print(blank_space, end="")
#         delay_effect([error])  
#         print()
#         print(blank_space, end="")
#         delay_effect([new_screen])
#         print(blank_space, end="")
#         print(input())
#         clear_screen()
#         print_menu_screen(delay=0)
#         print()
        
#         return menu_select(valid_selections)
    
#     clear_screen()
#     for _ in range(20):
#         print()
#     print(blank_space + " " * 15 + "GAME LOADING")
#     sleep(2)
#     clear_screen()

#     return choice


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
    if delay != 0:
        delay = 0  # Used for testing to speed up output
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

### Original Works for Tic Tac Toe
def create_row_tictactoe(row: list[list[Square]]) -> str:
    """Returns a formatted string of a single board row."""
    return "\n".join([
        "*".join(line).center(os.get_terminal_size().columns - 1)
        for line in zip(*row)
    ])
### Original Works for Tic Tac Toe
def create_board_tictactoe(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a formatted string representation of the board."""
    return f"\n{line.center(os.get_terminal_size().columns - 1)}\n".join(
        [create_row_tictactoe([square.value for square in row]) for row in game_board])

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

# ### TESTING
# def create_row(row: list[list[Square]]) -> str:
#     """Returns a formatted string of a single board row with proper centering."""
    
#     # Determine the width of the longest square in the row
#     max_width = max(len(line) for line in zip(*row))

#     # Ensure each square is consistently padded to match the max width in the row
#     return "\n".join([
#         "*".join(line).center(max_width)
#         for line in zip(*row)
#     ])
#     # Center the row based on the terminal width
#     # return row_str.center(os.get_terminal_size().columns - 1)

# ### TESTING
# def create_board(game_board: list[list[Union[int, str]]], line: str) -> str:
#     """Returns a formatted string representation of the board."""   
    
#     # Create all rows first, ensuring consistency
#     board_rows = [create_row([square.value for square in row]) for row in game_board]
#     # board_rows = [create_row(row) for row in game_board]
    
#     # Get terminal width for centering
#     terminal_width = os.get_terminal_size().columns - 1
    
#     # Join rows with a centered separator
#     return f"\n{line.center(terminal_width)}\n".join(board_rows)

def print_board_connect4(game_board: list[list[Union[int, str]]], line: str, labels: str) -> None:
    """Prints the game board with a slight delay effect."""
    translated_board = board_translator(game_board)
    delay_effect([create_board_connect4(translated_board, line)], 0, False)
    print(line)
    print(labels)

def print_board(game_board: list[list[Union[int, str]]], line: str) -> None:
    """Prints the game board with a slight delay effect."""
    translated_board = board_translator(game_board)
    delay_effect([create_board_tictactoe(translated_board, line)], 0.00075, False)

def print_board(game_board: list[list[Union[int, str]]], game_name: str) -> None:
    """Prints the game board with a slight delay effect."""
    translated_board = board_translator(game_board)
    if game_name == 'TicTacToe':
        delay_effect([create_board_tictactoe(translated_board, line=tictactoe_strings["boardline"])], 0.00075, False)
    elif game_name == 'Connect4':
        delay_effect([create_board_connect4(translated_board, line=connect4_strings["boardline"])], 0, False)
        print(connect4_strings["boardline"])
        print(connect4_strings["boardlabels"])
    # else:
    #     raise ValueError()

def print_start_game(game_type: str):
    """Prints the welcome message and introduction."""
    if game_type == 'TicTacToe':
        string_dict = tictactoe_strings
    elif game_type == 'Connect4':
        string_dict = connect4_strings
    # else:
    #     raise ValueError
    print(string_dict["welcome"])
    delay_effect([string_dict["intro"]])

# import shutil, sys

# def center_multiline_string(multiline_str: str, terminal_width: int) -> str:
#     """
#     Centers a multi-line string (like ASCII art) within the terminal width.
#     Each line of the art is centered relative to the widest line in the art,
#     and then the entire block is centered.
#     """
#     lines = multiline_str.strip().split('\n') # .strip() removes leading/trailing blank lines
    
#     # Find the maximum width of any line in the ASCII art
#     max_line_width = 0
#     for line in lines:
#         # We need to consider that the first line after .strip() might be empty if original had leading newline
#         if line.strip(): # Only consider non-empty lines for width calculation
#             max_line_width = max(max_line_width, len(line))
    
#     if max_line_width == 0: # Handle empty input string case
#         return ""

#     centered_lines = []
#     for line in lines:
#         # Center each line of the art relative to the max_line_width of the art itself
#         # This preserves the internal structure of the ASCII art
#         padded_line = line.ljust(max_line_width) # Pad shorter lines to max_line_width
        
#         # Now center this padded line within the terminal width
#         centered_lines.append(padded_line.center(terminal_width))
        
#     return "\n".join(centered_lines)


def print_game_over(winner_mark: str):
    """Displays a flashing 'Game Over' message."""
    print()
    clear_screen()
    # columns = shutil.get_terminal_size().columns
    for i in range(5):
        if i % 2 == 0:
            # centered_output = center_multiline_string(other_strings["gameover"], columns)
            # print(centered_output.center(columns), end='')
            print(other_strings["gameover"].center(os.get_terminal_size().columns - 1), end='\r')
        else:
            # centered_output = center_multiline_string(other_strings[winner_mark], columns)
            # print(centered_output.center(columns), end='')
            print(other_strings[winner_mark].center(os.get_terminal_size().columns - 1), end='\r')
        # sys.stdout.flush()
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

def play_again() -> bool:
    message = "\nYou must enter 'Yes' or 'No' only."
    while True:
        try:
            play_again = input(
                "\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                return True
            elif play_again in ['no', 'n']:
                delay_effect([
                    "\nGame session complete.\n\nThanks for playing Tic-Tac-Toe. See you in the next session.\n"
                ])
                return False
            else:
                print(message)

        except ValueError:
            print(message)

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
#     def print_player_turn_prompt_tictactoe(name: str) -> None:
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

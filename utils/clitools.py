"""
clitools.py 
Author: Robert Pal
Updated: 2025-08-05

This module contains helper functrions for Command Line Applications.
"""
import os
import shutil
from time import sleep
from itertools import chain
from utils.game_options import GameOptions
from utils.square import Square
from utils.strings import tictactoe_strings, connect4_strings, solitaire_strings, other_strings
from typing import Union, Set, Optional

# ==== Helper functions for console and screen management at os level in controlling overall command line display ====
def clear_screen() -> None:
    """Clears all printed input on terminal screen for display purposes."""
    os.system('cls' if os.name == 'nt' else 'clear')

def set_console_window_size(width: float, height: float) -> None:
    """Sets the console window size to fit the board better for both Windows."""
    os.system('cls||clear')
    # Make it compliant for Linux/MacOS and Windows systems
    if os.name == 'nt':
        os.system(f'mode con: cols={width} lines={height}')
    else:
        os.system(f'printf "\033[8;{height};{width}t"')
        
# ==== Helper for functions for string management in creating typewriter effect and box effect on output to user  ====
def delay_effect(strings: Union[list[str], str], delay: float = 0.015, word_flush: bool = True) -> None:
    """
    Creates the effect of printing line by line or character by character. Speed of printing can be changed with delay parameter.
    When word_flush is true, each character or letter will print one by one according to the delay speed.
    When word_flush is false, each individual line will print one by one according to the delay speed.
    Requires a list of strings to be displayed. If a string is passed, each character will be printed on its onw line. 
    """
    # Used for testing to speed up output
    # if delay != 0:
    #     delay = 0  
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)

def surround_string(strings: list[str], symbol: str, offset: int = 0) -> list[str]:
    """Creates a bordered box display around any mulit-line text and centers it, which is used for scoreboards or other messages."""
    # Split each string from list on '\n' if it has one; otherwise, keep the string as a single element by wrapping it in a list.
    # Use itertools.chain.from_iterable to flatten the resulting list of lists into a single string, which is then wrapped in a list of strings, which
    # each line in the text is a single element in the list.
    string_list = list(chain.from_iterable(
        string.split("\n") if "\n" in string else [string] for string in strings)
        )
    # Find the longest line from string list and build a border using the symbol, padded by offset on both sides if not set to 0.
    border = symbol * (len(max(string_list, key=len)) + 2 * offset)
    # Make complete list with top border, centered line of text matching the border length, and bottom border
    output_list = [border, *[string.center(len(border)) for string in string_list], border]
    # Add side symbols to each line, join lines with newlines, and add spacing above and below for final list
    return ["\n" + "\n".join([symbol + string + symbol for string in output_list]) + "\n"]

def print_menu_screen(delay: float=0.025):
    """Displays a menu of game options centered in the terminal screen. Allows for new games to be added to menu with ENUMs."""
    clear_screen()
    # Get the command line console size
    columns, rows = shutil.get_terminal_size()
    # Dynamically add more game options using game_options ENUM, which stores the game options numerically via a string
    MENU_OPTIONS = {
        GameOptions.TIC_TAC_TOE.value: "Tic Tac Toe", # game_option "1"
        GameOptions.CONNECT_FOUR.value: "Connect 4",  # game_option "2"
        GameOptions.SOLITAIRE.value: "Solitaire"      # game_option "3"
    }

    # Menu options string created with top text and game options indented from top text
    menu_text = "Welcome to Simple Games.\n\n"
    for key, value in MENU_OPTIONS.items():
        menu_text += f"    {key}. {value}\n"
    # Centre left to right relative to the longest line in the menu_text, which should be the first line 
    horizontal_pos = (columns - len(max(menu_text.splitlines(), key=len))) // 2
    # Centre top to bottom relative to the total number of lines in te the menu_text
    vertical_pos = (rows - menu_text.count('\n') - 1) // 2

    # Start printing menu_text after adding the appropriate number of new lines as calculated in vertical_pos
    print('\n' * vertical_pos, end='')
    for line in menu_text.splitlines():
        # Start printing menu_text after adding the appropriate number of spaces as calculated in horizontal_pos
        print(' ' * horizontal_pos, end="")
        # Use delay)_effect for typewriter printing effect
        delay_effect([line], delay)

def menu_select(valid_selections: GameOptions, load_message: bool=True):
    """
    Obtain user selection from the game options. Repeat until a valid selection has been made from the ENUM class of game options. 
    Default boolean load_message for simulating classic game loading screens
    """
    print()
    # Get the terminal size
    columns, _ = shutil.get_terminal_size()
    prompt = "Select the game you want to play: "
    error = "Please only select a game from the available options."
    # Get the left to right positions for both prompt and error; add apppropriate number of spaces, as per procedure in print_menu_screen
    horizontal_pos_for_prompt = (columns - len(prompt)) // 2
    horizontal_pos_for_error  = (columns - len(error)) // 2
    blank_space_prompt = ' ' * horizontal_pos_for_prompt
    blank_space_error = ' ' * horizontal_pos_for_error
    # All displays are centred in the middle of the screen and appropriated spacing is added using the blank_space strings
    while True:
        print(blank_space_prompt + prompt, end="")
        choice = input().strip()
        if choice in valid_selections: # from game_options ENUM - only allows 1, 2, or 3 (stored as strings so type casting not needed)
            break
        print('\n' + blank_space_prompt, end="") # for cursor location management 
        print()
        print(blank_space_error + error)  
        print('\n' + blank_space_error, end="") # for cursor location management 
        sleep(1.5)
        clear_screen()
        # Re-prints the menu screen if invalid option was selected 
        print_menu_screen(delay=0)
        print()
    
    clear_screen()
    if load_message:
        # Re-caculate console for centring the 'Game Loading' message
        columns, rows = shutil.get_terminal_size()
        print('\n' * (rows // 2)) # top bottom centring
        horizontal_pos = (columns - len("GAME LOADING")) // 2
        print(' ' * horizontal_pos + "GAME LOADING\n") # left right centring
        print('\n' + (' ' * horizontal_pos), end="") # cursor location management 
        sleep(2)
        clear_screen()

    return choice

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
        # print('\n' * 3)
        delay_effect([create_board_connect4(game_board=translated_board, line=connect4_strings["boardline"])], 
                     delay=0, word_flush=False) # No delay for Connect Four
        print(connect4_strings["boardline"])
        print(connect4_strings["boardlabels"])

def print_board_dropping_effect(board_states: list[list[list[Union[int, str]]]], sleep_delay=0.075):
    """Prints the Connect 4 Board with animation that simulates a dropping effect. Sleep delay can control the speed of the dropping piece."""
    # print the temp board starting from the top to simmulate falling piece
    for board_state in board_states:
        print("\n" * 3)
        print_board(board_state, "Connect4")
        sleep(sleep_delay)
        clear_screen()

def print_board_with_spacing(game_board, game="Connect4", spacing=3):
        """For printing the Connect 4 board with space on top and clear screen."""
        clear_screen()
        print("\n" * spacing)
        print_board(game_board=game_board, game_name="Connect4")

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
    delay_effect([f"\nIt is {name}'s turn. Select the column you want to drop your piece in.\n"], 0)

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
    print(f"\n{name} is now thinking.")
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
    """Updates the difficulty level boolean when playing against the computer. Returns None, False, or True"""
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    # Tic Tac Toe has three AI levels and Connect 4 only two (for now)
    if game_name == "TicTacToe":
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind, 2) Normal, 3) Impossible: "
    else:
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind or 2) Normal: "
    # Allow for user to input number or selection name
    valid_input = ['1', 'blind', '2', 'normal', '3', 'impossible']
    while True:
        level_of_difficulty = input(difficulty_choices).lower() # get the user's selection
        # None for blind or easy mode
        if level_of_difficulty in valid_input[:2]:
            delay_effect(["\nYou are playing against the computer in easy mode."])
            return None
        # False for normal or intermediate mode
        elif level_of_difficulty in valid_input[2:4]:
            delay_effect(["\nYou are playing against the computer in intermediate mode." ])
            return False
        # True for impossible or hard mode (not available for Connect 4)
        elif level_of_difficulty in valid_input[4:]:
            if game_name == "Connect4":
                print("\nThis option is not currently avaliable for Connect 4. Please select again")
            else:
                delay_effect(["\nYou are playing against the computer in hard mode."])
                return True
        else:
            print(
                "\nPlease select a valid option or press the corresponding number only.")


def print_tableau(tableau_lists: list[list]):
    """
    Displays all piles in the tableau by printing each row one at a time with lables and horizontal lines. All card widths are normalized for alignment.
    Includes customized options to ensure all piles are aligned correctly with proper spacing. Shorter piles are padded with blank spaces so all piles are the same length.
    """
    def normalize_cards_in_stack(card_stack, width=12):
        """
        Normalizes all cards in stack to be equal length to print the cards in-line on the command line screen. 
        Values require specific tweaking based on the command line console size because of the difference in sizes between various cards that 
        contain different sized emojis. Default width of 12."""
        new_card_stack = []
        for card in card_stack:
            # Face down card needs to be be defaulted to hard wiring code of 11 for proper spacing
            if card == "🎴":
                card = card.center(11)
            # For setting a blank draw when the pile has less cards than other piles
            elif card == " ":
                card = card.center(width)
            # For setting other cards in deck which have slightly different widths.
            else:
                card = card.center(width + 1)
            new_card_stack.append(card)
        return new_card_stack

    def print_labels(column_width=17):
        """Adds labels and name plate to be printed on top of tableau piles. Numbers are hard wired and tweaked for proper viewing."""
        print("TABLEAU")
        tableau_labels = ["Stack 1", "Stack 2", "Stack 3", "Stack 4", "Stack 5", "Stack 6", "Stack 7"]
        print()
        for label in tableau_labels:
            # Add the proper amount of spacing to the label for each pile
            print(f"{label:^{column_width}}", end='')
        print()
        # Add bottom line to label: Values need to be tweaked to align properly
        print(" " * 4 + (" -------" + " " * 9) * 7)

    # Get the number for the largest tableau card pile to add blank cards for padding of column stacks
    max_height = max(len(stack) for stack in tableau_lists)

    # Ensure all card stacks are the same length by adding blank spaces to shorter piles that have fewer cards
    padded_tableau = [
        stack + [" "] * (max_height - len(stack)) for stack in tableau_lists
    ]

    # Ensure all cards are padded to the same size for alignment in columns
    padded_cards_and_tableau = [normalize_cards_in_stack(card_stack) for card_stack in padded_tableau]

    # Print name and labels for tableau
    print_labels()
    # Customized spacing
    column_space = " " * 5
    # Print the cards row by row each pile using custom spacing for properly tweaked alignment
    for row in zip(*padded_cards_and_tableau):
        print(column_space.join(card for card in row))


def print_foundation_piles(piles):
    """Display the suit of an empty foundation pile, otherwise displays the face of the top card on the card stack."""
    print("FOUNDATION PILES\n")
    # Card stack has optionally atribute called 'suit' for displaying a foundation pile that hasn't been built on yet
    top_cards = [
        card_stack.get_stack_suit() if card_stack.is_empty()
        else card_stack.top_card().face
        for card_stack in piles.values()
    ]
    print("   |   ".join(top_cards)) # Divider


def print_draw_pile(pile, centering_value=6):
    """Display the stock pile as either face down card deck or empty card deck."""
    print("STOCK PILE")
    print()
    if not pile:
        print("🎴".center(centering_value))
    else:
        print("⚔️".center(centering_value))


def print_waste_pile(pile, centering_value=6):
    """Display the waste pile of cards for play: 1, 2 or 3 cards maximum or empty card deck."""
    if len(pile) == 0:
        print("⚔️".center(centering_value))
    else:
        for card in pile:
            print(card)


def print_card_table(tableau: list, foundation_piles: dict, draw_pile: bool, waste_pile: list):
    """Display the Solitaire table including the foundation, tableau, draw and waste piles."""
    print_foundation_piles(foundation_piles)
    print()
    print_tableau(tableau)
    print()
    print_draw_pile(draw_pile)
    print()
    print_waste_pile(waste_pile)
    print()
            
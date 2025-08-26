"""
prompting.py 
Author: Robert Pal
Updated: 2025-08-26

This module contains all prompting and move validation helper functions for Command Line Applications.
"""
import shutil
from time import sleep
from utils.clitools.console import clear_screen
from utils.clitools.console import delay_effect
from utils.clitools.printing import print_menu_screen
from utils.game_options import GameOptions
from typing import Union, Optional

# Function for prompting menu options from the user - used with `print_menu_screen`` from printing module
def menu_select(valid_selections: GameOptions, load_message: bool=True) -> GameOptions:
    """Obtains a user's game selection from the menu of game options.

    This function continuously prompts the user until a valid selection is made from the `GameOptions` Enum of availble games for play.

    Args:
        valid_selections: The Enum dictonary containing valid game options.
        load_message: If True, simulates a classic game loading screen. Defaults to True.

    Returns:
        The valid choice of game selected by the user or `GameOptions` Enum value.
    """
    print()
    columns, _ = shutil.get_terminal_size()
    prompt = "Select the game you want to play: "
    error = "Please only select a game from the available options."
    # Get the left to right positions for both prompt and error; add apppropriate number of spaces, as per procedure in print_menu_screen in printing
    horizontal_pos_for_prompt = (columns - len(prompt)) // 2
    horizontal_pos_for_error  = (columns - len(error)) // 2
    blank_space_prompt = ' ' * horizontal_pos_for_prompt
    blank_space_error = ' ' * horizontal_pos_for_error
    # All displays are centred in the middle of the screen and appropriate spacing is added using the blank_space strings and centre measurements above
    while True:
        print(blank_space_prompt + prompt, end="")
        choice = input().strip()
        if choice in valid_selections: # from game_options ENUM - only allows 1, 2, or 3 - stored as strings, so int type casting not needed.
            break
        print('\n' + blank_space_prompt, end="") # for cursor location management 
        print()
        print(blank_space_error + error)  
        print('\n' + blank_space_error, end="") # for cursor location management 
        sleep(1.5)
        clear_screen()
        # Re-prints the menu screen if invalid option was selected
        print_menu_screen(delay=0) # imported function from printing
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

# ==== Functions for player options including determining the number of players or name of the players ====
def get_player_names(two_players=False) -> Union[str, tuple[str, str]]:
    """Gets names for one or two players.

    Args:
        two_players: A boolean that determines whether to prompt for a second player's name. Defaults to False.

    Returns:
        If `two_players` is False, returns a single string representing the first player's name. 
        Otherwise, returns a tuple containing two strings, one for each player's name.
    """
    name_one = input("\nPlease enter the name for Player one or press enter: ")
    if not two_players:
        return name_one
    else:
        name_two = input("\nPlease enter the name for Player two or press enter: ")
        return name_one, name_two
 
def one_player() -> bool:
    """Determines if the game is for one or two players.

    This function prompts the user until a valid input is received.

    Returns:
        True if the game is for one player, False otherwise.
    """
    valid_input = {'1', '2', 'one', 'two'}
    while True:
        one_player_choice = input("How many players? One or two: ").lower()
        if one_player_choice in valid_input:
            return one_player_choice in ['1', 'one']
        print('\nOnly one or two players are allowed.\n')

# Function for selecting AI difficulty level of game play in Tic Tac Toe or Connect 4
def select_difficulty_level(game_name: str) -> Optional[bool]:
    """Prompts the user to select the AI difficulty level and returns the difficulty level settting for AI game play.

    This function offers different difficulty options based on the game and returns a boolean value representing the selected level.

    Args:
        game_name: The name of the game ('TicTacToe' or 'Connect4').

    Returns:
        True for 'impossible' mode, False for 'normal' mode, and None for 'blind' mode.
    
    Raises:
        ValueError: If `game_name` is not 'TicTacToe' or 'Connect4'.
    """
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    # Tic Tac Toe has three AI levels and Connect 4 only two (for now)
    if game_name == "TicTacToe":
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind, 2) Normal, 3) Impossible: "
    else:
        difficulty_choices = "\nSelect the level of difficult for the AI: 1) Blind or 2) Normal: "
    # Allow for user to input number or name of difficulty level
    valid_input = ['1', 'blind', '2', 'normal', '3', 'impossible'] # Use string slices for the 3 valid selections
    while True:
        level_of_difficulty = input(difficulty_choices).lower() 
        if level_of_difficulty in valid_input[:2]:
            delay_effect(["\nYou are playing against the computer in easy mode."])
            return None # None for blind or easy mode
        elif level_of_difficulty in valid_input[2:4]:
            delay_effect(["\nYou are playing against the computer in intermediate mode." ])
            return False # False for normal or intermediate mode
        elif level_of_difficulty in valid_input[4:]:
            if game_name == "Connect4":
                print("\nThis option is not currently avaliable for Connect 4. Please select again")
            else:
                delay_effect(["\nYou are playing against the computer in hard mode."])
                return True # True for impossible or hard mode (not currently available for Connect 4)
        else:
            print(
                "\nPlease select a valid option or press the corresponding number only.")

# Function for multi-play option
def play_again() -> bool:
    """Asks the user if they want to play again.

    This function validates user input, prompting until 'yes' or 'no' is entered.

    Returns:
        True if the user wants to play again, False otherwise.
    """
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

# ==== Two functions that work together for prompting board moves for single column move or row and column move for Tic Tac Toe and Connect 4 ====
def get_valid_int(prompt: str, valid_input: set, error_message: str) -> int:
    """Gets and validates an integer input from the user.

    This helper function prompts the user for an integer until validate input in allowed range is entered.

    Args:
        prompt: The message to display to the user.
        valid_input: A set of valid integer values.
        error_message: The message to display for invalid input.

    Returns:
        The validated integer input, adjusted for a 0-based index.
    """
    while True:
        try:
            input_value = int(input(prompt))
            if input_value in valid_input:
                return input_value - 1
            print(f"\n{error_message}\n")
        except ValueError:
            print("\nYou must enter a number. Try again.\n")

def prompt_move(game_name: str, valid_input_range: int) -> Union[tuple[int, int], int]:
    """Gets a valid move from the player based on the game.

    This function prompts the user for the necessary inputs, either a row and column for Tic-Tac-Toe, or a single column for Connect 4, 
    and validates it using the `get_validated_int_input` helper function.

    Args:
        game_name: The name of the game ('TicTacToe' or 'Connect4').
        valid_input_range: The maximum value for the column number.

    Returns:
        If `game_name` is 'TicTacToe', returns a tuple containing the 0-based row and column indices. 
        If `game_name` is not 'TicTacToe', returns a single integer representing the 0-based column index.
    """
    valid_input = {i + 1 for i in range(valid_input_range)}
    if game_name == 'TicTacToe':
        error_message = f"You must enter a number from 1 to {valid_input_range} only."
        row = get_valid_int(prompt="Enter the row: ", valid_input=valid_input, error_message=error_message)
        column = get_valid_int(prompt="Enter the column: ",valid_input=valid_input, error_message=error_message)
        return row, column
    else:
        column = get_valid_int(prompt="Enter the column: ",
                                         valid_input={i + 1 for i in range(valid_input_range)}, 
                                         error_message=f"You must enter a column from 1 to {valid_input_range} only.")
        return column

# Function for determining the difficulty level of Solitaire
def select_klondike_draw_number() -> int:
    """Asks the user to select the number of cards to draw at a time.

    This function validates user input to obtain a draw count of '1' or '3' for Klondike Solitaire game.

    Returns:
        An integer representing the number of cards to draw per turn: 1 or 3.
    """
    valid_input = {"1", "3"}
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
            
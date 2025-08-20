"""
prompting.py 
Author: Robert Pal
Updated: 2025-08-20

This module contains all prompting and move validation helper functions for Command Line Applications.
"""
import shutil
from time import sleep
from utils.clitools.console import clear_screen
from utils.clitools.console import delay_effect
from utils.clitools.printing import print_menu_screen
from utils.game_options import GameOptions
from typing import Union, Optional

# Function for dprompting menu options from the user - used with print_menu_screen from printing module
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

def get_validated_int_input(prompt: str, valid_input: set, error_message: str) -> int:
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
        error_message = f"You must enter a number from 1 to  {valid_input_range} only."
        row = get_validated_int_input(prompt="Enter the row: ", valid_input=valid_input, error_message=error_message)
        column = get_validated_int_input(prompt="Enter the column: ",valid_input=valid_input, error_message=error_message)
        return row, column
    else:
        column = get_validated_int_input(prompt="Enter the column: ",
                                         valid_input={i + 1 for i in range(valid_input_range)}, 
                                         error_message=f"You must enter a column from 1 to {valid_input_range} only.")
        return column


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
            
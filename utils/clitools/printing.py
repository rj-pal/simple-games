"""
printing.py 
Author: Robert Pal
Updated: 2025-08-21

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
def surround_string(strings: list[str], border_symbol: str="|", offset: int = 0) -> list[str]:
    """Creates a bordered box display around multi-line text with each line centred. Formatted strings are stored in a list.
    
    This function centers text based on the longest line from a list of strings with white space padding on shorter lines. It creates a top and bottom border 
    based on the length of the longest line, and adds a right and left border to each line. Offset padding can be set to extend the width of the box with 
    inner padding. The function is useful for scoreboards or other game info messaging.

    Args:
        strings: A list of strings to be placed inside the box.
        border_symbol: The symbol used for the box border. Defaults to '|'.
        offset: The amount of padding to add to the border. Defaults to 0.

    Returns:
        A list of formatted strings with new lines and the border symbol before and after the line of text, and a top and bottom border line.
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
    """Centers a multi-line ASCII art string within the terminal width.

    Args:
        list_of_strings: A list of strings representing the multi-line ASCII art.
        terminal_width: The width of the terminal.

    Returns:
        A single string with each line centered and joined by newlines.
    """
    centered_lines = []
    for line in list_of_strings:
        centered_lines.append(line.center(terminal_width))
    return "\n".join(centered_lines)

# ==== Functions for general board creation and display ====
def board_translator(game_board: list[list[Union[int, str]]]) -> list[list[Square]]:
    """Convert raw board data into Square Enum values.

    This function maps raw board data from Tic-Tac-Toe or Connect 4 to `Square` Enum values for command-line display.

    Args:
        game_board: A 2D list containing integer or string representations of the game board cells.

    Returns:
        A 2D list with the cell values translated to `Square` Enums or ASCII art form.
    """
    # Translator is necessary since Board objects are lists of str and int, whereas printing requires 2D marker representation in ascii art form
    marker_mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y} 
    return [[marker_mapping[cell] for cell in row] for row in game_board]


def print_board(game_board: list[list[Union[int, str]]], game_name: str, delay_rate: float=0.000175) -> None:
    """Prints the game board with an optional delay effect for typewritter dispaly.

    This function translates board data (strings and integers) to `Square` Enum strings for display. Lines are created row by row by zipping together each
    2D `Square` Enum for each row. Each square is printed line by line from top to bottom in the board with added border symbols to create the 2D grid board.
    The formatted board string is passed as a list to the delay function to create the typewritter effect if delay is not 0. 

    Args:
        game_board: A 2D list representing the current state of the game board.
        game_name: The name of the game ('TicTacToe' or 'Connect4').
        delay_rate: The delay rate for the print effect. Defaults to 0.000175.
    
    Raises:
        ValueError: If `game_name` is not 'TicTacToe' or 'Connect4'.
    """
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    
    translated_board = board_translator(game_board=game_board) # Get 2D `Square` Enum board for typewritter printing
    
    if game_name == 'TicTacToe':
        delay_effect([create_board(game_board=translated_board, game_name="TicTacToe", grid_line=tictactoe_strings["boardline"])],
                     delay=delay_rate, word_flush=False) # Use default delay for Tic Tac Toe
    elif game_name == 'Connect4':
        delay_effect([create_board(game_board=translated_board, game_name="Connect4", grid_line=connect4_strings["boardline"])],
                     delay=0, word_flush=False) # No delay for Connect Four since it uses dropping effect
        # For adding bottom borderline to Connect4 board and column labels for easier UI experience in making moves
        print(connect4_strings["boardline"])
        print(connect4_strings["boardlabels"])


def create_row(row: list[list[Square]], border_symbol: str, centre: bool = False) -> str:
    """Returns a formatted string of a single game board row.

    This function zips together a single row of a 2D board with grid border lines for inside walls.

    Args:
        row: A 2D list representing a single row of the board.
        border_symbol: The symbol for the inside grid lines.
        centre: A boolean flag to centre the row. Defaults to False.

    Returns:
        A formatted string of the board row.
    """
    # Centre functionality is used with Tic Tac Toe only - previous function does boolean check of game_name to pass the correct boolean flag here
    if centre: 
        return "\n".join([border_symbol.join(line).center(shutil.get_terminal_size().columns - 1)for line in zip(*row)])
    else:
        return "\n".join([border_symbol.join(line) for line in zip(*row)])

def create_board(game_board: list[list[Union[int, str]]], game_name: str, grid_line: str) -> str:
    """Returns a formatted string representation of the entire game board.

    Args:
        game_name: The name of the game ('TicTacToe' or 'Connect4').
        game_board: A 2D list representing the game board.

    Returns:
        A formatted string of the complete board.
    
    Raises:
        ValueError: If `game_name` is not 'TicTacToe' or 'Connect4'.
    """
    if game_name not in {'TicTacToe', 'Connect4'}: # Extra safety precaution
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    
    # Game configuration accounts for minor differences in boards and can be customized (main difference is centring of the board or not)
    game_config = {
        'TicTacToe': {'border_symbol': '*', 'line_func': lambda line: line.center(shutil.get_terminal_size().columns - 1)},
        'Connect4': {'border_symbol': '|', 'line_func': lambda line: line}
    }

    board_config = game_config[game_name]
    border_symbol = board_config['border_symbol']
    line_func = board_config['line_func'] 
    
    line = f"\n{line_func(grid_line)}\n"  # Grid lines are the row seperators and the symbols match with the column walls

    return line.join([create_row(row=[square.value for square in row], border_symbol=border_symbol, 
                                 centre=(game_name == 'TicTacToe')) for row in game_board]) # Boolean check for game_name since only TicTacToe should be centred


# ==== Functions for specific for Connect 4 board display ====
def print_board_dropping_effect(board_states: list[list[list[Union[int, str]]]], sleep_delay: float=0.075, top_spacing: int=3) -> None:
    """Prints the Connect 4 board with a dropping animation effect.

    Args:
        board_states: A list of 2D lists, where each list represents a board state for the animation frames.
        sleep_delay: The time delay between each animation frame. Defaults to 0.075 seconds.
        top_spacing: The number of newlines to print before the board for top spacing. Defaults to 3.                 
    """
    for board_state in board_states:
        print("\n" * top_spacing)
        print_board(game_board=board_state, game_name="Connect4")
        sleep(sleep_delay)
        clear_screen()

def print_board_with_spacing(game_board: list[list[Union[int, str]]], top_spacing=3) -> None:
    """Prints the Connect 4 board with top spacing for displaying single use board state of the current game.

    Args:
        game_board: The 2D list representing the current game board.
        top_spacing: The number of newlines to print before the board for top spacing. Defaults to 3.
    """    
    clear_screen()
    print("\n" * top_spacing)
    print_board(game_board=game_board, game_name="Connect4")

# ==== Functions for game messaging ====
def print_winner_info(name: str, marker: str, win_type: str, win_index: int, border_symbol: str="#", offset: int=9, 
                      delay: float=0.00075, word_flush=False) -> None:
    """Displays the winner's information based on saved attributes from the `Game` object. Displays message for draw game with no winner.

    Args:
        name: The name of the winner.
        marker: The marker of the winner ('x', 'o', 'r' or 'y').
        win_type: The type of win ('row', 'column', 'right_diagonal', or 'left_diagonal').
        win_index: The index of the winning row, column, or starting point of diagonal.
        border_symbol: The symbol for the message border. Defaults to '#'.
        offset: The padding for the message box. Defaults to 9.
        delay: The delay rate for the print effect. Defaults to 0.00075.
        word_flush: A boolean to control word flushing for typewriter effecdt.
    """
    if all(info is None for info in (name, marker, win_type)): # Attributes are all None in draw game, since attributes only update when winner is found
        draw_string = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"
        delay_effect(surround_string(strings=[draw_string], border_symbol=border_symbol, offset=offset), delay=delay, word_flush=word_flush)     
    else:
        winner_string = f"\nWinner winner chicken dinner. {name} is the winner.\n{marker.upper()} wins in"
        win_type_dict = { # Use winner attributes to create dictionary based on the type of win
            "row": f"row {win_index + 1}.",
            "column": f"column {win_index + 1}.",
            "right_diagonal": "the right diagonal.",
            "left_diagonal": "the left diagonal."
        }
        winner_string = f"{winner_string} {win_type_dict[win_type]}\n"
        delay_effect(surround_string(strings=[winner_string], border_symbol=border_symbol, offset=offset), delay=delay, word_flush=word_flush)


def print_scoreboard(player_list: list[str], border_symbol: str="#", offset: int=25, delay: float=0.00075, word_flush=False) -> None:
    """Displays the player statistics for the game.

    Args:
        player_list: A list of strings containing player statistics. __str__ representation of a `Player` object.
        border_symbol: The symbol for the scoreboard border. Defaults to '#'.
        offset: The padding for the scoreboard. Defaults to 25.
        delay: The delay rate for the print effect. Defaults to 0.00075.
        word_flush: A boolean to control word flushing for typewriter effect. Defaults to False.
    """
    delay_effect(surround_string(strings=player_list, border_symbol=border_symbol, offset=offset), delay=delay, word_flush=word_flush)


def print_computer_thinking(name: str="Computer", time_delay: int=1.5) -> None:
    """Prints a message to simulate the computer thinking with delay time.

    Args:
        name: The name of the computer player. Defaults to 'Computer'.
        time_delay: The delay in seconds before the message disappears. Defaults to 1.5.
    """
    print(f"\n{name} is now thinking.")
    print()
    sleep(time_delay)

def print_player_turn_prompt(name: str, game_name: str, delay_rate: float=0.015) -> None:
    """Print the prompt for the player's turn.

    Args:
        name: The name of the current player.
        game_name: The name of the game ('TicTacToe' or 'Connect4').
        delay_rate: The speed of the typewriter effect. Defaults to 0.015.

    Raises:
        ValueError: If `game_name` is not 'TicTacToe' or 'Connect4'.
    """
    if game_name not in {'TicTacToe', 'Connect4'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4'.")
    if game_name == 'TicTacToe':
        turn_prompt = f"\nIt is {name}'s turn. Select a row and column\n"
    elif game_name == 'Connect4':
        turn_prompt = f"\nIt is {name}'s turn. Select the column you want to drop your piece in.\n"
    delay_effect(strings=[turn_prompt], delay=delay_rate)


def print_first_player(name: str) -> None:
    """Prints who plays first and their marker.

    Args:
        name: The name of the first player.
    """
    delay_effect([f'\n{name} plays first.'])
    input('\nPress Enter to start the game.')

def print_square_occupied_prompt(name: str) -> None:
    """Prints a message when the selected square is occupied.
    
    Args:
        name: The name of the current player.
    """
    print("\nThe square is already occupied. Select another square.")
    delay_effect([f"\nIt is {name}'s turn again. Select a free square.\n"])

def print_current_move(name: str, row: int, column: int) -> None:
    """Prints the last move made by the current player.

    Args:
        name: The name of the current player.
    """
    delay_effect([
        f"\n{name} played the square in row {row + 1} and column {column + 1}.\n"
    ])

def print_game_over(winner_mark: str) -> None:
    """Displays flashing ascii art game over messages when a winner is found.

    Args:
        winner_mark: The marker of the winning player to display.
    """
    print()
    clear_screen()
    columns = shutil.get_terminal_size().columns
    for i in range(5):
        if i % 2 == 0: # Alternates between printing Game Over ascii art and 'Marker' Wins ascii art
            print(center_display_string(list_of_strings=other_strings["gameover"], terminal_width=columns))
        else:
            print(center_display_string(list_of_strings=other_strings[winner_mark], terminal_width=columns))
        sleep(0.45)
        clear_screen()
        sleep(0.45)
    print()

# ==== Functions for menu printing and game start up welcome messaging ====
def print_menu_screen(delay: float=0.025) -> None:
    """Displays a menu of game options centered on the terminal screen.

    This function allows for new games to be added using the `GameOptions` Enum.

    Args:
        delay: The delay rate for the typewriter print effect. Defaults to 0.025.
    """
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
        delay_effect(strings=[line], delay=delay) # Use delay_effect for typewriter printing effect


def print_start_game_message(game_name: str) -> None:
    """Prints the welcome and introduction message for a specific game.

    Args:
        game_name: The name of the game ('TicTacToe', 'Connect4', or 'Solitaire').
    
    Raises:
        ValueError: If `game_name` is not one of 'TicTacToe', 'Connect4', or 'Solitaire'.
    """
    if game_name not in {'TicTacToe', 'Connect4', 'Solitaire'}:
        raise ValueError("Invalid game argument passed. Must be 'TicTacToe' or 'Connect4' or 'Solitaire'.")
    if game_name == 'TicTacToe':
        string_dict = tictactoe_strings
    elif game_name == 'Connect4':
        string_dict = connect4_strings
    else:
        string_dict = solitaire_strings
    print(string_dict["welcome"])
    delay_effect(strings=[string_dict["intro"]])

# ==== Functions for displaying the complete Solitaire Game Table ====
def print_tableau(tableau_lists: list[list]) -> None:
    """Displays all piles in the tableau.

    This function normalizes the card widths and aligns all piles correctly with proper spacing. Shorter piles are padded with blank spaces to ensure all
    piles have the same height.

    Args:
        tableau_lists: A list of lists representing the tableau piles.
    """
    def normalize_cards_in_stack(card_stack: list, width: int=12) -> list:
        """Normalizes all cards in a stack to a uniform length.

        This helper function ensures proper in-line printing on the command line. Values require specific adjustments based on the terminal's font and size
        due to the varying widths of emojis.

        Args:
            card_stack: A list of cards within a single tableau pile.
            width: The target width for each card. Defaults to 12.

        Returns:
            A new list with all cards padded to the same width.
        """
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

    def print_labels(column_width: int=17) -> None:
        """Adds labels and a nameplate for the tableau piles.

        This functiuon contains hard-wired numbers for proper viewing alignment.
        """
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


def print_foundation_piles(piles: dict) -> None:
    """Displays the foundation piles.

    If a pile is empty, it displays the suit; otherwise, it shows the face of the top card on the stack.

    Args:
        piles: A dictionary of card piles representing the foundation piles.
    """
    print("FOUNDATION PILES\n")
    # Card stack has optionally atribute called 'suit' for displaying a foundation pile that hasn't been built on yet
    top_cards = [
        card_stack.get_stack_suit() if card_stack.is_empty()
        else card_stack.top_card().face
        for card_stack in piles.values()
    ]
    print("   |   ".join(top_cards)) # Divider


def print_draw_pile(pile_is_empty: bool, pile:list, centering_value=6) -> None:
    """Displays the stock and waste piles.

    The stock pile is represented as a face-down card deck emoji, or an empty deck emoji if the pile is empty. The waste pile shows the top card(s)
    or an empty deck emoji. The number of cards in the waste pile matches the klondike value of 1 or 3.

    Args:
        pile: The draw pile.
        centering_value: The value used to center the emoji. Defaults to 6.
    """
    print("DRAW PILE")
    print()
    if not pile_is_empty:
        print("🎴".center(centering_value))
    else:
        print("⚔️".center(centering_value))
    print()
    if len(pile) == 0:
        print("⚔️".center(centering_value))
    else:
        for card in pile:
            print(card)


def print_card_table(tableau: list, foundation_piles: dict, stock_pile_is_empty: bool, waste_pile: list) -> None:
    """Displays the complete Solitaire table.

    This function calls four helper functions to display the complete solitaire table: foundation, tableau, draw, and waste piles.

    Args:
        tableau: A list of lists representing the tableau piles.
        foundation_piles: A dictionary of the foundation piles.
        draw_pile: A boolean indicating if the draw pile has cards.
        waste_pile: A list of cards in the waste pile.
    """
    print_foundation_piles(foundation_piles)
    print()
    print_tableau(tableau)
    print()
    print_draw_pile(stock_pile_is_empty, waste_pile)
    print()

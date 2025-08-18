"""
main.py 
Author: Robert Pal
Updated: 2025-08-17

This module contains control flow logic for running the the Simple Games applications through the main() function. Game option Enums are used to 
determine the permitted game to be run. Command line tools are used for user input and display. It also includes some testing and in developement functions.
"""
from cli import TicTacToeCLI, ConnectFourCLI, SolitaireCLI
from utils.clitools.printing import print_menu_screen
from utils.game_options import GameOptions
from utils.clitools.clitools import menu_select
from utils.strings import SIMPLE_GAMES_START

### In development ###
# import sys
# import select

# def clear_stdin_buffer():
#     """Clears any pending input typed by the user before the prompt."""
#     while select.select([sys.stdin], [], [], 0)[0]:
#         sys.stdin.read(1)  # Read one character at a time until buffer is empty


### Quick Running of a game for testing new feature or change to avoid menu options screen ###
def test():
    """Running command line app directly for testing. Comment out the games that are not being tested at the time."""
    # TicTacToeCLI.run()
    # SolitaireCLI.run()
    ConnectFourCLI.run()
    exit()


def main():
    print_menu_screen()
    ### In development mode
    # clear_stdin_buffer()
    valid_game_options = GameOptions.values()
    choice = menu_select(valid_game_options)

    if choice == GameOptions.TIC_TAC_TOE.value:
        TicTacToeCLI.run()
    elif choice == GameOptions.CONNECT_FOUR.value:
        ConnectFourCLI.run()
    elif choice == GameOptions.SOLITAIRE.value:
        SolitaireCLI.run()
    else:
        raise ValueError("Invalid choice. See you next time.")

if __name__ == '__main__':
    # main()
    ### Use when testing
    test()

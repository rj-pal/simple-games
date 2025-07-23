from cli import TicTacToeCLI, ConnectFourCLI, SolitaireCLI
from utils.game_options import GameOptions
from utils.clitools import print_menu_screen, menu_select
from utils.strings import SIMPLE_GAMES_START

# import sys
# import select

# def clear_stdin_buffer():
#     """Clears any pending input typed by the user before the prompt."""
#     while select.select([sys.stdin], [], [], 0)[0]:
#         sys.stdin.read(1)  # Read one character at a time until buffer is empty

 
def main():
    ### For quick testing of individual games
    # TicTacToeCLI.run()
    # SolitaireCLI.run()
    # ConnectFourCLI.run()
    # exit()
    print_menu_screen() 
    # clear_stdin_buffer()
    valid_game_options  = GameOptions.values()
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
    main()

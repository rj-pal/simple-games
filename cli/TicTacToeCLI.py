"""
TicTacToeCLI.py 
Author: Robert Pal
Updated: 2025-08-26

This module contains all control flow logic for running the Tic Tac Toe Command Line Application.
It includes:
- run() which acts as the main() game running function
- set_up_game() which sets game play configerations
- play_game() which controls the all actual game play logic and commands
"""
from games.tictactoe import TicTacToe
import utils.clitools.printing as display
import utils.clitools.prompting as prompt
import utils.clitools.console as console
 
def set_up_game() -> TicTacToe:
    """Sets up the game configurations for one or two players.

    This function prompts for the number of players, sets the AI difficulty if a single player is chosen, and allows players to customize their names. 
    Player one is assigned the 'x' marker and moves first.

    Returns:
        An instance of the `TicTacToe` class with the configured game settings and name updates.
    """
    game = TicTacToe()
    # One or two player mode set by function from command line utility tools using tertiary values T, F or None.
    if prompt.one_player():
        difficulty = prompt.select_difficulty_level(game_name="TicTacToe")
        name_dictionary = {
            None: "CPU Easy",
            False: "CPU Intermediate",
            True: "CPU Hard"
        }
        # Allow for player one to update default player names
        game.create_ai_player(name=name_dictionary[difficulty], difficulty=difficulty)
        player_one_name = prompt.get_player_names(two_players=False)
        game.update_player_name(name=player_one_name, marker="x")

    else:
        # Allows for both users to update default player names
        player_one_name, player_two_name = prompt.get_player_names(two_players=True)
        game.update_player_name(name=player_one_name, marker="x")
        game.update_player_name(name=player_two_name, marker="o")

    return game


def play_game(game) -> None:
    """Runs the game control flow for a single game.

    This function manages all user input and display using command-line tools for a nine-round game. It handles both human and AI player turns and
    terminates early if a winner is found.

    Args:
        game: An instance of the `TicTacToe` game class.
    """
    for i in range(game.board_size):
        # When go_first is true, player one or 'x' will be the player set for the round, or else player two or 'o' will be set for the round
        player = game.get_player(i % 2) if game.go_first else game.get_player(i % 2 - 1)
        name = player.name
        marker = player.marker
        if i == 0: # introduce the start of game to user
            display.print_first_player(name=name)
            prompt.clear_screen()

        # Handles human player logic, prompts and input
        if isinstance(player, TicTacToe.TicTacToePlayer):
            display.print_player_turn_prompt(name=name, game_name='TicTacToe') 
            while True:
                row, col = prompt.prompt_move(game_name='TicTacToe', valid_input_range=game.dimension)
                if game.make_move(row=row, col=col, marker=marker):
                    break
                else:
                    display.print_square_occupied_prompt(name=name)
        # Handles AI player logic
        elif isinstance(player, TicTacToe.AIPlayer):
            display.print_computer_thinking(name=name)
            row, col = player.move(board=game.board.get_board())
            game.make_move(row=row, col=col, marker=marker)
        
        # Displays board and other info to the user about the most current move
        prompt.clear_screen()
        display.print_current_move(name=name, row=row, column=col)
        display.print_board(game_board=game.board.get_board(), game_name="TicTacToe")

        # Ends the game before the final round if a winner is found. Check begins after minimum four moves have been played.
        if i >= 4 and game.check_winner():
            display.print_game_over(winner_mark=marker) # use player marker attribute to display correct game over screen        
            break
    # Updates winner info and player stats and gets winner infor for summary display
    game.update_winner_info()
    game.update_players_stats()
    winner = game.get_winner_attributes()
    if winner[0] is not None: # reprint the final board state if there was a winner. winner[0] is either the winning players name or None
        display.print_board(game_board=game.board.get_board(), game_name="TicTacToe")
    display.print_winner_info(*winner)
    # Resets the game state for new game
    game.reset_game_state()

def run(width: int=85, height: int=30, multiplay: bool=True) -> None:
    """Runs the main game control flow.

    This function initiates a game, sets up the game state, and controls the flow for single or multiple games in a session. It handles the display,
    player setup, and prompts the user to play again after each game. It displays an initial game message and introduction to the game.

    Args:
        width: The desired width of the console window. Defaults to 85.
        height: The desired height of the console window. Defaults to 30.
        multiplay: A boolean to determine if multiple games are allowed. Defaults to True.
    """
    console.set_console_window_size(width=width, height=height) # console dimensions: width, height
    display.print_start_game_message(game_name="TicTacToe")
    game = set_up_game() # for one or two player with AI settings
    play_game(game)
    multiplay = prompt.play_again() # allows for multiplay game sessions
    while multiplay:
        display.print_scoreboard(player_list=game.get_players_info_string_as_list()) # Show games history
        game.reset_board()
        play_game(game=game)
        multiplay = prompt.play_again()
    display.print_scoreboard(player_list=game.get_players_info_string_as_list())

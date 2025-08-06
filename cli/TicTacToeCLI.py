"""
TicTacToeCLI.py 
Author: Robert Pal
Updated: 2025-08-05

This module contains all control flow logic for running the Tic Tac Toe Command Line Application.
It includes:
- run() which acts as the main() game running function
- set_up_game() which sets game play configerations
- play_game() which controls the all actual game play logic and commands
"""
import utils.clitools as GameCLI
from games.tictactoe import TicTacToe
from utils.strings import tictactoe_strings, other_strings
 
def set_up_game() -> TicTacToe:
    """
    Sets up game play configurations for one or two players. If one player, sets the AI difficulty to easy, intermediate or hard.
    Player one plays 'x' and player two or AI plays 'o'. X moves first. In multi-play, the first player changes with each subsequent game.
    Players can select name or default name assigned if skipped.
    """
    game = TicTacToe()
    # One or Two player mode set by function from command line utility tools using tertiary values T, F or None.
    if GameCLI.one_player():
        difficulty = GameCLI.select_difficulty_level("TicTacToe")
        name_dictionary = {
            None: "CPU Easy",
            False: "CPU Intermediate",
            True: "CPU Hard"
        }
        # Allow for player one to update default player names
        game.create_ai_player(name=name_dictionary[difficulty], difficulty=difficulty)
        x = GameCLI.get_player_name()
        game.update_player_name(x, "x")

    else:
        # Allows for both users to update default player names
        player_one, player_two = GameCLI.get_player_names()
        game.update_player_name(player_one, "x")
        game.update_player_name(player_two, "o")

    return game


def play_game(game) -> None:
    """Runs the game control flow for a single, nine round game controling all user input and display using Command Line Tools."""
    for i in range(game.board_size):
        # When go_first is true, player one or 'x' will be the player set for the round, or else player two or 'o' will be set for the round
        if game.go_first:
            player = game.get_player(i % 2)
        else:
            player = game.get_player(i % 2 - 1)

        # Get the name for dipslay purposes
        name = player.get_player_name()
        if i == 0:
            GameCLI.print_first_player(name)
            GameCLI.clear_screen()

        # Handles human player logic, prompts and input
        if isinstance(player, TicTacToe.TicTacToePlayer):
            GameCLI.print_player_turn_prompt_tictactoe(name)
            while True:
                row, col = GameCLI.prompt_move()
                if game.make_move(row, col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
        # Handles AI player logic
        elif isinstance(player, TicTacToe.AIPlayer):
            GameCLI.print_computer_thinking(name)
            row, col = player.move(game.board.get_board())
            game.make_move(row, col, player.marker)
        
        # Displays board and other info to the user about the most current move
        GameCLI.clear_screen()
        GameCLI.print_current_move(name, row, col)
        GameCLI.print_board(game.board.get_board(), "TicTacToe")

        # Ends the game before the final round if a winner is found
        if i >= 4 and game.check_winner():
            GameCLI.print_game_over(player.marker) # use player marker attribute to display correct game over screen        
            break
    # Updates winner info and player stats
    game.update_winner_info()
    game.update_players_stats()
    # Gets the winner info for summary display
    winner = game.get_winner_attributes()
    if winner[0] is not None: # reprint the final board state if winner
        GameCLI.print_board(game.board.get_board(), "TicTacToe")
    GameCLI.print_winner_info(*winner)
    # Resets the game state for new game
    game.reset_game_state()

def run(width: int=85, height: int=30, multiplay: bool=True) -> None:
    """Main game control flow that initiates, sets up and asks for multi-game play."""
    GameCLI.set_console_window_size(width, height) # console dimensions: width, height
    
    # Game introduction message with basic game play explanation
    GameCLI.print_start_game("TicTacToe")
    
    # Set up the game state for one or two players and AI settings
    game = set_up_game()
    
    # Allow for multiple game play in a loaded session
    play_game(game)
    # Run function script to get boolean for multiplay
    multiplay = GameCLI.play_again()
    while multiplay:
        GameCLI.print_scoreboard(game.players) # Show games history
        game.reset_board()
        play_game(game)
        multiplay = GameCLI.play_again()
    GameCLI.print_scoreboard(game.players) # Show games history
    
    exit()

"""
ConnectFourCLI.py 
Author: Robert Pal
Updated: 2025-08-20

This module contains all control flow logic for running the Connect Four Command Line Application.
It includes:
- run() which acts as the main() game running function
- set_up_game() which sets game play configerations
- play_game() which controls the all actual game play logic and commands
"""
from games.connect4 import ConnectFour
import utils.clitools.prompting as prompt
import utils.clitools.printing
import utils.clitools.console

def set_up_game():
    """
    Sets up game play configurations for one or two players. If one player, sets the AI difficulty to easy, intermediate or hard.
    Player one plays 'Red' and player two or AI plays 'Yellow'. Red moves first. Players can select name or default name assigned if skipped.
    """
    game = ConnectFour()
    if prompt.one_player():
        difficulty = prompt.select_difficulty_level("Connect4")
        game.create_ai_player(difficulty=difficulty)
        red_player_1_name = prompt.get_player_names(two_players=False)
        game.update_player_name(red_player_1_name, "r")
    else:
        red_player_1_name, yellow_player_2_name = prompt.get_player_names(two_players=True)
        game.update_player_name(red_player_1_name, "r")
        game.update_player_name(yellow_player_2_name, "y")

    return game

def play_game(game) -> None:
    """Runs the game control flow for a single game controling all user input and display using Command Line Tools."""
    for i in range(game.board_size):
        player = game.get_current_player()
         
        # Display a welcome message and the initial prompt on first round to start game.
        if i == 0:
            utils.clitools.printing.print_first_player(name=player.name)
            # utils.clitools.printing.print_player_turn_prompt(name=player.name, game_name='Connect4')
        
        # Store the board state before any move to correctly handle screen updates, messaging to user and command line dispaly glitches.
        board_state_before_move = game.board.get_board(mutable=True)
        utils.clitools.printing.print_board_with_spacing(game_board=board_state_before_move.get_board())

        # Get validated column on board for human player or AI player to make move
        if player.is_human:
            utils.clitools.printing.print_player_turn_prompt(name=player.name, game_name='Connect4')
            while True:
                current_col = prompt.prompt_move(game_name='Connect4', valid_input_range=7)
                if not game.is_full(col=current_col):
                    break
                else:
                    utils.clitools.printing.print_square_occupied_prompt(name=player.name)
        else:
            utils.clitools.printing.print_computer_thinking(name=player.name, time_delay=2)
            current_col = player.move() # Use AI player method to get validated column
        
        # Updated the game state with validated column or else exit program - safety check
        if not game.make_move(col=current_col, marker=player.marker):
            print("Critical Error: Invalid move was attempted after move validation. Exiting the program.")
            exit(1)
        
        # Reprint the pre-move board and prompt to avoid screen glitches caused by the input prompt and ensure smooth user experience
        if player.is_human:
            utils.clitools.printing.print_board_with_spacing(game_board=board_state_before_move.get_board())
            utils.clitools.printing.print_player_turn_prompt(name=player.name, game_name='Connect4', delay_rate=0)
        
        # Display validation of last successful move to user before board animation
        utils.clitools.printing.print_current_move(player.name, *game.move_list[i])
        prompt.sleep(2)
        prompt.clear_screen()
        
        # Animation of game piece using a dropping effect
        board_states = game.get_board_animation_states(player_marker=player.marker)
        utils.clitools.printing.print_board_dropping_effect(board_states=board_states)
        
        # Check for a winner and end the game if a win condition is met. The game can only be won after a minimum of 7 moves (i>=6).
        if i >= 6 and game.check_winner():
            game.update_winner_info()
            game.update_players_stats()
            utils.clitools.printing.print_game_over(winner_mark=player.marker)
            prompt.clear_screen()
            utils.clitools.printing.print_board(game_board=game.board.get_board(), game_name="Connect4")
            game.print_winner()
            break

def run():
    # Optimized console window size for display for smooth user experience.
    utils.clitools.console.set_console_window_size(100, 48)
    utils.clitools.printing.print_start_game_message("Connect4")
    game = set_up_game()
    play_game(game)
    exit()

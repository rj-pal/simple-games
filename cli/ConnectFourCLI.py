"""
ConnectFourCLI.py 
Author: Robert Pal
Updated: 2025-08-26

This module contains all control flow logic for running the Connect Four Command Line Application.
It includes:
- run() which acts as the main() game running function
- set_up_game() which sets game play configerations
- play_game() which controls the all actual game play logic and commands
"""
from games.connect4 import ConnectFour
import utils.clitools.prompting as prompt
import utils.clitools.printing as display
import utils.clitools.console as console

def set_up_game():
    """Sets up the game configurations for one or two players.

    This function prompts the user for the number of players, sets the AI difficulty if a single player is chosen, and allows players to customize their names.
    Player one is assigned the 'Red' marker, and player two or the AI is assigned the 'Yellow' marker. 'Red' moves first.

    Returns:
        An instance of the `ConnectFour` class with the configured game settings and name updates.
    """
    game = ConnectFour()
    if prompt.one_player():
        difficulty = prompt.select_difficulty_level(game_name="Connect4")
        game.create_ai_player(difficulty=difficulty)
        red_player_1_name = prompt.get_player_names(two_players=False)
        game.update_player_name(name=red_player_1_name, marker="r")
    else:
        red_player_1_name, yellow_player_2_name = prompt.get_player_names(two_players=True)
        game.update_player_name(name=red_player_1_name, marker="r")
        game.update_player_name(name=yellow_player_2_name, marker="y")

    return game

def play_game(game) -> None:
    """Runs the game control flow for a single game.

    This function manages user input, displays the game board, and controls the flow for both human and AI player turns. It also includes the board animation
    and checks for a winner after each move.

    Args:
        game: An instance of the `ConnectFour` game class.
    """
    for i in range(game.board_size): # standard board size is 6 x 7
        player = game.get_current_player() 
        name = player.name
        marker = player.marker
        if i == 0: # introduce the start of game to user
            display.print_first_player(name=name)
        
        # Store the board state before any move to correctly handle screen updates, messaging to user and command line dispaly glitches.
        board_state_before_move = game.board.get_board(mutable=True)
        display.print_board_with_spacing(game_board=board_state_before_move.get_board())
        # Handles human player validation 
        if player.is_human:
            display.print_player_turn_prompt(name=name, game_name='Connect4')
            while True:
                current_col = prompt.prompt_move(game_name='Connect4', valid_input_range=game.columns)
                if not game.is_full(col=current_col):
                    break
                else:
                    display.print_square_occupied_prompt(name=name)
        # Handles AI player move validation
        else:
            display.print_computer_thinking(name=name, time_delay=2)
            current_col = player.move()
        
        # Updated the game state with validated column or else exit program - safety check
        if not game.make_move(col=current_col, marker=marker):
            print("Critical Error: Invalid move was attempted after move validation. Exiting the program.")
            exit(1)
        
        # Reprint the pre-move board and prompt to avoid screen glitches caused by the input prompt and ensure smooth user experience
        if player.is_human:
            display.print_board_with_spacing(game_board=board_state_before_move.get_board())
            display.print_player_turn_prompt(name=name, game_name='Connect4', delay_rate=0)
        
        # Display validation of last successful move to user before board animation
        display.print_current_move(name=name, *game.move_list[i]) # move list uses row, column
        prompt.sleep(2)
        prompt.clear_screen()
        
        # Animation of game piece using a dropping effect
        board_states = game.get_board_animation_states(player_marker=marker)
        display.print_board_dropping_effect(board_states=board_states)
        
        # Check for a winner and end the game if a win condition is met. The game can only be won after a minimum of 7 moves (i>=6).
        if i >= 6 and game.check_winner():
            game.update_winner_info()
            game.update_players_stats()
            display.print_game_over(winner_mark=marker)
            prompt.clear_screen()
            display.print_board(game_board=game.board.get_board(), game_name="Connect4")
            game.print_winner()
            break

def run():
    """Runs the main game control flow for Connect 4.
    This function initiates a game, sets up the game state, and controls the flow for a single session. It optimizes the console window size and 
    displays the initial game message.
    """
    # Optimized console window size for display for smooth user experience.
    console.set_console_window_size(100, 48)
    display.print_start_game_message(game_name="Connect4")
    game = set_up_game()
    play_game(game=game)

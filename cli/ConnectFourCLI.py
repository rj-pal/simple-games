"""
ConnectFourCLI.py 
Author: Robert Pal
Updated: 2025-08-01

This module contains all control flow logic for running the Connect Four Command Line Application.
It includes:
- run() which acts as the main() game running function
- set_up_game() which sets game play configerations
- play_game() which controls the all actual game play logic and commands
"""
from games.games import ConnectFour
import utils.clitools as GameCLI
from utils.strings import other_strings

def set_up_game():
    game = ConnectFour()

    if GameCLI.one_player():
        difficulty = GameCLI.select_difficulty_level("Connect4")
        game.create_ai_player(difficulty=difficulty)
        r = GameCLI.get_player_name()
        game.update_player_name(r, "r")

    else:
        r, y = GameCLI.get_player_names()
        game.update_player_name(r, "r")
        game.update_player_name(y, "y")

    return game

def play_game(game) -> None:
    
    for i in range(game.board_size):
        if game.go_first:
            player = game.players[i % 2]
        else:
            player = game.players[i % 2 - 1]

        name = player.get_player_name()
        if i == 0:
            GameCLI.print_first_player(name)
            GameCLI.print_player_turn_prompt_connect4(name)

        GameCLI.clear_screen()
        if player.is_human:
            pass

            
        if isinstance(player, ConnectFour.ConnectFourPlayer):
            
            
            # print(f"\nRound {game.round_count + 1}")
            print("\n" * 3)
            # Used to keep the board from not moving on the command line
            board_state_before_move = game.board.get_board(True)
            GameCLI.print_board(board_state_before_move.get_board(), "Connect4")
            GameCLI.print_player_turn_prompt_connect4(name)
            while True:
                col = GameCLI.prompt_column_move()
                if game.make_move(col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
            # Overwrite the get input prompt (or make_move) with the original prompt - this keeps the board in one position without screen glitches
            GameCLI.clear_screen()
            print("\n" * 3)
            # Re-print the board before the move 
            GameCLI.print_board(board_state_before_move.get_board(), "Connect4")
            # Re-print the prompt so it appears the state never changed (the current move is printed after this line, replacing the get input prompt line)
            GameCLI.print_player_turn_prompt_connect4(name)
        elif isinstance(player, ConnectFour.AIPlayer):
            print(other_strings["thinking"])
            GameCLI.sleep(2)
            col = player.move()
            game.make_move(col, player.marker)
        # Print the last made move by the player or AI player
        GameCLI.print_current_move(name, *game.move_list[i])
        GameCLI.sleep(2)
        GameCLI.clear_screen()
        board_states = game.get_board_animation_states(player.marker)
        # Printing for dropping effect
        GameCLI.print_board_dropping_effect(board_states=board_states)
        # Re-print the current board  
        print("\n" * 3)
        GameCLI.print_board(game.board.get_board(), "Connect4")
        if i >= 6 and game.check_winner():
            game.update_winner_info()
            game.update_players_stats()
            GameCLI.print_game_over(player.marker) # use player marker to print correct game over screen
            GameCLI.clear_screen()
            GameCLI.print_board(game.board.get_board(), "Connect4")
            game.print_winner()
            break
        

def run():
    GameCLI.set_console_window_size(100, 48)
    GameCLI.print_start_game("Connect4")
    game = set_up_game()
    play_game(game)
    exit()

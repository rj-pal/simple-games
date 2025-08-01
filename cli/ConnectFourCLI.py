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
            
        

        if isinstance(player, ConnectFour.ConnectFourPlayer):
            GameCLI.clear_screen()
            print(f"\nRound {game.round_count + 1}")
            GameCLI.print_player_turn_prompt_connect4(name)
            GameCLI.print_board(game.board.get_board(), "Connect4")
            print()
            while True:
                col = GameCLI.prompt_column_move()
                if game.make_move(col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
        elif isinstance(player, ConnectFour.AIPlayer):
            print(other_strings["thinking"])
            GameCLI.sleep(2)
            col = player.move()
            game.make_move(col, player.marker)

        # GameCLI.clear_screen()
        current_row, current_col = game.move_list[i]
        # GameCLI.clear_screen()
        print()
        # Printing for dropping effect
        for j in range(current_row):
            temp_board = game.board.get_board(True)
            for k in range(len(game.move_list) - 1): # populate the temp board up without the current move
                row, col =  game.move_list[k]
                temp_board.add_to_square(row, col, game.get_player(k % 2).marker)
            # print the temp board starting from the top to simmulate falling piece
            temp_board.add_to_square(j, current_col, player.marker)
            GameCLI.print_board(temp_board.get_board(), "Connect4")
            GameCLI.sleep(0.075)
            GameCLI.clear_screen()
            print()
            
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
        print()
        GameCLI.print_current_move(name, *game.move_list[i])

def run():
    GameCLI.set_console_window_size(100, 48)
    GameCLI.print_start_game("Connect4")
    game = set_up_game()
    play_game(game)
    exit()

import os
from time import sleep
from typing import Optional
import utils.clitools as GameCLI
from games.games import TicTacToe
from utils.strings import tictactoe_strings, other_strings#BOARDLINE_TICTAC, WELCOME_TICTACTOE, INTRO_TICTACTOE, GAMEOVER, THINKING
 
def set_up_game():
    game = TicTacToe()
    if GameCLI.one_player():
        difficulty = GameCLI.select_difficulty_level()
        name_dictionary = {
            None: "CPU Easy",
            False: "CPU Intermediate",
            True: "CPU Hard"
        }
        game.create_ai_player(name=name_dictionary[difficulty],
                              difficulty=difficulty)
        x = GameCLI.get_player_name()
        game.update_player_name(x, "x")

    else:
        x, y = GameCLI.get_player_names()
        game.update_player_name(x, "x")
        game.update_player_name(y, "o")

    return game


def play_game(game) -> None:
    for i in range(game.board_size):
        # print(game.round_count)
        if game.go_first:
            player = game.players[i % 2]
        else:
            player = game.players[i % 2 - 1]

        name = player.get_player_name()
        if i == 0:
            GameCLI.print_first_player(name)
            GameCLI.clear_screen()

        if isinstance(player, TicTacToe.TicTacToePlayer):

            GameCLI.print_player_turn_prompt_tictactoe(name)
            while True:
                row, col = GameCLI.prompt_move()
                if game.make_move(row, col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
        elif isinstance(player, TicTacToe.AIPlayer):
            print(other_strings["thinking"])
            sleep(1.5)
            row, col = player.move(game.board.get_board())
            game.make_move(row, col, player.marker)

        # GameCLI.clear_screen()
        GameCLI.print_current_move(name, row, col)
        GameCLI.print_board(game.board.get_board(), tictactoe_strings["boardline"])

        if i >= 4 and game.check_winner():
            GameCLI.print_game_over(other_strings["gameover"])
            GameCLI.print_board(game.board.get_board(), tictactoe_strings["boardline"])
            break
        
    game.update_winner_info()
    game.update_players_stats()
    winner = game.get_winner_attributes()
    GameCLI.print_winner_info(*winner)
    game.reset_game_state()


def play_again():
    message = "\nYou must enter 'Yes' or 'No' only."
    while True:
        try:
            play_again = input(
                "\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                return True
            elif play_again in ['no', 'n']:
                GameCLI.delay_effect([
                    "\nGame session complete.\n\nThanks for playing Tic-Tac-Toe. See you in the next session.\n"
                ])
                return False
            else:
                print(message)

        except ValueError:
            print(message)


def run():
    GameCLI.set_console_window_size(85, 30) # console dimensions: width, height
    GameCLI.print_start_game(tictactoe_strings["welcome"], tictactoe_strings["intro"])
    game = set_up_game()
    multiplay = True
    while multiplay:
        play_game(game)
        multiplay = play_again()
        GameCLI.print_scoreboard(game.players)
        game.reset_board()
    exit()

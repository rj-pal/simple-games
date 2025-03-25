from games.game import ConnectFour
from utils.strings import BOARDLINE_CONNECT4
from utils.clitools import * #set_console_window_size, print_board
import utils.clitools as GameCLI
from utils.strings import connect4_strings, other_strings

LINE = BOARDLINE_CONNECT4

def set_up_game():
    game = ConnectFour()

    if GameCLI.one_player():
        difficulty = GameCLI.select_difficulty_level()
        name_dictionary = {
            None: "CPU Easy",
            False: "CPU Intermediate",
            True: "CPU Hard"
        }
        game.create_ai_player(name=name_dictionary[difficulty],
                              difficulty=difficulty)
        # r = GameCLI.get_player_name()
        # game.update_player_name(r, "r")

    else:
        r, y = GameCLI.get_player_names()
        game.update_player_name(r, "r")
        game.update_player_name(y, "y")

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

        if isinstance(player, ConnectFour.ConnectFourPlayer):

            GameCLI.print_player_turn_prompt(name)
            while True:
                col = GameCLI.prompt_column_move()
                if game.make_move(col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
        elif isinstance(player, ConnectFour.AIPlayer):
            print(other_strings["thinking"])
            sleep(2)
            col = player.move(game.board)
            game.make_move(col, player.marker)

        GameCLI.clear_screen()
        current_row, current_col = game.move_list[i]
        clear_screen()
        for j in range(current_row):
            temp_board = game.board.get_board(True)
            temp_board.update_square(current_row, current_col, 0)
            temp_board.add_to_square(j, current_col, player.marker)
            GameCLI.print_board_conect4(temp_board.get_board(), connect4_strings["boardline"])
            sleep(0.05)
            clear_screen()

        GameCLI.print_board_conect4(game.board.get_board(), connect4_strings["boardline"])
        if i >= 6 and game.check_winner():
            sleep(1)
            if player.marker == "y":
                GameCLI.print_game_over(other_strings["gameover"])
            else:
                GameCLI.print_game_over(other_strings["redwinner"])
            GameCLI.print_board_conect4(game.board.get_board(), connect4_strings["boardline"])
            break
        print()
        GameCLI.print_current_move(name, *game.move_list[i])
    game.update_winner_info()
    game.update_players_stats()
    game.print_winner()
    # winner = game.get_winner_attributes()
    # GameCLI.print_winner_info(*winner)

def run():
    set_console_window_size(100, 40)
    play_game(set_up_game())
    exit()

    test = ConnectFour()
    test.make_move(0, "r")
    test.make_move(0, "y")
    test.make_move(6, "y")
    test.make_move(6, "r")
    test.make_move(7, "y")
    test.make_move(3, "y")
    test.make_move(3, "y")
    test.make_move(3, "y")
    test.make_move(4, "y")
    test.make_move(4, "y")
    test.make_move(4, "r")
    test.make_move(1, "r")
    test.make_move(2, "r")
    test.make_move(5, "r")

    print_board(test.board.get_board(), LINE)
    # print(test.board.get_rows())
    # testboard = board_translator(test.board.get_board())
    # print(len(testboard[-1]))
    # print(testboard[-1][0].value)
    # for sq  in testboard[-2][0].value:
    #     print(len(sq))
    # print(len(BOARDLINE_CONNECT4))


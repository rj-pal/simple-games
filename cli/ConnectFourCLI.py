from games.game import ConnectFour
from utils.strings import BOARDLINE_CONNECT4
from utils.clitools import * #set_console_window_size, print_board

LINE = BOARDLINE_CONNECT4

def run():
    set_console_window_size(100, 40)

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


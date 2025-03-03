from games.Game import ConnectFour
from utils.display import set_console_window_size, print_board

LINE = "* " * 44 + "*" # for Connect 4

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

    print_board(test.board.get_board(), LINE)

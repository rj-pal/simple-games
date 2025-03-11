from games.Game import ConnectFour
from utils.strings import BOARDLINE_CONNECT4
from utils.display import Display #set_console_window_size, print_board

LINE = BOARDLINE_CONNECT4
display = Display()

def run():
    display.set_console_window_size(100, 40)

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

    display.print_board(test.board.get_board(), LINE)

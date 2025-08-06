from games.games import ConnectFour
from utils.clitools import print_board

test = ConnectFour()
print("MMMM")
print(test.get_player(0).name)
print(test.get_current_player().name)
print("MNNNNNNN")
board = test.board
board.add_to_square(5, 1, "y")
board.add_to_square(5, 0, "y")
board.add_to_square(4, 0, "r")
print(board.__repr__())
board_copy = board.get_board(True)
print(board_copy.__repr__())
board_copy.add_to_square(3, 0, "r")
board_copy.add_to_square(2, 0, "r")
print(board)
print(board_copy.__repr__())
print(board.__repr__())
print
exit()
# print(test.board)
board = test.board.get_board(True)
print(board)
# print_board(test.board.get_board(True).get_board(), "Connect4")
# board = test.board.get_board(True)
# board.make_move(3, "r")
# print(board)
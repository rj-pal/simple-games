from games.game import ConnectFour

test = ConnectFour()
test.create_ai_player()
# print(test.height_list)

# test.make_move(0,"r")
test.make_move(1,"y")
# test.make_move(2,"y")
# test.make_move(3,"y")
test.make_move(4,"r")
test.make_move(5,"r")
# test.make_move(6,"y")
test.make_move(0,"r")
# test.make_move(1,"r")
# test.make_move(2,"r")
test.make_move(2,"r")
test.make_move(2,"r")
# test.make_move(3,"r")
# test.make_move(4,"r")
# test.make_move(4,"y")
# test.make_move(5,"r")
# test.make_move(6,"r")
print(test.board)
player = test.players[1]
player
# print(test.board.get_diagonal_line(3, 3, 3,"left"))
# for position in player.get_empty_move_positions():
#     print(test.board.get_square_value(*position))
player.win_or_block()
# exit()

# for i in range(test.board.rows):
#     print(test.board.get_diagonal_line(i,0,4,"right"))
# print(test.board.get_diagonal_line(2, 5,4,"left"))
# print("OUT OF BOUNDS OR NOT")
# print(test.board.get_diagonal_line(4, 4, 2,"right"))
# print("LEFT TEST")
# for i in range(test.board.columns):
#     print(test.board.get_diagonal_line(4,i,3,"left"))

# print("RIGHT TEST")
# for i in range(test.board.columns):
#     print(test.board.get_diagonal_line(4,i,3,"right"))
exit()

    # test = TicTacToe()
    # test.create_ai_player("Testing Robot", None)
    # # test.print_stats()
    # test.make_move(0,1,"o")
    # print(test.board)
    # print(test.board.get_rows())
    # print(test.board.get_columns())
    # print(test.board.get_diagonals(3, "right"))
    # row_1 = test.board.get_rows()[0]
    # print(row_1)
    # print(LineChecker.two_blanks(row_1, "o", 1))
    # robot = test.players[1]
    
    # test.reset_board()
    # test.make_move(0,2,"o")
    # test.make_move(1,1,"o")
    # test.make_move(2,0,"o")
    # print(robot.two_blanks(test.board))
    # print(test.check_winner())
    # test.update_winner_info()
    # test.print_winner()
    # # print(test)

    # exit()
    # test = ConnectFour()
    # test.create_ai_player()
    # print(test.height_list)

    # # test.make_move(0,"r")
    # test.make_move(1,"y")
    # test.make_move(2,"y")
    # test.make_move(3,"y")
    # test.make_move(4,"r")
    # test.make_move(5,"r")
    # test.make_move(6,"y")
    # test.make_move(0,"r")
    # # test.make_move(1,"r")
    # test.make_move(2,"r")
    # test.make_move(2,"r")
    # test.make_move(2,"r")
    # test.make_move(3,"r")
    # test.make_move(4,"r")
    # # test.make_move(5,"r")
    # # test.make_move(6,"r")
    # print(test.board)
    # # print(test.board.get_diagonals(7, 'right'))
    # print(test.check_winner())
    # line = LineChecker(test.board)
    # last_row = test.board.get_rows()[-2]
    # print(last_row)
    # line_dict = line.two_blanks(last_row, "r", 2)
    # print(line_dict)
    # print(test.height_list)
    # player = test.players[1]
    # print(player.win_or_block(test.board))
    # # print(test._win.check_rows(4))
    # print(line_dict.get("y")[0]["window"])
    
    # exit()
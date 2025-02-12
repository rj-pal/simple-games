from Board import Board, WinChecker, winner_info


test = Board(6, 7)

# Fill the bottom row (row index 5) with "b"
for col in range(7):
    test.update_square(5, col, "b")

print(test)

win = WinChecker(test)
result = win.check_for_winner(4)  # Standard Connect 4 win condition

if result:
    a, b, c, d = result
    winner_info(a, b, c, d)
else:
    print("No winner found.")

test.reset_board()




test = Board(3, 8)
test.update_square(0, 0, "x")
test.update_square(0, 1, "x")
test.update_square(0, 2, "x")
test.update_square(1, 1, "o")
test.update_square(2, 2, "o")
print(test)


win = WinChecker(test)
result = win.check_for_winner(2)
if result:
    a, b, c, d = result
    winner_info(a, b, c, d)
else:
    print("No winner yet.")

test.reset_board()
exit()
test = Board(3, 4)
test.update_square(0, 2, "x")
test.update_square(0, 3, "x")
# test.update_square(1, 0, "o")
# test.update_square(1, 1, "o")
print(test)

win = WinChecker(test)
result = win.check_for_winner(2)
if result:
    a, b, c, d = result
    winner_info(a, b, c, d)
else:
    print("No winner yet.")

test.reset_board()



exit()




test=Board(6,7)
test.update_square(2,3,"x")
test.update_square(3,3,"x")
test.update_square(4,3,"x")
test.update_square(5,3,"x")
test.update_square(4, 6, "o")
print(test)
win = WinChecker(test)
a, b, c ,d = win.check_for_winner(4)
winner_info(a, b, c, d)
test.reset_board()


# Right diagonal winner configuration (from top-left to bottom-right)
test.update_square(0, 0, "x")
test.update_square(1, 1, "x")
test.update_square(2, 2, "x")
test.update_square(3, 3, "x")
test.update_square(4, 6, "o")
print(test)
a, b, c ,d = win.check_for_winner(4)
winner_info(a, b, c, d)

# Left diagonal winner (random position from top-right to bottom-left)
test.reset_board()
test.update_square(2, 4, "x")  # First "x" in the diagonal
test.update_square(3, 3, "x")  # Second "x" in the diagonal
test.update_square(4, 2, "x")  # Third "x" in the diagonal
test.update_square(5, 1, "x")  # Fourth "x" in the diagonal
test.update_square(4, 6, "o")  # Just a random "o" in another spot
print(test)
a, b, c ,d = win.check_for_winner(4)
winner_info(a, b, c, d)

# Right diagonal winner (random position from top-left to bottom-right)
test.reset_board()
test.update_square(1, 1, "x")  # First "x" in the diagonal
test.update_square(2, 2, "x")  # Second "x" in the diagonal
test.update_square(3, 3, "x")  # Third "x" in the diagonal
test.update_square(4, 4, "x")  # Fourth "x" in the diagonal
test.update_square(5, 0, "o")  # Just a random "o" in another spot
print(test)
a, b, c ,d = win.check_for_winner(4)
winner_info(a, b, c, d)
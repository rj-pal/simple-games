from Board import Board, WinChecker, winner_info

WinChecker()

# Visualizations of the Board Unit Tests

# Basic Board Functionality Tests
B=Board(3,3)
B.add_to_square(0, 0, "o")
B.add_to_square(1, 2, "x")
B.add_to_square(2, 0, "o")
print(B)
print(B.get_rows())
print(B.get_columns())
print(B.get_diagonals(3,"right"))
print(B.get_diagonals(3,"left"))
print(B.get_diagonals(2,"right"))
print(B.get_diagonals(2,"left"))
print(B.get_diagonals(1, "left")) # This goes right to left


def print_winner(win_object, win_number):
    """Requires Winchecker function. Returns any winner information as string."""
    result = win_object.check_for_winner(win_number) 
    if result:
        winner_stats = win_object.get_win_info()
        winner_info(winner_stats)
        print(f"Winning Condition: {win_number}-in-a-row.")
    else:
        print("No winner found.")


# Testing winner condition in standard 6x7 Connect Four board
test = Board(6, 7)

# Fill the bottom row (row index 5) with "b" to check for a 4-in-a-row win 
for col in range(7):
    test.update_square(5, col, "b")
print(test.board)
print(test)

win = WinChecker(test)
print_winner(win, 4)  # Standard Connect 4 win condition of 4 in a row


# Testing winner condition in non-standard boards. This is to make sure the diagonal win checking is functional
# Make sure it does not through error for various sized win conditions that do not fit on a board

test = Board(3, 8)
test.update_square(0, 0, "b")
test.update_square(0, 1, "b")
test.update_square(0, 2, "b")
test.update_square(1, 1, "r")
test.update_square(2, 2, "r")
print(test)


win = WinChecker(test)
print_winner(win, 2)
win.reset_win_info()
# print_winner(win, 10)
win.reset_win_info()
test.reset_board()
test.update_square(0, 0, "b")
test.update_square(1, 1, "r")
test.update_square(2, 2, "r")
print(test)
print_winner(win, 2)



test = Board(6, 7)
win = WinChecker(test)
# Right diagonal winner configuration (from top-left to bottom-right)
test.update_square(0, 0, "b")
test.update_square(1, 1, "b")
test.update_square(2, 2, "b")
test.update_square(3, 3, "b")
test.update_square(4, 6, "r")
print(test)
print_winner(win, 2)
win.reset_win_info()
print_winner(win, 4)
win.reset_win_info()
print_winner(win, 5)


# Left diagonal winner (random position from top-right to bottom-left) with X and Os
test.reset_board()
test.update_square(2, 4, "x")  # First "x" in the diagonal
test.update_square(3, 3, "x")  # Second "x" in the diagonal
test.update_square(4, 2, "x")  # Third "x" in the diagonal
test.update_square(5, 1, "x")  # Fourth "x" in the diagonal
test.update_square(4, 6, "o")  # Just a random "o" in another spot
print(test)
print_winner(win, 4)

# Right diagonal winner (random position from top-left to bottom-right)
test.reset_board()
test.update_square(1, 1, "x")  # First "x" in the diagonal
test.update_square(2, 2, "x")  # Second "x" in the diagonal
test.update_square(3, 3, "x")  # Third "x" in the diagonal
test.update_square(4, 4, "x")  # Fourth "x" in the diagonal
test.update_square(5, 0, "o")  # Just a random "o" in another spot
print(test)
print_winner(win, 4)
from typing import Union, Optional
from collections import Counter

def int_converter(number, columns):
    return divmod(number, columns)

def winner_info(a, b, c, d):
    print(f"Winner {a} is type {b} in Row {c + 1} and Column {d + 1}")

class Board:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.board: list[list[Union[int, str]]] = self._initialize_board()
    
    def _initialize_board(self) -> list[list[Union[int, str]]]:
        return [[0] * self.columns for _ in range(self.rows)]

    def reset_board(self) -> None:
        self.board = self._initialize_board()

    def get_board(self) -> list[list[Union[int, str]]]:
        # Return a deep copy to ensure immutability
        from copy import deepcopy
        return deepcopy(self.board)
    
    def get_rows(self) -> list[list[int]]:
        return self.board
    
    def get_columns(self) -> list[list[int]]:
        return [list(col) for col in zip(*self.board)]
    
    def get_diagonals(self, dimension: int, direction: str) -> list[list[int]]:
        if dimension > min(self.rows, self.columns):
            return []
        diagonals = []
        for i in range(self.rows - dimension + 1):
            for j in range(self.columns - dimension + 1):
                if direction == "right":
                    diagonals.append([self.board[i + n][j + n] for n in range(dimension)])
                elif direction == "left":
                    diagonals.append([self.board[i + n][(self.columns - 1) - (j + n)] for n in range(dimension)])
        return diagonals
    
    def square_is_occupied(self, row: int, column: int) -> bool:
        return self.board[row][column] != 0
    
    def add_to_square(self, row: int, column: int, value: Union[int, str]) -> bool:
        if 0 <= row < self.rows and 0 <= column < self.columns:
            if not self.square_is_occupied(row, column):
                self.board[row][column] = value
                return True
        return False
    
    def update_square(self, row: int, column: int, value: Union[int, str]) -> bool:
        """Updates a square regardless of occupancy. Returns True if successful, False otherwise."""
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.board[row][column] = value  # Allow modification
            return True
        return False  # Invalid index
    
    def __str__(self) -> str:
        return "\n".join([" ".join(str(cell) for cell in row) for row in self.board])
    
    def __repr__(self) -> str:
        return f"Board({self.rows}x{self.columns})\n{self.__str__()}"

class WinChecker:
    def __init__(self, board: Board):
        self.board = board
        self.win_marker = None
        self.win_type = None
        self.win_row = None
        self.win_column = None

    def get_win_info(self):
        return self.win_marker, self.win_type, self.win_row, self.win_column
    
    def _update_win_info(self, marker: Union[int, str], win_type: str, win_row: int, win_column: int):
        self.win_marker = marker
        self.win_type = win_type 
        self.win_row = win_row
        self.win_column = win_column

    def _check_win(self, line: list[Union[int, str]], win_value: int) -> Optional[Union[int, str]]:
        counter = Counter(line)
        for key, value in counter.items():
            if value >= win_value and key != 0:
                return key
        # value, count = counter.most_common(1)[0]
        # if count >= win_value and value != 0:
        #     return value
        return None
    
    def _check_rows(self, win_value: int) -> Optional[tuple]:
        for r, row in enumerate(self.board.get_rows()):
            if winner := self._check_win(row, win_value):
                c = row.index(winner)
                return winner, "row", r, c
    
    def _check_columns(self, win_value: int) -> Optional[tuple]:
        for c, column in enumerate(self.board.get_columns()):
            if winner := self._check_win(column, win_value):
                r = column.index(winner)
                return winner, "column", r, c
    
    def _check_diagonals(self, win_value: int) -> Optional[tuple]:
        for l, line in enumerate(self.board.get_diagonals(win_value, "right")):
            if winner := self._check_win(line, win_value):
                r, c = int_converter(l, self.board.columns - win_value + 1)
                return winner, "right_diagonal", r, c
        for l, line in enumerate(self.board.get_diagonals(win_value, "left")):
            if winner := self._check_win(line, win_value):
                r, c = int_converter(l, self.board.columns - win_value + 1)
                c = self.board.columns - 1 - c
                return winner, "left_diagonal", r, c
    
    def check_for_winner(self, win_value: int=3) -> Optional[tuple]:
        # if win_value <= max(self.board.rows / 2, self.board.columns / 2):
        #     raise ValueError(f"Invalid win condition: {win_value} is too small for this board size "
        #                  f"({self.board.rows}x{self.board.columns}). "
        #                  f"win_value must be greater than {int(max(self.board.rows / 2, self.board.columns / 2) // 1)}")
        for check_func in (self._check_rows, self._check_columns, self._check_diagonals):
            if winner_found := check_func(win_value):
                self._update_win_info(*winner_found)
                return True
        return False


# from typing import Union, Optional
# from collections import Counter

# def int_converter(number, columns):
#     return divmod(number, columns)

# def winner_info(a, b, c, d):
#     print(f"Winner {a} is type {b} in Row {c + 1} and Column {d + 1}")

   
# class Board:
#     def __init__(self, rows: int, columns: int):
#         self.rows = rows
#         self.columns = columns
#         self.board: list[list[Union[int, str]]] = self._initialize_board()
    
#     def _initialize_board(self) -> list[list[Union[int, str]]]:
#         """Initialize board in empty state."""
#         return [[0] * self.columns for _ in range(self.rows)]
    
#     def get_rows(self) -> list[list[int]]:
#         """Make a list of all the rows in the board."""
#         return self.board
    
#     def get_columns(self) -> list[list[int]]:
#         """Make a list of all columns in the board."""
#         return [list(col) for col in zip(*self.board)]

#     def get_diagonals(self, dimension: int, direction: str) -> list[list[int]]:
#         """Make a list of all diagonals of given dimension in the 'right' or 'left' direction in the board."""
        
#         # If the requested dimension is larger than the smallest board side, return an empty list
#         if dimension > min(self.rows, self.columns):
#             return []

#         diagonals = []

#         # Iterate over all possible starting positions for diagonals
#         # self.rows - dimension + 1 ensures we do not exceed row limits when forming diagonals
#         for i in range(self.rows - dimension + 1):  
#             # self.columns - dimension + 1 ensures we do not exceed column limits when forming diagonals
#             for j in range(self.columns - dimension + 1):  

#                 if direction == "right":
#                     # Collect a diagonal of 'dimension' length going in the right-down direction
#                     diagonals.append([self.board[i + n][j + n] for n in range(dimension)])

#                 elif direction == "left":
#                     # (self.columns - 1) - (j + n) calculates the column index for left diagonals.
#                     # It mirrors the diagonal positions from right to left.
#                     diagonals.append([self.board[i + n][(self.columns - 1) - (j + n)] for n in range(dimension)])

#         return diagonals



#     def get_diagonals(self, dimension: int, direction: str) -> list[list[int]]:
#         """Make a list of all diagonals of given dimension in the 'right' or 'left' direction in the board."""
#         if dimension > min(self.rows, self.columns):
#             return []
#         diagonals = []
#         for i in range(self.rows - dimension + 1):
#             for j in range(self.columns - dimension + 1):
#                 if direction == "right":
#                     diagonals.append([self.board[i + n][j + n] for n in range(dimension)])
#                 elif direction == "left":
#                     diagonals.append([self.board[i + n][(self.columns - 1) - (j + n)] for n in range(dimension)])
#         return diagonals
    
#     def square_is_occupied(self, row: int, column: int) -> bool:
#         """Checks if a square is empty."""
#         return self.board[row][column] != 0
    
#     def add_to_square(self, row: int, column: int, value: Union[int, str]) -> bool:
#         """Adds a value to an empty square. Returns True if successful, False otherwise."""
#         if 0 <= row < self.rows and 0 <= column < self.columns:
#             if not self.square_is_occupied(row, column):  # Only add if empty
#                 self.board[row][column] = value
#                 return True
#         return False  # Move invalid or square occupied

#     def update_square(self, row: int, column: int, value: Union[int, str]) -> bool:
#         """Updates a square regardless of occupancy. Returns True if successful, False otherwise."""
#         if 0 <= row < self.rows and 0 <= column < self.columns:
#             self.board[row][column] = value  # Allow modification
#             return True
#         return False  # Invalid index

#     def reset_board(self) -> None:
#         """Returns board to empty state."""
#         self.board = self._initialize_board()

#     def _check_win(self, line: list[Union[int, str]], win_value: int) -> Optional[Union[int, str]]:
#         """Checks if a line has all the same markers to see if the game has been won."""
#         counter = Counter(line)
#         value, count = counter.most_common(1)[0]
#         if count == win_value and value != 0:
#             return value  # Return the value of the winning marker (e.g., 'x' or 'o')
#         return None  # No winner


#     def _check_rows(self, win_value: int) -> Optional[Union[int, str]]:
#         """Checks for winner in rows. Uses returned Square object to update the winner attributes. False if no Square
#         object is assigned. """
#         for r, row in enumerate(self.get_rows()):
#             if winner := self._check_win(row, win_value):
#                 # self._update_winner_info(winner, "row", r)
#                 c = row.index(winner)
#                 return winner, "row", r, c

#     def _check_columns(self, win_value: int) -> Optional[Union[int, str]]:
#         """Checks for winner in columns. Uses returned Square object to update winner attributes. False if no Square
#         object is assigned. """
#         for c, column in enumerate(self.get_columns()):
#             if winner := self._check_win(column, win_value):
#                 print(column)
#                 # self._update_winner_info(winner, "col", c)
#                 r = column.index(winner)
#                 return winner, "column", r, c

#     def _check_diagonals(self, win_value: int) -> Optional[Union[int, str]]:
#         """Checks for winner in diagonals. Uses returned Square object to update winner attributes. False if no
#         Square object is assigned. """
#         for l, line in enumerate(self.get_diagonals(win_value, "right")):
#             if winner := self._check_win(line, win_value):
#             # self._update_winner_info(winner, "right_diag")
#                 r, c = int_converter(l, self.columns - win_value + 1)
#                 return winner, "right_diagonal", r, c
#         for l, line in enumerate(self.get_diagonals(win_value, "left")):
#             if winner := self._check_win(line, win_value):
#             # self._update_winner_info(winner, "left_diag")
#                 r, c = int_converter(l, self.columns - win_value + 1)
#                 c = self.columns - 1 - c
#                 return winner, "left_diagonal", r, c
            
#     def check_for_winner(self, win_value: int) -> Optional[Union[int, str]]:
#         """Checks if the game has been won in a row, column, or diagonal."""
#         for check_func in (self._check_rows, self._check_columns, self._check_diagonals):
#             if winner_found := check_func(win_value):
#                 return winner_found
#         return None  
    
#     def __str__(self) -> str:
#         """Returns a more readable board representation."""
#         return "\n".join([" ".join(str(cell) for cell in row) for row in self.board])

#     def __repr__(self) -> str:
#         return f"Board({self.rows}x{self.columns})\n{self.__str__()}"


# print(test._check_rows(4))
# print(test._check_columns(4))

# for row in test.get_rows():
#     print(row)
# diagonals = test.get_diagonals(4, "right")
# for i in diagonals:
#     print(i)
# diagonals = test.get_diagonals(4, "left")
# for i in diagonals:
#     print(i)
# test.reset_board()
# for row in test.get_rows():
#     print(row)

# diagonals = test.get_right_diagonals(4)
# for i in diagonals:
#     print(i)


# def board(rows: int, columns: int):
#     board = []
#     for i in range(rows):
#         if i == 1:
#             board.append(["x" for _ in range(columns)])
#         else:
#             board.append([0 for _ in range(columns)])
#     return board

# def get_rows(self) -> list[list]:
#         """Returns a list of the rows of Square objects. It is the 2D game Board object list of lists."""
#         return self.board

#     def get_columns(self) -> list[list]:
#         """Returns a list of the columns of Square objects. It is a list of lists of each row position from
#         the Board object using zipped row positions and mapped into a list for consistency with rows."""
#         return list(map(list, zip(*self.board)))   
    
#     def get_left_diagonal(self) -> list:
#         """Returns a list of the left diagonal of Square objects. It is a sliced list of the game Board object."""
#         return list(self.board[i][-(i + 1)] for i in range(len(self.board)))
    
#     def get_right_diagonal(self) -> list:
#         """Returns a list of the right diagonal of Square objects. It is a sliced list of the game Board object."""
#         return list(self.board[i][i] for i in range(len(self.board)))

#     def square_is_occupied(self, row: int, column: int) -> bool:
#         """Checks if a square is occupied by an Ex or Oh."""
#         return self.board[row][column] != 0

#     def update_square(self, row: int, column: int, square: str) -> None:
#         """Updates the square on the board to an Ex or Oh from the Square class."""
#         self.board[row][column] = square

#     def update_board(self, row: int, column: int, marker: str) -> None:
#         """Updates the board with the last played square."""
#         self.board.update_square(row, column, marker)

#     def reset_board(self) -> None:
#         """Sets each square in the board to a blank."""
#         self.board = [[0] * 3 for _ in range(3)]

# board = [
#     [ 1,  2,  3,  4],
#     [ 5,  6,  7,  8],
#     [ 9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]
        # for i in range(self.rows):
        #     if i == 1 or i == 5:
        #         board.append([8//n for n in range(1, self.columns + 1)])
        #     else:
        #         board.append([0 for _ in range(self.columns)])
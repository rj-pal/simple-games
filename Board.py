class Board:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.board = self._initialize_board()
    
    def _initialize_board(self) -> list[list]:
        board = []
        for i in range(self.rows):
            if i == 1 or i == 5:
                board.append([1 for _ in range(self.columns)])
            else:
                board.append([0 for _ in range(self.columns)])
        return board
    
    def get_rows(self) -> list[list]:
        return self.board
    
    def get_columns(self) -> list[list]:
        return list(map(list, zip(*self.board)))
    
    def get_left_diagonal(self) -> list:
        return [self.board[i][-(i + 1)] for i in range(len(self.board))]
    
    def get_right_diagonals(self, dimension: int) -> list:
        column_space = self.rows - dimension + 1
        row_space = self.columns - dimension + 1
        print({column_space, row_space})
        right_diagonals = []
        for i in range(column_space):
            
            for j in range(row_space):
                print(f"ROW {i}, COL{j}")
                right_diagonals.append([self.board[i + n][j+ n] for n in range(4)])
                # print(right_diagonals)
        return right_diagonals

    def get_right_diagonal(self) -> list:
        return [self.board[i][i] for i in range(len(self.board))]
    
    def square_is_occupied(self, row: int, column: int) -> bool:
        return self.board[row][column] != 0
    
    def update_square(self, row: int, column: int, square: str) -> None:
        self.board[row][column] = square
    
    def update_board(self, row: int, column: int, marker: str) -> None:
        self.update_square(row, column, marker)
    
    def reset_board(self) -> None:
        self.board = [[0] * self.columns for _ in range(self.rows)]

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the board for information purposes only."""
        return f'Board:\n{str(self.board)}'

test=Board(6,7)
for row in test.get_rows():
    print(row)
diagonals = test.get_right_diagonals(4)

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
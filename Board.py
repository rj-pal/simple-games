from typing import Union, Optional
from collections import Counter

def int_converter(number, columns):
    return divmod(number, columns)

def winner_info(winner_dictionary):
    print(f"Winning player marker {winner_dictionary['marker']} is win of type {winner_dictionary['type']} in "
      f"Row {winner_dictionary['row'] + 1} and Column {winner_dictionary['column'] + 1}")


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
        return {
            "marker": self.win_marker,
            "type": self.win_type,
            "row": self.win_row,
            "column": self.win_column
        }

    def get_win_info_as_tuple(self):
        return self.win_marker, self.win_type, self.win_row, self.win_column
    
    def reset_win_info(self):
        self._update_win_info()
    
    def _update_win_info(self, marker: Union[int, str]=None, win_type: str=None, win_row: int=None, win_column: int=None):
        self.win_marker = marker
        self.win_type = win_type 
        self.win_row = win_row
        self.win_column = win_column

    def _check_win(self, line: list[Union[int, str]], win_value: int) -> Optional[Union[int, str]]:
        counter = Counter(line)
        for key, value in counter.items():
            if value >= win_value and key != 0:
                return key
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
        if win_value > max(self.board.rows, self.board.columns):
            raise ValueError(f"Invalid win condition: {win_value} is too large for a board of size "
                         f"({self.board.rows}x{self.board.columns}). It must fit within given board dimensions. ")
        for check_func in (self._check_rows, self._check_columns, self._check_diagonals):
            if winner_found := check_func(win_value):
                self._update_win_info(*winner_found)
                return True
        return False
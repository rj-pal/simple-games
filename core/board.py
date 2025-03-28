from typing import Union, Optional
from copy import deepcopy
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

    def get_board(self, mutable: bool = False) -> Union[list[list[Union[int, str]]], "Board"]:
        """
        Returns either a deep copy of the board that is immutable, used for displaying the board,  or a deep copy of 
        the entire Board object that is mutable, that is used to create a snap shot of the board for flash displaying.
        
        parametre- mutable: If True, returns a full Board copy. Otherwise, returns a deep copy of board data.
        """
        return deepcopy(self) if mutable else deepcopy(self.board)
    
    def get_rows(self) -> list[list[int]]:
        return self.board
    
    def get_columns(self) -> list[list[int]]:
        return [list(col) for col in zip(*self.board)]
    

    def get_diagonal_line(self, row, column, length, direction):
        if row + length > self.rows:
            return []
        if direction == "right":
            if column + length > self.columns:
                return []
            return [self.board[row + n][column + n] for n in range(length)]
        elif direction == "left":
            if column < self.columns - length:
                return []
            return [self.board[row + n][column - n] for n in range(length)]
    
    def get_diagonals(self, length: int, direction: str) -> list[list[int]]:
        """Gets every diagonal from the board of a fixed size (length) starting from left to right 
        if direction is 'right' and right to left if direction is 'left'. Diagonal length must fit 
        on the board."""
        if length > min(self.rows, self.columns):
            return []
        diagonals = []
        for i in range(self.rows - length + 1):
            for j in range(self.columns - length + 1):
                if direction == "right":
                    diagonals.append([self.board[i + n][j + n] for n in range(length)])
                elif direction == "left":
                    diagonals.append([self.board[i + n][(self.columns - 1) - (j + n)] for n in range(length)])
        return diagonals
    
    def square_is_occupied(self, row: int, column: int) -> bool:
        return self.board[row][column] != 0
    
    def get_square_value(self, row: int, column: int) -> Union[int, str]:
        return self.board[row][column]
    
    def add_to_square(self, row: int, column: int, value: Union[int, str]) -> bool:
        if 0 <= row < self.rows and 0 <= column < self.columns:
            if not self.square_is_occupied(row, column):
                self.board[row][column] = value
                return True
        return False  # Invalid index was passe
    
    def update_square(self, row: int, column: int, value: Union[int, str]) -> bool:
        """Updates a square regardless of occupancy. Returns True if successful, False otherwise."""
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.board[row][column] = value  # Allows modification even if square is occupied
            return True
        return False  # Invalid index was passed
    
    def __deepcopy__(self, memo):
        """Creates a deep copy of the Board instance, avoiding redundant copies using memo."""
        if id(self) in memo:
            return memo[id(self)]  # Return existing copy

        new_board = Board(self.rows, self.columns)
        memo[id(self)] = new_board  # Store in memo
 
        new_board.board = deepcopy(self.board, memo) # Deep copy the board data that is immutable so as not to affect game play
        return new_board
    
    def __str__(self) -> str:
        return "\n".join([" ".join(str(cell) for cell in row) for row in self.board]) # basic string matrix representation of the board
    
    def __repr__(self) -> str:
        return f"Board({self.rows}x{self.columns})\n{self.__str__()}"

class LineChecker:
    def __init__(self, board: Board, win_value: int=3):
        self.board = board
        self.win_checker = self._check_for_winner # win_checker attribute used to help encapsulate the methods used for win checking

        self.win_value = win_value
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
    
    @staticmethod
    def line_check(sequence, target_element, target_count, other_element, other_count, window_size, all_occurrences=False):
        """
        Scans a sequence to find all fixed-size subsets that contain:
        - `target_element` exactly `target_count` times
        - `other_element` exactly `other_count` times
        - If `other_element` is 'any', it allows any non-`target_element` value to match `other_count` times.
        
        Parameters:
        sequence (list): The input list to scan.
        target_element (any): The specific element that must appear `target_count` times.
        target_count (int): Number of times `target_element` must appear in each valid subset.
        other_element (any or "any"): The second required element (or "any" for flexibility).
        other_count (int): Number of times `other_element` must appear in each valid subset.
        window_size (int): The fixed size of each subset being checked.
        all_occurrences (bool): If True, returns **all** indices of `target_element` in each matching subset.
        
        Returns:
        dict: A dictionary where keys are unique `other_element_master` values.
            Each key maps to a list of dictionaries containing:
                - `"window"`: The index of the window in the sequence.
                - `"window_indices"`: The relative indices of `target_element` within the window.
                - `"absolute_indices"`: The absolute indices of `target_element` in the full sequence.
                - If `all_occurrences=False`: `"first_index"` and `"absolute_index"` are included.
        """

        # Validate inputs
        if window_size > len(sequence):
            raise ValueError("Window size cannot exceed the length of the sequence.")
        if target_count + other_count != window_size:
            raise ValueError("The sum of target_count and other_count must equal the window size.")

        matches = {}  # Dictionary where keys are `other_element_master`
        window_index = 0

        # Sliding window approach
        for i in range(len(sequence) - window_size + 1):
            window = sequence[i: i + window_size]

            target_indices = []
            target_window_indices = []
            other_element_master = other_element
            other_element_count = 0
            other_element_found = False

            # Scan the window
            for j, item in enumerate(window):
                if item == target_element:
                    target_indices.append(i + j)  # Store absolute index of target element
                    target_window_indices.append(j)
                elif other_element == "any":
                    if not other_element_found:
                        other_element_found = True
                        other_element_master = item  # First non-target element becomes the reference
                    if item == other_element_master:
                        other_element_count += 1
                elif item == other_element:
                    other_element_count += 1
                else:
                    break  # Invalid window, stop processing

            # If window is valid, add it to results
            if len(target_indices) == target_count and other_element_count == other_count:
                match_data = {
                    "window": window_index,
                    "window_indices": target_window_indices,
                    "absolute_indices": target_indices
                }

                if not all_occurrences:
                    match_data["first_index"] = target_window_indices[0]
                    match_data["absolute_index"] = target_indices[0]

                # Store in dictionary under `other_element_master` as key for quick look up based on the marker
                if other_element_master not in matches:
                    matches[other_element_master] = []
                matches[other_element_master].append(match_data)

            window_index += 1

        return matches

   
    @staticmethod
    def two_blanks(sequence, marker, size):
        return LineChecker.line_check(sequence, 0, 2, marker, size, size + 2, True)
    

    
    @staticmethod
    def check_all_same(line: list[Union[int, str]], win_value: int) -> Optional[tuple]:
        "Checks if any line has all the same elements that are non-null or zero. Returns the winning marker element."
        if all(element == line[0] for element in line):
            return line[0] if line[0] != 0 else None
    
    def _check_full_rows(self, win_value: int) -> Optional[tuple]:
        for r, row in enumerate(self.board.get_rows()):
            if winner := LineChecker.check_all_same(row, win_value):
                c = row.index(winner)
                return winner, "row", r, c
    
    def _check_full_columns(self, win_value: int) -> Optional[tuple]:
        for c, column in enumerate(self.board.get_columns()):
            if winner := LineChecker.check_all_same(column, win_value):
                r = column.index(winner)
                return winner, "column", r, c
    
    def _check_diagonals(self, win_value: int) -> Optional[tuple]:
        for l, line in enumerate(self.board.get_diagonals(win_value, "right")):
            if winner := LineChecker.check_all_same(line, win_value):
                r, c = int_converter(l, self.board.columns - win_value + 1)
                return winner, "right_diagonal", r, c
        for l, line in enumerate(self.board.get_diagonals(win_value, "left")):
            if winner := LineChecker.check_all_same(line, win_value):
                r, c = int_converter(l, self.board.columns - win_value + 1)
                c = self.board.columns - 1 - c
                return winner, "left_diagonal", r, c
    
    def _check_for_winner(self) -> Optional[tuple]:
        if self.win_value > max(self.board.rows, self.board.columns):
            raise ValueError(f"Invalid win condition: {self.win_value} is too large for a board of size "
                         f"({self.board.rows}x{self.board.columns}). It must fit within given board dimensions. ")
        for check_func in (self._check_full_rows, self._check_full_columns, self._check_diagonals):
            if winner_found := check_func(self.win_value):
                self._update_win_info(*winner_found)
                return True
        return False
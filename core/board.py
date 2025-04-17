from typing import Union, Optional
from copy import deepcopy
from collections import Counter

def int_converter(number, columns):
    return divmod(number, columns)

def winner_info(winner_dictionary):
    print(f"Winning player marker {winner_dictionary['marker']} is win of type {winner_dictionary['type']} in "
      f"Row {winner_dictionary['row'] + 1} and Column {winner_dictionary['column'] + 1}")

from typing import Union

class Board:
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._board: list[list[Union[int, str]]] = self._initialize_board()
    
    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns
    
    def _initialize_board(self) -> list[list[Union[int, str]]]:
        return [[0] * self._columns for _ in range(self._rows)]
    
    def reset_board(self) -> None:
        self._board = self._initialize_board()
    
    def is_on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self._rows and 0 <= col < self._columns
    
    def square_is_occupied(self, row: int, column: int) -> Union[bool, None]:
        if self.is_on_board(row, column):
            return self._board[row][column] != 0
        return None
    
    def get_square_value(self, row: int, column: int) -> Union[int, str, None]:
        if self.is_on_board(row, column):
            return self._board[row][column]
        return None
    
    def add_to_square(self, row: int, column: int, value: Union[int, str]) -> Union[bool, None]:
        if self.is_on_board(row, column):
            if not self.square_is_occupied(row, column):
                self._board[row][column] = value
                return True
            return False
        return None
    
    def update_square(self, row: int, column: int, value: Union[int, str]) -> Union[bool, None]:
        """Updates a square regardless of occupancy. Returns True if successful, False otherwise."""
        if self.is_on_board(row, column):
            self._board[row][column] = value  # Allows modification even if square is occupied
            return True
        return None  # Invalid index was passed

    # @property
    # def board(self) -> list[list[Union[int, str]]]:
    #     return [row[:] for row in self._board]  # Returns a copy



# class Board:
#     def __init__(self, rows: int, columns: int):
#         self._rows = rows
#         self._columns = columns
#         self._board: list[list[Union[int, str]]] = self._initialize_board()
    
#     def _initialize_board(self) -> list[list[Union[int, str]]]:
#         return [[0] * self._columns for _ in range(self._rows)]
    
#     def reset_board(self) -> None:
#         self._board = self._initialize_board()
    
#     def is_on_board(self, row, col):
#         return 0 <= row < self._rows and 0 <= col < self._columns
    
#     def square_is_occupied(self, row: int, column: int) -> bool:
#         if self.is_on_board(row, column):
#             return self._board[row][column] != 0
#         return None
    
#     def get_square_value(self, row: int, column: int) -> Union[int, str]:
#         if self.is_on_board(row, column):
#             return self._board[row][column]
#         return None
    
#     def add_to_square(self, row: int, column: int, value: Union[int, str]) -> bool:
#         if self.is_on_board(row, column):
#             if not self.square_is_occupied(row, column):
#                 self._board[row][column] = value
#                 return True
#         return False  # Invalid index was passe
    
    def get_board(self, mutable: bool = False) -> Union[list[list[Union[int, str]]], "Board"]:
        """
        Returns current state of the board.

        Args:
            mutable (bool): 
                - If False (default), returns a deep copy of the board (list of lists), safe for viewing only.
                - If True, returns a full deep copy of the Board object, useful for flash states or undo features.

        Returns:
            Union[list[list[Union[int, str]]], Board]: 
                A safe copy of the board data or the whole Board instance.
        """
        return deepcopy(self) if mutable else deepcopy(self._board)

    # def get_board(self, mutable: bool = False) -> Union[list[list[Union[int, str]]], "Board"]:
    #     """
    #     Returns either a deep copy of the board that is immutable, used for displaying the board,  or a deep copy of 
    #     the entire Board object that is mutable, that is used to create a snap shot of the board for flash displaying.
        
    #     Parametre- mutable: If True, returns a full Board copy. Otherwise, returns a deep copy of board data.
    #     """
    #     return deepcopy(self) if mutable else deepcopy(self._board)


    def get_rows(self) -> list[list[Union[int, str]]]:
        return self.get_board()

    def get_columns(self) -> list[list[Union[int, str]]]:
        board_copy = self.get_board()
        return [list(col) for col in zip(*board_copy)]
    
    def get_diagonals(self, length: int, direction: str) -> list[list[Union[int, str]]]:
        """
        Gets all diagonals of a given length from the board.

        Args:
            length (int): Length of each diagonal (must fit on the board).
            direction (str): 'right' for top-left to bottom-right, 'left' for top-right to bottom-left.

        Returns:
            List of diagonals (each a list of board values).
        """
        if length > min(self._rows, self._columns):
            return []

        if direction not in {"right", "left"}:
            raise ValueError("Direction must be either 'right' or 'left'.")

        diagonals = []
        # board_copy = self.get_board()  # Use copied board for safety

        for i in range(self._rows - length + 1):
            for j in range(self._columns - length + 1):
                diagonal = [
                    self.get_square_value(i + n, j + n if direction == "right" else (self._columns - 1) - (j + n) )
                    for n in range(length)
                ]
                # if direction == "right":
                #     diagonal = [self.get_square_value(i + n, j + n) for n in range(length)]
                # else:  # direction == "left"
                #     diagonal = [self.get_square_value(i + n, (self._columns - 1) - (j + n)) for n in range(length)]
                diagonals.append(diagonal)

        return diagonals


    # def get_rows(self) -> list[list[int]]:
    #     return self.get_board()
    
    # def get_columns(self) -> list[list[int]]:
    #     return [list(col) for col in zip(*self._board)]
    

    def get_diagonal_line_down(self, row, column, length, direction):
        if (row + length > self._rows) or (row < 0):
            return []
        if direction == "right":
            if column + length > self._columns:
                return []
            return [self._board[row + n][column + n] for n in range(length)]
        elif direction == "left":
            if column < self._columns - (length + 2): # compensate since going backwards.
                return []
            return [self._board[row + n][column - n] for n in range(length)]

    
    def get_diagonal_line_up(self, row, column, length, direction):
        if (row < length - 1) or (row >= self._rows):  # Ensuring we don't go out of bounds upwards
            return []  
        if direction == "right":
            if (column + length > self._columns) or (column < 0):  # Ensure we don't go out of bounds right
                return []
            return [self._board[row - n][column + n] for n in range(length)]
        elif direction == "left":
            if (column < length - 1) or (column >= self._columns):  # Ensure we don't go out of bounds left
                return []
            # print(row, column )
            return [self._board[row - n][column - n] for n in range(length)]

    
    # def get_diagonals(self, length: int, direction: str) -> list[list[int]]:
    #     """Gets every diagonal from the board of a fixed size (length) starting from left to right 
    #     if direction is 'right' and right to left if direction is 'left'. Diagonal length must fit 
    #     on the board."""
    #     if length > min(self._rows, self._columns):
    #         return []
    #     diagonals = []
    #     for i in range(self._rows - length + 1):
    #         for j in range(self._columns - length + 1):
    #             if direction == "right":
    #                 diagonals.append([self._board[i + n][j + n] for n in range(length)])
    #             elif direction == "left":
    #                 diagonals.append([self._board[i + n][(self._columns - 1) - (j + n)] for n in range(length)])
    #     return diagonals
    
    def is_valid_line_segment(self, row, col, length, direction):
        """
        Checks if a line segment of the given length and direction fits within the board boundaries.

        Args:
            row (int): Starting row index.
            col (int): Starting column index.
            length (int): Length of the segment.
            direction (str): Direction of the segment ('up', 'down', 'left', or 'right').

        Returns:
            bool: True if the segment is within bounds, False otherwise.

        Raises:
            ValueError: If the direction is not one of 'up', 'down', 'left', or 'right'.
        """
        if direction == 'right':
            return col + length <= self._columns
        
        elif direction == 'left':
            return col - length >= 0
        
        elif direction == 'down':
            return row + length <= self._rows

        elif direction == 'up':
            return row - (length - 1) >= 0
        
        else:
            raise ValueError("Direction must be 'right', 'left', 'up', or 'down'")
        
    def get_row_segment(self, row: int, col: int, length: int, right: bool = True) -> Optional[list[Union[int, str]]]:
        """
        Returns a segment from the row starting at (row, col) of the specified length.
        
        Args:
            row (int): Row index to start from.
            col (int): Column index to start from.
            length (int): Number of squares to include.
            right (bool): Direction of segment. If True, go right. If False, go left.

        Returns:
            list[Union[int, str]] or None if the segment length or start position is invalid.
        """
        if not self.is_on_board(row, col) or length <= 0:
            return None

        direction = "right" if right else "left"
        if self.is_valid_line_segment(row, col, length, direction):
            return [
                self.get_square_value(row, col + i if right else col - i)
                for i in range(length)
            ]

        return None
    
    # def get_row_segment(self, row, col, length, right=True):
    #     """Returns a segment from the row starting at (row, col) of the specified length."""
    #     if not self.is_on_board(row, col):
    #         return None
    #     if right:
    #         if self.is_valid_line_segment(row, col, length, 'right'):
    #             return [self.get_square_value(row, col + i) for i in range(length)]
    #     else:
    #         if self.is_valid_line_segment(row, col, length, 'left'):
    #             return [self.get_square_value(row, col - i) for i in range(length)]
    #     return None

    def get_column_segment(self, row, col, length, down=True):
        """
        Returns a segment from the column starting at (row, col) of the specified length.
        
        Args:
            row (int): Row index to start from.
            col (int): Column index to start from.
            length (int): Number of squares to include.
            down (bool): Direction of segment. If True, go down. If False, go up.

        Returns:
            list[Union[int, str]] or None if the segment length or start position is invalid.
        """
        if not self.is_on_board(row, col) or length <= 0:
            return None
        
        direction = 'down' if down else 'up'
        if self.is_valid_line_segment(row, col, length, direction):
            return [
                self.get_square_value(row + i if down else row - 1, col) 
                for i in range(length)
            ]
        return None
        # else:
        #     if self.is_valid_line_segment(row, col, length, 'up'):
        #         return [self.get_square_value(row - i, col) for i in range(length)]
        # return None
        
     
    def get_diagonal_segment(self, row, col, length, up=True, right=True):
        """
        Returns a diagonal segment starting at (row, col) of the specified length.

        Args:
            row (int): Row index to start from.
            col (int): Column index to start from.
            length (int): Number of squares to include.
            up (bool): Vertical direction of the segment. If True, go up. If False, go down.
            right (bool): Horizontal direction of the segment. If True, go right. If False, go left.

        Returns:
            list[Union[int, str]] or None if the segment length or start position is invalid.
        """
        if not self.is_on_board(row, col) or length <= 0:
            return None

        vertical_direction = 'up' if up else 'down'
        horizontal_direction = 'right' if right else 'left'
        if self.is_valid_line_segment(row, col, length, vertical_direction) and self.is_valid_line_segment(row, col, length, horizontal_direction):
            return [
                self.get_square_value(row - i if up else row + i ,col + i if right else col - i)
                for i in range(length)
            ]
        return None
        # if right:
        #     if not self.is_on_board(row, col) or not self.is_valid_line_segment(row, col, length, 'right'):
        #         return None
        #     if up:
        #         if self.is_valid_line_segment(row, col, length, 'up'):
        #             return [self.get_square_value(row - i, col + i) for i in range(length)]
        #     else:
        #         if self.is_valid_line_segment(row, col, length, 'down'):
        #             return [self.get_square_value(row + i, col + i) for i in range(length)]
        #     return None
        # else:
        #     if not self.is_on_board(row, col) or not self.is_valid_line_segment(row, col, length, 'left'):
        #         return None
        #     if up:
        #         if self.is_valid_line_segment(row, col, length, 'up'):
        #             return [self.get_square_value(row - i, col - i) for i in range(length)]
        #     else:
        #         if self.is_valid_line_segment(row, col, length, 'down'):
        #             return [self.get_square_value(row + i, col - i) for i in range(length)]
        #     return None
    
    def __deepcopy__(self, memo):
        """
        Creates a deep copy of the Board instancen for viewing purposes.

        Args:
            memo (dict): Dictionary used to track already copied objects to prevent redundant copies 
                        and handle circular references.

        Returns:
            Board: A new Board instance with duplicated internal state that does not share mutable data 
                with the original.
        """
        if id(self) in memo:
            return memo[id(self)]  # Return existing copy

        new_board = Board(self._rows, self._columns)
        memo[id(self)] = new_board  # Store in memo
 
        new_board.board = deepcopy(self._board, memo) # Deep copy the board data that is immutable so as not to affect game play
        return new_board
   
    def __str__(self) -> str:
        """Returns a string representation of the board as a grid matrix."""
        return "\n".join([" ".join(str(cell) for cell in row) for row in self._board]) # basic string matrix representation of the board
    
    def __repr__(self) -> str:
        """Returns a detailed string with board dimensions and grid content."""
        return f"Board({self._rows}x{self._columns})\n{self.get_board()}"

class LineChecker:
    def __init__(self, board: Board, win_value: int=3):
        self._board = board
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
    

    def check_all_same(segment):
        """Checks if all elements in the given segment are the same and non-zero."""
        if all(element == segment[0] for element in segment) and segment[0] != 0:
            return segment[0]
        return None

    
    @staticmethod
    def check_all_same(line: list[Union[int, str]]) -> Optional[tuple]:
        "Checks if any line has all the same elements that are non-null or zero. Returns the winning marker element."
        if line[0] != 0 and all(element == line[0] for element in line):
            return line[0]
        else:
            return None
    
    def _check_full_rows(self, win_value: int) -> Optional[tuple]:
        for r, row in enumerate(self._board.get_rows()):
            if winner := LineChecker.check_all_same(row):
                c = row.index(winner)
                return winner, "row", r, c
    
    def _check_full_columns(self, win_value: int) -> Optional[tuple]:
        for c, column in enumerate(self._board.get_columns()):
            if winner := LineChecker.check_all_same(column):
                r = column.index(winner)
                return winner, "column", r, c
    
    def _check_diagonals(self, win_value: int) -> Optional[tuple]:
        for l, line in enumerate(self._board.get_diagonals(win_value, "right")):
            if winner := LineChecker.check_all_same(line):
                r, c = int_converter(l, self._board.columns - win_value + 1)
                return winner, "right_diagonal", r, c
        for l, line in enumerate(self._board.get_diagonals(win_value, "left")):
            if winner := LineChecker.check_all_same(line):
                r, c = int_converter(l, self._board.columns - win_value + 1)
                c = self._board.columns - 1 - c
                return winner, "left_diagonal", r, c
    
    def _check_for_winner(self) -> Optional[tuple]:
        if self.win_value > max(self._board.rows, self._board.columns):
            raise ValueError(f"Invalid win condition: {self.win_value} is too large for a board of size "
                         f"({self._board.rows}x{self._board.columns}). It must fit within given board dimensions. ")
        for check_func in (self._check_full_rows, self._check_full_columns, self._check_diagonals):
            if winner_found := check_func(self.win_value):
                self._update_win_info(*winner_found)
                return True
        return False
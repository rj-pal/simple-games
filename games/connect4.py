"""
connect4.py 
Author: Robert Pal
Updated: 2025-08-06

This module contains code for connect4.
"""
from core.board import Board, LineChecker
from core.player import Player
from games.games import int_converter

from random import randint
from typing import List, Tuple, Optional

class ConnectFour:

    def __init__(self, connect_value: int=4, rows: int=6, columns: int=7):
         self.connect_value = connect_value # Options to set the connect_value to play variations of Connect 4 (board size via row and columns should be modified)
         self.rows = rows
         self.columns = columns
         self.board: List[List] = self.create_board() # Public attribute available as mutable copy or nested list data structure for display purposes
         self.move_list: List = []
         self.height_list: List = [self.rows] * self.columns # Tracks how full a column on the board is, for quick move validation and AI strategy
         self.round_count: int = 0
         self.go_first: bool = True
         self._win: LineChecker = self.ConnectFourWinChecker(self.board) # Private attribute for checking winner lines and updating winner attributes.
         self.players = self.create_human_players() # Default to two player mode
         
         self.winner_name: str = None  # Winner attributes used for tracking winner info, stats or display (default to None or -1 when no winner)
         self.winner_marker: str = None
         self.win_type: str = None
         self.win_row: int = -1
         self.win_column: int = -1
         
         self._premove_board_state = None

    @property
    def board_size(self):
        """Read only property based on the number of rows and columns."""
        return self.rows * self.columns

    def create_board(self):
        """Creates board object based on size dimensions of the number of rows and columns."""
        return Board(self.rows, self.columns)

    def create_human_players(self) -> Tuple[Player, Player]:
        """Creates two human players for game play in two player mode."""
        return (
            self.ConnectFourPlayer("Player 1", "r"),
            self.ConnectFourPlayer("Player 2", "y"),
        )
    def create_ai_player(self, difficulty: Optional[bool]=True) -> Tuple[Player, Player]:
        """Creates one human player and one AI player for game play in one player mode."""
        self.players = (
            self.ConnectFourPlayer("Player 1", "r"),
            self.AIPlayer(difficulty=difficulty, game=self),
        )

    def get_current_player(self):
        """Returns the current player based on the round count. Red player moves first and is at index 0 in players list."""
        return self.players[self.round_count % 2] if self.go_first else self.players[self.round_count % 2 - 1]
        

    def _add_ai_players_for_testing(self, difficulty_one: bool=True, difficulty_two: bool=True, hard_test=True):
        """Adds two AI players with specified difficulties for testing purposes. Defaults to testing both players in hard-mode."""
        self.players = (
            self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=difficulty_one, hard_test=hard_test),
            self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=difficulty_two, hard_test=hard_test),
        )

    def is_full(self, col: int):
        """Checks if a given column is full."""
        return self.height_list[col] == 0 # quick validation of column to play

    def is_valid(self, row, col):
        """Validates if a move is on the board aby checking if square is not occupied."""
        if 0 <= col < self.columns: # validate the move is on the board and free
            return not self.board.square_is_occupied(row, col)
        return False
    
    def make_move(self, col: int, marker: str):
        """
        Records a move on the board for a given column and marker.
        Returns True if the move was successful, otherwise returns False.
        """
        if not 0 <= col < self.columns:
            raise ValueError(f"Invalid column '{col}'. Must be between 0 and {self.columns - 1}.")
        
        for row in range(self.rows - 1, -1, -1):
            if self.is_valid(row, col):
                self._premove_board_state = self.board.get_board(True)
                self.board.add_to_square(row, col, marker)
                self.move_list.append((row, col))
                self.height_list[col] = row
                self.round_count += 1
                return True
        return False
    
    def check_winner(self):
        """Checks the board for a winning condition."""
        return self._win._check_for_winner()
    
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()

    def reset_game_state(self):
        """Resets the board, winner information, move history, and round count to start a new game."""
        self.reset_board()
        self.reset_board()
        self.reset_winner()
        self.move_list = []
        self.round_count = 0
        self.go_first = not self.go_first

    def reset_winner(self):
        """Resets all winner-related attributes to their default values."""
        self._win.reset_win_info()
        self.winner_name = None
        self.winner_marker = None
        self.win_type = None
        self.win_row = -1
        self.win_column = -1

    def get_winner_info(self):
        """Returns a dictionary with the winner's information."""
        return self._win.get_win_info()

    def get_player(self, index: int):
        """Returns the player at the specified index."""
        return self.players[index]

    
    def get_winner_attributes(self):
        """Returns a tuple of the winner's name, marker, win type, row, and column."""
        return self.winner_name, self.winner_marker, self.win_type, self.win_row, self.win_column
    

    def get_board_animation_states(self, player_marker):
        """
        Generates a list of board states for animating a move.
        Returns a list of board states, from the top of the column to the final position.
        """
        # lazy method called only when needed
        board_states = []
        # Get a mutable copy of the current board state that allows for board manipulation without change the actual state of the game board
        temp_board = self._premove_board_state
        current_row_played, current_column_played = self.move_list[-1]
        # Create a boad state with the current player's marker starting from the top row to the final row position of the current move
        for j in range(current_row_played + 1):
            temp_board.add_to_square(j, current_column_played, player_marker)
            board_states.append(temp_board.get_board())
            if j < current_row_played:
                temp_board.update_square(j, current_column_played, 0)
        self._last_pre_move_state = None

        return board_states

    def update_player_name(self, name: str, marker: str) -> None:
        """Updates a player's name based on their marker ('r' or 'y')."""
        marker = marker.lower()
        if marker not in {"r", "y"}:
            raise ValueError(f"Invalid marker '{marker}'. Must be 'r' or 'y'.")
        marker_to_index = {"r": 0, "y": 1}
        self.players[marker_to_index[marker.lower()]].name = name

    def update_players_stats(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player.name == self.winner_name:
                player.won()
            elif self.winner_name is not None:
                player.lost()

    def update_winner_info(self) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if there is no winner. """
        winner_info = self.get_winner_info()
        for player in self.players:
            if player.marker == winner_info["marker"]:
                self.winner_name = player.name
                self.winner_marker = player.marker
        self.win_type = winner_info["type"]
        self.win_row = winner_info["row"]
        self.win_column = winner_info["column"]

    def update_ai_player_level(self, difficulty: bool):
        """Updates the difficulty level for the AI player."""
        ai_player_found = False
        for player in self.players:
            if isinstance(player, self.AIPlayer): 
                player.difficulty = difficulty
                ai_player_found = True
    
        if not ai_player_found:
            raise RuntimeError("Cannot update AI player level. No AI player found")

    def print_winner(self):
        """Prints the winner's name, marker, and winning move details."""
        print(f"Winning Player: {self.winner_name}")
        print(f"Playing {self.winner_marker}")
        print(f"Won in {self.win_type} at row {self.win_row + 1} and column {self.win_column + 1}.")

    def print_stats(self):
        """Prints the game statistics for each player."""
        for player in self.players:
            print(player.__str__())

    class ConnectFourWinChecker(LineChecker):
        def __init__(self, board, win_value=4):
            super().__init__(board, win_value)

        def _check_full_rows(self, win_value: int) -> Optional[tuple]:
            for r, row in enumerate(self._board.get_rows()):
                for i in range(4):
                    row_slice = row[i:i + 4]
                    if winner := LineChecker.check_all_same(row_slice):
                        return winner, "row", r, i

        def _check_full_columns(self, win_value: int) -> Optional[tuple]:
            for c, column in enumerate(self._board.get_columns()):
                for i in range(3):
                    col_slice = column[i:i + 4]
                    if winner := LineChecker.check_all_same(col_slice):

                        return winner, "column", i, c

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


    class ConnectFourPlayer(Player):
        def __init__(self, name: str = "Me", marker: str = "r"):
            super().__init__(name, marker)  # Initialize the name first
            self.marker = marker  # Use the property setter for validation
            self.marker_name = self._get_marker_name()

        @Player.name.setter
        def name(self, value):
            """Ensure name is assigned for empty string."""
            if not value:
                value = f"Anonymous {self.marker.capitalize()}"
            self._name = value  # Directly set the private attribute

        @Player.marker.setter
        def marker(self, value):
            """Ensure marker is only 'r' or 'y'."""
            if value not in {"r", "y", "R", "Y"}:
                raise ValueError(f"Invalid marker: {value}. Must be 'r' or 'y'.")
            self._marker = value.lower()  # Directly set the private attribute
            self.marker_name = self._get_marker_name()  # Update marker_name when marker changes

        def _get_marker_name(self):
            """Determine the marker name based on the marker value."""
            return "Red" if self._marker == "r" else "Yellow"

        @property
        def is_human(self):
            """Ensure the is_human boolean tag is True."""
            return True


    class AIPlayer(Player):

        def __init__(self, name: str = "CPU", marker: str = "y", difficulty: bool = False, game: 'ConnectFour' = None):
            """AIPlayer is a child class of Player"""
            super().__init__(name, marker)
            self.game = game
            self.score = 0

        @property
        def is_human(self):
            """Ensure the is_human boolean tag is False."""
            return False

        def get_random_column(self):
                return randint(0, self.game.columns - 1)

        def random_int(self) -> tuple[int, int]:
            """Selects any open random positions on the board. Returns row and column index."""
            column = self.get_random_column()
            while self.game.board.square_is_occupied(0, column):
                column = self.get_random_column()

            return column

        def move(self):

            if (move:= self.win_or_block()) is not None:
                # print("Played WIN or BLOCK")
                # print(f"Computer's move {move}")
                # sleep(5)
                return move
            ### Debugging
            # print(self.game.height_list)
            # print("Played RANDOM")
            # sleep(5)
            return self.random_int()

        # def get_empty_move_positions(self):
        #     for column in range(self.game.board.columns):
        #         return [(self.game.height_list[column] - 1, column) for column in range(self.game.board.columns)]

        def win_or_block(self):
            block_position = -1
            horizontal_midpoint = self.game.board.columns // 2

            def marker_check(line):
                if marker := LineChecker.check_all_same(line):
                    if marker == 'y':
                            return True
                    elif marker == 'r':
                        return False
                return None

            def check_and_update(line, row, column):
                if not line:
                    return None
                nonlocal block_position
                win_or_block = marker_check(line)
                if win_or_block is True:
                    return column  # Winning move
                elif win_or_block is False:
                    block_position = column  # Possible block move
                return None

            def left_right_pattern(line, square):
                if not (line and square):
                    return None
                line.append(square)
                return line

            def star_pattern_check(row, row_height, column):
                diagonal_line = self.game.board.get_diagonal_segment
                down_left = self.game.board.get_square_value(row_height, column - 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row - 1, col=column + 1, length = 2, up=True, right=True),
                        down_left
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                down_right = self.game.board.get_square_value(row_height, column + 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row - 1, col=column - 1, length = 2, up=True, right=False),
                        down_right
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                up_right = self.game.board.get_square_value(row - 1, column + 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row_height, col=column - 1, length = 2, up=False, right=False),
                        up_right
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                up_left = self.game.board.get_square_value(row - 1, column - 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row_height, col=column + 1, length = 2, up=False, right=True),
                        up_left
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                return None

            def down_check(row_height, column):
                column_line = self.game.board.get_column_segment
                if (move := check_and_update(column_line(row=row_height, col=column, length = 3), row, column)) is not None:
                    # print(f"WON in DOWN COL at move {move}")
                    return move

                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row_height, col=column + 1, length = 3, up=False, right=True), row, column)) is not None:
                    # print(f"WON in DOWN Diag Right {move}")
                    return move
                if (move := check_and_update(diagonal_line(row=row_height, col=column - 1, length = 3, up=False, right=False), row, column)) is not None:
                    # print(f"WON in DOWN Diag Left {move}")
                    return move
                return None

            def right_and_up_check(row, column):
                row_line = self.game.board.get_row_segment
                if (move := check_and_update(row_line(row=row, col=column + 1, length=3), row, column)):
                    return move

                # One-two pattern
                one_two_pattern = left_right_pattern(
                    row_line(row=row, col=column + 1, length = 2),
                    left_value
                )
                if (move := check_and_update(one_two_pattern, row, column)):
                    return move

                # Two-one pattern
                two_one_pattern = left_right_pattern(
                    row_line(row=row, col=column - 2, length=2),
                    right_value
                )
                if (move := check_and_update(two_one_pattern, row, column)):
                    return move

                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row - 1, col=column + 1, length=3, up=True, right=True), row, column)):
                    return move

                return None

            def left_and_up_check(row, column):
                row_line = self.game.board.get_row_segment
                if (move := check_and_update(row_line(row=row, col=column - 1, length = 3, right=False), row, column)) is not None:
                    return move

                # One-two pattern here
                one_two_pattern = left_right_pattern(
                    row_line(row=row, col=column + 1, length = 2),
                    left_value
                )

                if (move := check_and_update(one_two_pattern, row, column)) is not None:
                    return move
                # Two-one pattern here
                two_one_pattern = left_right_pattern(
                    row_line(row=row, col=column - 2, length = 2),
                    right_value
                )
                if (move := check_and_update(two_one_pattern, row, column)) is not None:
                        return move

                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row - 1, col=column - 1, length = 3, up=True, right=False), row, column)) is not None:
                    return move

                return None

            for column, row_height in enumerate(self.game.height_list):
                # Check if column is full; height list at 0 means the top row is occupied and there are no moves in the column
                if row_height == 0:
                    continue

                # Update the row to the current open position in the column
                row = row_height - 1

                # Check for three in a row down, down-right and down left starting from vertical mid-point
                if row_height <= self.game.board.rows // 2:
                    if move := down_check(row_height, column):
                        # print(f"WON in DOWN {move}")
                        return move

                # Check all diagonal directions with one-two or two-one patterns
                if move:= star_pattern_check(row, row_height, column):
                    # print(f"Won in a Star at {move}")
                    return move

                left_value = self.game.board.get_square_value(row, column - 1)
                right_value = self.game.board.get_square_value(row, column + 1)

                # Check if both neighbors of current open position in the column are either out of bounds or empty to avoid unnecessary checks
                if (left_value == 0 or left_value is None) and (right_value == 0 or right_value is None):
                    continue

                if column <= horizontal_midpoint:
                    # Check row right combinations and up-right diagonal
                    if move := right_and_up_check(row, column):
                        # print(f"WON in ROW RIGHT at Col {move}")
                        return move

                if column >= horizontal_midpoint:
                    # Check row left combinations and up-left diagonal
                    if (move := left_and_up_check(row, column)) is not None:
                        # print(f"WON in ROW LEFT at Col {move}")
                        return move

            return block_position if block_position != -1 else None
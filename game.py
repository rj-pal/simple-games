from collections import Counter
from random import choice, randint
from typing import Tuple, List, Union, Optional
from Board import Board, WinChecker
from Player import Player

def int_converter(number, columns):
    return divmod(number, columns)

def pair_converter(pair, columns):
    return pair[0]*columns + pair[1]

def board(rows: int, columns: int):
    board = []
    for i in range(rows):
        if i == 1:
            board.append(["x" for _ in range(columns)])
        else:
            board.append([0 for _ in range(columns)])
    return board

class TicTacToe:

    def __init__(self):
         self.board: List[List] = self.create_board()
         self.move_list: List = []
         self.round_count: int = 0
         self.go_first: bool = True
         self.winner_name: str = None  # All winner attributes default to None when no winner or based on Winchecker
         self.winner_marker: str = None
         self.win_type: str = None
         self._win: WinChecker = WinChecker(self.board)
         self.players = self.create_human_players() # Default to two player mode

    def create_board(self):
        return Board(3,3)

    def create_human_players(self) -> Tuple[Player, Player]:
        return (
            self.TicTacToePlayer("Player 1", "x"),
            self.TicTacToePlayer("Player 2", "o"),
        )
    def create_ai_player(self, name: Optional[str], difficulty: Optional[bool]) -> Tuple[Player, Player]:
        self.players = (
            self.TicTacToePlayer("Player 1", "x"),
            self.AIPlayer(name=name, difficulty=difficulty, game=self),
        )

    def add_two_hard_move_ai_players_for_testing(self):
        self.players = (
            self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=True, hard_test=True),
            self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=True, hard_test=True),
        )

    def add_ai_players_for_testing(self, difficulty_one: bool, difficulty_two: bool):
        self.players = (
            self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=difficulty_one),
            self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=difficulty_two),
        )

    @property
    def board_size(self):
        return self.board.rows * self.board.columns

    def print_winner(self):
        print(f"Winning Player: {self.winner_name}")
        print(f"Playing {self.winner_marker}")
        if self.win_index == -1:
             print(f"Won in {self.win_type}")
        else:
            print(f"Won in {self.win_type} {self.win_index + 1}")
    
    def print_stats(self):
        for player in self.players:
            print(player.__str__())

    def is_valid(self, row, col):
        if 0 <= (row * col) < self.board_size: # validate the move is on the board
            return not self.board.square_is_occupied(row, col)
        return False

    def make_move(self, row, col, marker):
        if self.is_valid(row, col):
            self.board.add_to_square(row, col, marker)
            self.move_list.append((row, col))
            self.round_count += 1
            return True
        return False
    
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()

    def reset_game_state(self):
        self.reset_board()
        self.reset_winner()
        self.move_list = []
        self.round_count = 0
        self.go_first = not self.go_first

    def update_ai_player_level(self, difficulty: bool):
        for player in self.players:
            if isinstance(player, self.AIPlayer): 
                player.difficulty = difficulty

    def update_player_name(self, name: str, marker: str) -> None:
        """Updates a player's name based on their marker ('x' or 'o')."""
        marker = marker.lower()    
        if marker not in {"x", "o"}:
            raise ValueError(f"Invalid marker '{marker}'. Must be 'x' or 'o'.")
        marker_to_index = {"x": 0, "o": 1}
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
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        winner_info = self.get_winner_info()
        for player in self.players:
            if player.marker == winner_info["marker"]:
                self.winner_name = player.name
                self.winner_marker = player.marker
        self.win_type = winner_info["type"]
        # marker_to_index = {"row": row, "column": col}
        self.win_index = winner_info.get(self.win_type, -1)

    def check_winner(self):
        return self._win.check_for_winner()

    def get_winner_info(self):
        return self._win.get_win_info()
    
    def reset_winner(self):
        self._win.reset_win_info()
        self.winner_name = None
        self.winner_marker = None
        self.win_type = None
        self.win_index = None
        

    class TicTacToePlayer(Player):

        def __init__(self, name: str = None, marker: str = None):
            super().__init__(name, marker)  # Initialize the name first
            self.marker = marker  # Use the property setter for validation

        @Player.name.setter
        def name(self, value):
            """Ensure name is assigned for empty string."""
            if not value:
                value = f"Anonymous {self.marker.capitalize()}"
            self._name = value  # Directly set the private attribute

        @Player.marker.setter
        def marker(self, value):
            """Ensure marker is only 'x' or 'o'."""
            if value not in {"x", "o", "X", "O"}:
                raise ValueError(f"Invalid marker: {value}. Must be 'x' or 'o'.")
            self._marker = value.lower()  # Directly set the private attribute

    class AIPlayer(Player):

        def __init__(self, name: str = 'CPU', marker: str = "o", difficulty: bool = False, game: 'TicTacToe' = None):
            """AIPlayer is a child class of Player and contains all the functionality for a one-player game
            against the computer. The computer player has three modes: easy, intermediate and hard.
            The computer is defaulted to name 'Computer' and marker 'O'"""
            super().__init__(name, marker)
            self.game = game
            self._difficulty = None  # Backing private attribute
            self.difficulty = difficulty  # None is easy mode, False is intermediate mode, True is hard mode
            self.corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            self.insides = [(0, 1), (1, 0), (1, 2), (2, 1)]

        @property
        def difficulty(self) -> Optional[bool]:
            """Getter for the difficulty attribute."""
            return self._difficulty

        @difficulty.setter
        def difficulty(self, value: Optional[bool]) -> None:
            """Setter for the difficulty attribute, ensuring it's True, False, or None."""
            if value not in {True, False, None}:
                raise ValueError("Difficulty must be True, False, or None.")
            self._difficulty = value
        

        def get_fork_index(self, lines: list[Union[str, int]]) -> Optional[Union[int, bool]]:
            """Finds the position of a branch of a fork. Returns an integer of the row or column index
            if there is a column or row with a branch of a fork. Returns True if there is a diagonal fork 
            branch position. Returns None if no fork branch is found."""
            for index, line in enumerate(lines):
                fork = Counter(line)
                if fork["o"] == 1 and fork[0] == 2:
                    if len(lines) == 1:  # this is for the two diagonals which are just a 1x3 matrix
                        return True
                    else:
                        return index
            else:
                return

        def check_fork(self, board: Board) -> Optional[tuple[int, int]]:
            """Checks for forks on the board that allows the computer to make a move where it will have 
            a winning position in two or more lines. The function searches the board for any fork branches.
            If there is an intersection of two branches, the fork is added to a list, and randomly selects a fork.
            Returns the row and column position of the selected fork, or else return None if there are no forks."""
            fork_row_index = None
            fork_column_index = None
            fork_diagonal_right = None
            fork_diagonal_left = None
            # list of all potential forks on a board after a given move by a human player
            fork_positions = []

            rows = self.game.board.get_rows()
            columns = self.game.board.get_columns()

            # check rows, columns and two diagonals to get an index of any fork position for row/col,
            # or T/F for diagonal fork position
            fork_row_index = self.get_fork_index(rows)
            fork_column_index = self.get_fork_index(columns)
            fork_diagonal_right = self.get_fork_index(
                self.game.board.get_diagonals(3, "right"))  # get_fork_index only accepts a list of lines or 2D array
            fork_diagonal_left = self.get_fork_index(self.game.board.get_diagonals(3, "left"))

            # check for all forks: a fork is the intersection of a row and column or an intersection of a row or column
            # and a diagonal. For any fork in a row and column intersection or a row and diagonal intersection
            if fork_row_index is not None:
                if fork_column_index is not None:
                    if not self.game.board.square_is_occupied(fork_row_index, fork_column_index):
                        fork_positions.append([fork_row_index, fork_column_index])
                # row and right diagonal fork has the same column position as the row
                if fork_diagonal_right:
                    if not self.game.board.square_is_occupied(fork_row_index, fork_row_index):
                        fork_positions.append([fork_row_index, fork_row_index])
                        # row and left diagonal fork has the opposite column position as the row reflected through
                        # the centre horizontal line
                if fork_diagonal_left:
                    if not self.game.board.square_is_occupied(fork_row_index, 2 - fork_row_index):
                        fork_positions.append([fork_row_index, 2 - fork_row_index])

            # for any fork in a column and diagonal intersection    
            if fork_column_index is not None:
                # column and right diagonal fork has the same row position as the column
                if fork_diagonal_right:
                    if not self.game.board.square_is_occupied(fork_column_index, fork_column_index):
                        fork_positions.append([fork_column_index, fork_column_index])
                # column and left diagonal fork has the opposite row position as the column reflected through
                # the centre vertical line
                if fork_diagonal_left:
                    if not self.game.board.square_is_occupied(2 - fork_column_index, fork_column_index):
                        fork_positions.append([2 - fork_column_index, fork_column_index])

            # for a fork in the diagonal intersection: the centre is the intersection
            if fork_diagonal_right and fork_diagonal_left:
                fork_positions.append([1, 1])

            if fork_positions:  # selects a random fork position if there is more than one fork or just the one
                return fork_positions[randint(0, len(fork_positions) - 1)]
            else:
                return  # no forks were found

        def two_blanks(self, board) -> Optional[tuple[int, int]]:
            """Finds any line with two blanks and one 'O' marker. Used as alternative to random 
            integers and allows for possibility of victory. Returns row and column index else None."""
            rows = self.game.board.get_rows()
            columns = self.game.board.get_columns()
            diagonals = [self.game.board.get_diagonals(3, "right"),
                        self.game.board.get_diagonals(3, "left")]  # right diagonal is index 0, and left is index 1

            # returns the first found unoccupied square in a line with two blanks for intermediate mode
            # or possible win in hard mode
            for index, row in enumerate(rows):
                if row.count(0) == 2 and row.count("o") == 1:
                    for col in range(2):
                        if self.game.board.square_is_occupied(index, col):
                            continue
                        else:
                            return index, col
            for index, col in enumerate(columns):
                if col.count(0) == 2 and col.count("o") == 1:
                    for row in range(2):
                        if self.game.board.square_is_occupied(row, index):
                            continue
                        else:
                            return row, index
            for index, diag in enumerate(diagonals):
                if diag.count(0) == 2 and diag.count("o") == 1:
                    if index == 0:
                        for move_index in range(2):
                            if self.game.board.square_is_occupied(move_index, move_index):
                                continue
                            else:
                                return move_index, move_index
                    elif index == 1:
                        for move_index in range(2):
                            if self.game.board.square_is_occupied(move_index, 2 - move_index):
                                continue
                            else:
                                return move_index, 2 - move_index

        def random_ints(self, board: Board) -> tuple[int, int]:
            """Selects any open random positions on the board. Returns row and column index."""
            row = randint(0, 2)
            column = randint(0, 2)
            while self.game.board.square_is_occupied(row, column):
                row = randint(0, 2)
                column = randint(0, 2)

            return row, column

        def defence_mode(self, board: Board) -> tuple[int, int]:
            """AI strategy for when the computer plays second. Strategy is based on the first move
            by the human player. The AI always optimizes for a win or draw. Returns optimal move."""
            

            def assert_test(two_ints: tuple[int, int]):
                assert len(two_ints) == 2
                a, b = two_ints
                assert a is not None
                assert b is not None 


            r, c = self.game.move_list[0]
            if self.game.round_count == 1:

                if (r, c) == (1, 1):
                    move = choice(self.corners)
                    # print(*move)
                    assert move is not None
                    assert_test(move)
                    # move = choice(self.corners)
                else:
                    move = 1, 1
                
                return move

            elif self.game.round_count == 3:
                if (r, c) == (1, 1):
                    # Only triggered when the opposite corner to the move in previous round was played by player X
                    for corner in self.corners:
                        if not self.game.board.square_is_occupied(*corner):  # randomly select one of the two free corners
                            move = corner
                            assert move is not None
                            assert_test(move)
                            return move#corner
                elif (r, c) in self.corners:
                    if not self.game.board.square_is_occupied((r + 2) % 4, (c + 2) % 4):
                        move = (r + 2) % 4, (c + 2) % 4
                        assert_test(move)
                        assert move is not None
                        return move#(r + 2) % 4, (c + 2) % 4
                    else:
                        move = choice(self.insides)
                        assert_test(move)
                        assert move is not None
                        return move#choice(self.insides)
                elif (r, c) in self.insides:
                    r1, c1 = self.game.move_list[2]
                    if (r1, c1) in self.insides:
                        if r == 1:
                            move = choice([0, 2]), c
                            assert move is not None
                            assert_test(move)
                            return move#choice([0, 2]), c
                        else:
                            move = r, choice([0, 2])
                            assert move is not None
                            assert_test(move)
                            return move#r, choice([0, 2])
                    else:
                        if r == 1:
                            move = r1, c
                            assert move is not None
                            assert_test(move)
                            return r1, c
                        else:
                            move = r, c1
                            assert move is not None
                            assert_test(move)
                            return r, c1

            elif self.game.round_count == 5:
                if (r, c) == (1, 1):
                    r, c = self.game.move_list[4]
                    # find a two blank strategy and place in same row or column as the last x move
                    if self.game.board.get_rows()[r].count(0) == 1:
                        move = r, (c + 2) % 4
                        assert move is not None
                        assert_test(move)
                    elif self.game.board.get_columns()[c].count(0) == 1:
                        move = (r + 2) % 4, c
                        assert move is not None
                        assert_test(move)

                elif (r, c) in self.corners:
# Might need this two blank strategy to keep win alive
                    # if move := self.two_blanks(self.game.board):
                    #     return move

                    for corner in self.corners:
                        if not self.game.board.square_is_occupied(*corner):
                            move = corner
                            assert move is not None
                            assert_test(move)

                elif move := self.two_blanks(self.game.board):
                    assert move is not None
                    assert_test(move)
                    return move

                else:
                    # print("IM HERE!!!!")
                    # print(self.game.move_list)
                    # print(self.game.board)
                    move = self.random_ints(self.game.board)
                return move
            
            else:
                if move := self.two_blanks(self.game.board):
                    assert move is not None
                    assert_test(move)
                    return move
                else:
                    move = self.random_ints(self.game.board)

                    assert move is not None
                    assert_test(move)
                    return move#self.random_ints(self.game.board)

        def offence_mode(self, board: Board) -> tuple[int, int]:
            """AI strategy for when the computer plays first. Strategy is based on the first move by the
            computer and human player. The AI always optimizes for a win or draw. Returns optimal move."""
            # for testing purposes so hard mode can play versus hard mode used by TestGame class; otherwise, ignored
            # if self.game.round_count % 2 == 0:
            #     return self.defence_mode(self.game.board)

            if self.game.round_count == 0:
                # Only allow for corner or centre start to guarantee a win or draw
                starts = self.corners + [(1, 1)]
                return choice(starts)  # add element of randomness to first move

            elif self.game.round_count == 2:
                r, c = self.game.move_list[0]
                if (r, c) == (1, 1):
                    if self.game.move_list[1] not in self.corners:
                        move = choice(self.corners)
                    else:
                        r, c = self.game.move_list[1]
                        move = (r + 2) % 4, (c + 2) % 4

                elif (r, c) in self.corners:
                    if self.game.move_list[1] == (1, 1):
                        # print("HERE")

                        # move = (r + 2) % 4, c
                        move = (r + 2) % 4, (c + 2) % 4

                    elif self.game.move_list[1] in self.corners:
                        for corner in self.corners:
                            if self.game.board.square_is_occupied(*corner):
                                pass
                            else:
                                move = corner

                    elif self.game.move_list[1] in self.insides:
                        for i in range(3):
                            if self.game.board.get_rows()[r - i].count("x") == 1:
                                if self.game.board.square_is_occupied(1, c):
                                    pass
                                else:
                                    move = ((r + 2) % 4), c
                            elif self.game.board.get_columns()[c].count("x") == 1:
                                move = r, ((c + 2) % 4)
                return move

            elif self.game.round_count == 4:
                if move := self.check_fork(self.game.board):
                    return move

                elif self.game.move_list[1] in self.corners:
                    for move in self.corners:
                        if self.game.board.square_is_occupied(*move):
                            pass
                        else:
                            return move
                elif move := self.two_blanks(self.game.board):
                    return move

                else:
                    return self.random_ints(self.game.board)

            else:
                if move := self.two_blanks(self.game.board):
                    return move

                return self.random_ints(self.game.board)

        def win_or_block(self, board: Board) -> Optional[tuple[int, int]]:
            """Checks for a win or block. Selects the first found win position or a random block position if there are
            more than one block moves."""
            block_positions = []  # Makes a list of all possible blocking points on the board of the opponent

            lines = [self.game.board.get_rows(),
                    self.game.board.get_columns(),
                    self.game.board.get_diagonals(3, "right"),
                    self.game.board.get_diagonals(3, "left")
                    ]
            for indicator, line in enumerate(lines):

                for index_1, squares in enumerate(line):
                    marker, count = Counter(squares).most_common(1)[0]
                    if count == (len(squares) - 1) and marker !=  0:
                        for index_2, square in enumerate(squares):
                            if indicator == 0:
                                if not self.game.board.square_is_occupied(index_1, index_2):
                                    if marker !=  "o":
                                        block_positions.append([index_1, index_2])
                                    else:
                                        return index_1, index_2

                            elif indicator == 1:
                                if not self.game.board.square_is_occupied(index_2, index_1):
                                    if marker !=  "o":
                                        block_positions.append([index_2, index_1])
                                    else:
                                        return index_2, index_1

                            elif indicator == 2:
                                if not self.game.board.square_is_occupied(index_2, index_2):
                                    if marker !=  "o":
                                        block_positions.append([index_2, index_2])

                                    else:
                                        return index_2, index_2
                            else:
                                if not self.game.board.square_is_occupied(index_2, 2 - index_2):
                                    if marker !=  "o":
                                        block_positions.append([index_2, 2 - index_2])

                                    else:
                                        return index_2, 2 - index_2
            if block_positions:
                # Use randomly selected block position from max of three for variety sake
                return block_positions[randint(0, len(block_positions) - 1)]
            else:
                return None

        def move(self, board: Board) -> Union[tuple[int, int], list[int]]:
            """Selects a move for the AI player based on the play mode of easy, intermediate or hard. """
            if self.difficulty is None:  # easy mode
                result = self.random_ints(self.game.board)
                assert result is not None 
                return result
                # return self.random_ints(self.game.board)

            if move := self.win_or_block(self.game.board):  # intermediate or hard mode always checks for win or block first
                return move
                # result = move
                # assert result is not None 
                # return result
            

            if self.difficulty:  # hard mode
                if self.game.go_first:  # strategy is based on if human player plays first or not (go_first is for human player
                    
                    result = self.defence_mode(self.game.board)
                    # assert result is not None 
                    return result
                    # return self.defence_mode(self.game.board)
                else:

                    result = self.offence_mode(self.game.board)
                    assert result is not None 
                    return result
                    # return self.offence_mode(self.game.board)

            else:  # intermediate mode always checks for a fork first then for two blanks after two random moves
                if self.game.round_count > 3:
                    if move := self.check_fork(self.game.board):
                        return move
                    if move := self.two_blanks(self.game.board):
                        return move
                return self.random_ints(self.game.board)
    
    class AITestPlayer(AIPlayer):

        def __init__(self, name: str = 'Computer', marker: str = "o", difficulty: bool = False, game: 'TicTacToe' = None, hard_test: bool = False):
            """AIPlayer is a child class of Player and contains all the functionality for a one-player game
            against the computer. The computer player has three modes: easy, intermediate and hard.
            The computer is defaulted to name 'Computer' and marker 'O'"""
            super().__init__(name, marker, difficulty, game)
            self.hard_test = hard_test

        def move(self, board: Board) -> Union[tuple[int, int], list[int]]:
            """Selects a move for the AI player based on the play mode of easy, intermediate or hard. """
            if self.difficulty is None:  # easy mode
                result = self.random_ints(self.game.board)
                return result

            if result := self.win_or_block(self.game.board):  # intermediate or hard mode always checks for win or block first
                return result
               

            if self.difficulty:  # hard mode
                if self.game.go_first:  # strategy is based on if human player plays first or not (go_first is for human player)
                    if self.hard_test and (self.game.round_count % 2 == 0):
                        return self.offence_mode(self.game.board)
                    return self.defence_mode(self.game.board)
                else:
                    if self.hard_test and (self.game.round_count % 2 == 1):
                        return self.defence_mode(self.game.board)

                    return self.offence_mode(self.game.board)

            else:  # intermediate mode always checks for a fork first then for two blanks after two random moves
                if self.game.round_count > 3:
                    if move := self.check_fork(self.game.board):
                        return move
                    if move := self.two_blanks(self.game.board):
                        return move
                return self.random_ints(self.game.board)

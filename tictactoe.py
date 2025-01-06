import os
from itertools import chain
from enum import Enum
from typing import Union, Optional
from collections import Counter, namedtuple
from random import randint, choice
from time import sleep

# Constant string used in Game class
WELCOME = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *     *       *   * * *   *       * * *    *  *      *   *     * * *      *
   *      *  *  *    * *     *      *        *    *    *  *  *    * *        *
   *       *   *     * * *   * * *   * * *    *  *    *       *   * * *      *
   *                                                                         *
   *                                                                         *
   *      * * *   *  *                                                       *
   *        *    *    *                                                      *
   *        *     *  *                                                       *
   *                                                                         *
   *                                                                         *
   *      * * *   *    * *     * * *    *     * *     * * *   * *   * * *    *
   *        *     *   *          *     * *   *          *    *   *  * *      *
   *        *     *    * *       *    *   *   * *       *     * *   * * *    *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

INTRO = """
This is an online version of the classic game. Play multiple games per session
against and opponent or the computer. X starts the game.
"""

GAMEOVER = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *               * * *        **        *       *    * * * *               *
   *              *            *  *       * *   * *    *                     *
   *              *   * *     *    *      *   *   *    * * *                 * 
   *              *     *    *      *     *       *    *                     *
   *               * * *    *        *    *       *    * * * *               *
   *                                                                         *
   *                                                                         *
   *                *  *     *       *    * * * *     *  *  *                *
   *              *      *    *     *     *           *      *               *
   *              *      *     *   *      * * *       *  *  *                *
   *              *      *      * *       *           *      *               *
   *                *  *         *        * * * *     *       *              *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""


# Printing functions for creating computer output effect and border box

def delay_effect(strings: list[str], delay: float = 0.025, word_flush: bool = True) -> None:
    """Creates the effect of the words or characters printed one letter or line at a time. 
    Word_flush True delays each character. False delays each complete line in a list. """
    #     Used when testing so that can play the games quicker
    #     if delay != 0:
    #         delay = 0
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)


def surround_string(strings: list[str], symbol: str, offset: int = 0) -> list[str]:
    """Creates a border around any group of sentences. Used to create the scoreboard for the players."""
    string_list = list(chain.from_iterable(
        string.split("\n") if "\n" in string
        else [string]
        for string in strings
    ))

    border = symbol * (len(max(string_list, key=len)) + 2 * offset)
    output_list = [
        border,
        *[string.center(len(border)) for string in string_list],
        border
    ]

    return ["\n" + "\n".join([symbol + string + symbol for string in output_list]) + "\n"]


# Enum class of each Square as a list of strings for printing one line at a time on a board

class Square(Enum):
    """A Square is Blank, X or O. Each represents one square on the board. Each square is printed one line or
    list element at a time. Name of the square will be printed when called directly for printing."""
    BLANK = [
        "            ",
        "            ",
        "            ",
        "            ",
        "            "
    ]

    O = [
        "    *  *    ",
        "  *      *  ",
        " *        * ",
        "  *      *  ",
        "    *  *    "
    ]

    X = [
        "  *       * ",
        "    *   *   ",
        "      *     ",
        "    *   *   ",
        "  *       * "
    ]

    def __str__(self) -> str:
        """Returns a string of the name of the square enum object."""
        return self.name

    def __repr__(self) -> str:
        """Returns a string of the name and value of the square enum object."""
        return f'Name: {self.name}\nValue: {self.value}'


class Board:
    """
    Board class stores the information for every square on the board. It allows for updating, resetting,
    and printing of the board as a string using a list of a list of a list Square objects. It has a board attribute, 
    which is a 3D array of Square objects, and a horizontal attribute for the row lines. The data is store in Rows.
    Columns can be created from zipping the rows. The board is displayed line-by-line from top to bottom and uses 
    the join method. Each row is created line-by-line from zipping each Square in a row, top to bottom combined with
    an asterisk, which make up the vertical lines in the board. Each row is joined to a horizontal line.
    """

    def __init__(self):
        self.board = [
            [Square.BLANK] * 3,
            [Square.BLANK] * 3,
            [Square.BLANK] * 3
        ]

        self.horizontal_line = "* " * 18 + "*"

    def get_rows(self) -> list[list[Square]]:
        """Returns a list of the rows of Square objects. It is the 2D game Board object list of lists."""
        return self.board

    def get_columns(self) -> list[list[Square]]:
        """Returns a list of the columns of Square objects. It is a list of lists of each row position from
        the Board object using zipped row positions and mapped into a list for consistency with rows."""
        return list(map(list, zip(*self.board)))

    def get_right_diagonal(self) -> list[Square]:
        """Returns a list of the right diagonal of Square objects. It is a sliced list of the game Board object."""
        return list(self.board[i][i] for i in range(len(self.board)))

    def get_left_diagonal(self) -> list[Square]:
        """Returns a list of the left diagonal of Square objects. It is a sliced list of the game Board object."""
        return list(self.board[i][-(i + 1)] for i in range(len(self.board)))

    def square_is_occupied(self, row: int, column: int) -> bool:
        """Checks if a square is occupied by an Ex or Oh."""
        return self.board[row][column] != Square.BLANK

    def update_square(self, row: int, column: int, square: Square) -> None:
        """Updates the square on the board to an Ex or Oh from the Square class."""
        self.board[row][column] = square

    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        for r, row in enumerate(self.board):
            for c in range(len(row)):
                self.board[r][c] = Square.BLANK

    def _create_row(self, row: list[list[Square]]) -> str:
        """Returns a string of a single row of the board from current state of the board attribute."""
        return "\n".join(["*".join(line).center(os.get_terminal_size().columns - 1) for line in zip(*row)])

    def _create_board(self) -> str:
        """Returns a string of the complete board created row by row using _create_row method for printing."""
        return f"\n{self.horizontal_line.center(os.get_terminal_size().columns - 1)}\n".join(
            [self._create_row([square.value for square in row]) for row in self.board])

    def __str__(self) -> str:
        """Returns full string representation of the board for printing in the Game Class."""
        return self._create_board()

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the board for information purposes only."""
        return f'Board:\n{str(self.board)}\nHorizontal line:\n{self.horizontal_line}'


class Player:
    def __init__(self, name: str, marker: Square):
        """
        Player Class stores all the information on a player. It has marker attribute that must be a Square 
        Ex or Oh object. It also has a name attribute with default settings if no name is passed. It has 3 
        statistics for wins, losses and games played. The number of draws is included in the stats when
        printing a string of a player. It has an attribute to indicate if the player will use the Game Class AI. 
        """
        self.marker = marker
        self.name = name if name else f"Anonymous {self.marker}"
        self.win_count = 0
        self.lost_count = 0
        self.games_played = 0

    def game_played(self) -> None:
        """Updates the number of total games played by the player."""
        self.games_played += 1

    def won(self) -> None:
        """Updates the number of games won of the player."""
        self.win_count += 1

    def lost(self) -> None:
        """Updates the number of games lost of the player."""
        self.lost_count += 1

    def get_draw_count(self) -> int:
        """Returns the number of tied games of the player based on the other game statistics."""
        return self.games_played - (self.win_count + self.lost_count)

    def __str__(self) -> str:
        """Returns a string of key information on the player statistics used for printing in the Game Class."""
        player_string = f"\n{self.marker}: {self.name}\nWin: {self.win_count}, Loss: {self.lost_count}, " \
                        f"Draw: {self.get_draw_count()}\n"
        return player_string

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the player for information purposes only. Stored
        as a named tuple. """
        PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "played"])

        player_info = PlayerRepr(
            self.name,
            self.marker.name,
            self.win_count,
            self.lost_count,
            self.games_played
        )
        return str(player_info)


class AIPlayer(Player):

    def __init__(self, name: str = 'Computer', marker: Square = Square.O, difficulty: bool = False):
        """AIPlayer is a child class of Player and contains all the functionality for a one-player game
        against the computer. The computer player has three modes: easy, intermediate and hard.
        The computer is defaulted to name 'Computer' and marker 'O'"""
        super().__init__(name, marker)
        self.difficulty = difficulty  # None is easy mode, False is intermediate mode, True is hard mode
        self.corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.insides = [(0, 1), (1, 0), (1, 2), (2, 1)]

    def get_fork_index(self, lines: list[[Square]]) -> Optional[Union[int, bool]]:
        """Finds the position of a branch of a fork. Returns an integer of the row or column index
        if there is a column or row with a branch of a fork. Returns True if there is a diagonal fork 
        branch position. Returns None if no fork branch is found."""
        for index, line in enumerate(lines):
            fork = Counter(line)
            if fork[Square.O] == 1 and fork[Square.BLANK] == 2:
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

        rows = board.get_rows()
        columns = board.get_columns()

        # check rows, columns and two diagonals to get an index of any fork position for row/col,
        # or T/F for diagonal fork position
        fork_row_index = self.get_fork_index(rows)
        fork_column_index = self.get_fork_index(columns)
        fork_diagonal_right = self.get_fork_index(
            [board.get_right_diagonal()])  # get_fork_index only accepts a list of lines or 2D array
        fork_diagonal_left = self.get_fork_index([board.get_left_diagonal()])

        # check for all forks: a fork is the intersection of a row and column or an intersection of a row or column
        # and a diagonal. For any fork in a row and column intersection or a row and diagonal intersection
        if fork_row_index is not None:
            if fork_column_index is not None:
                if not board.square_is_occupied(fork_row_index, fork_column_index):
                    fork_positions.append([fork_row_index, fork_column_index])
            # row and right diagonal fork has the same column position as the row
            if fork_diagonal_right:
                if not board.square_is_occupied(fork_row_index, fork_row_index):
                    fork_positions.append([fork_row_index, fork_row_index])
                    # row and left diagonal fork has the opposite column position as the row reflected through
                    # the centre horizontal line
            if fork_diagonal_left:
                if not board.square_is_occupied(fork_row_index, 2 - fork_row_index):
                    fork_positions.append([fork_row_index, 2 - fork_row_index])

        # for any fork in a column and diagonal intersection    
        if fork_column_index is not None:
            # column and right diagonal fork has the same row position as the column
            if fork_diagonal_right:
                if not board.square_is_occupied(fork_column_index, fork_column_index):
                    fork_positions.append([fork_column_index, fork_column_index])
            # column and left diagonal fork has the opposite row position as the column reflected through
            # the centre vertical line
            if fork_diagonal_left:
                if not board.square_is_occupied(2 - fork_column_index, fork_column_index):
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
        rows = board.get_rows()
        columns = board.get_columns()
        diagonals = [board.get_right_diagonal(),
                     board.get_left_diagonal()]  # right diagonal is index 0, and left is index 1

        # returns the first found unoccupied square in a line with two blanks for intermediate mode
        # or possible win in hard mode
        for index, row in enumerate(rows):
            if row.count(Square.BLANK) == 2 and row.count(Square.O) == 1:
                for col in range(2):
                    if board.square_is_occupied(index, col):
                        continue
                    else:
                        return index, col
        for index, col in enumerate(columns):
            if col.count(Square.BLANK) == 2 and col.count(Square.O) == 1:
                for row in range(2):
                    if board.square_is_occupied(row, index):
                        continue
                    else:
                        return row, index
        for index, diag in enumerate(diagonals):
            if diag.count(Square.BLANK) == 2 and diag.count(Square.O) == 1:
                if index == 0:
                    for move_index in range(2):
                        if board.square_is_occupied(move_index, move_index):
                            continue
                        else:
                            return move_index, move_index
                elif index == 1:
                    for move_index in range(2):
                        if board.square_is_occupied(move_index, 2 - move_index):
                            continue
                        else:
                            return move_index, 2 - move_index

    def random_ints(self, board: Board) -> tuple[int, int]:
        """Selects any open random positions on the board. Returns row and column index."""
        row = randint(0, 2)
        column = randint(0, 2)
        while board.square_is_occupied(row, column):
            row = randint(0, 2)
            column = randint(0, 2)

        return row, column

    def defence_mode(self, board: Board) -> tuple[int, int]:
        """AI strategy for when the computer plays second. Strategy is based on the first move
        by the human player. The AI always optimizes for a win or draw. Returns optimal move."""

        r, c = Game.move_list[0]
        if Game.round_count == 2:

            if (r, c) == (1, 1):
                move = choice(self.corners)
            else:
                move = 1, 1
            return move

        elif Game.round_count == 4:
            if (r, c) == (1, 1):
                # Only triggered when the opposite corner to the move in previous round was played by player X
                for corner in self.corners:
                    if not board.square_is_occupied(*corner):  # randomly select one of the two free corners
                        return corner
            elif (r, c) in self.corners:
                if not board.square_is_occupied((r + 2) % 4, (c + 2) % 4):
                    return (r + 2) % 4, (c + 2) % 4
                else:
                    return choice(self.insides)
            elif (r, c) in self.insides:
                r1, c1 = Game.move_list[2]
                if (r1, c1) in self.insides:
                    if r == 1:
                        return choice([0, 2]), c
                    else:
                        return r, choice([0, 2])
                else:
                    if r == 1:
                        return r1, c
                    else:
                        return r, c1

        elif Game.round_count == 6:
            if (r, c) == (1, 1):
                r, c = Game.move_list[4]
                if board.get_rows()[r].count(Square.BLANK) == 1:
                    move = r, (c + 2) % 4
                elif board.get_columns()[c].count(Square.BLANK) == 1:
                    move = (r + 2) % 4, c

            elif (r, c) in self.corners:

                if move := self.two_blanks(board):
                    return move

                for corner in self.corners:
                    if not board.square_is_occupied(*corner):
                        move = corner

            elif move := self.two_blanks(board):
                return move

            return move

        else:
            if move := self.two_blanks(board):
                return move
            else:
                return self.random_ints(board)

    def offence_mode(self, board: Board) -> tuple[int, int]:
        """AI strategy for when the computer plays first. Strategy is based on the first move by the
        computer and human player. The AI always optimizes for a win or draw. Returns optimal move."""
        # for testing purposes so hard mode can play versus hard mode used by TestGame class; otherwise, ignored
        if Game.round_count % 2 == 0:
            return self.defence_mode(board)

        if Game.round_count == 1:
            # Only allow for corner or centre start to guarantee a win or draw
            starts = self.corners + [(1, 1)]
            return choice(starts)  # add element of randomness to first move

        elif Game.round_count == 3:
            r, c = Game.move_list[0]
            if (r, c) == (1, 1):
                if Game.move_list[1] not in self.corners:
                    move = choice(self.corners)
                else:
                    r, c = Game.move_list[1]
                    move = (r + 2) % 4, (c + 2) % 4

            elif (r, c) in self.corners:
                if Game.move_list[1] == (1, 1):

                    move = (r + 2) % 4, c

                elif Game.move_list[1] in self.corners:
                    for corner in self.corners:
                        if board.square_is_occupied(*corner):
                            pass
                        else:
                            move = corner

                elif Game.move_list[1] in self.insides:
                    for i in range(3):
                        if board.get_rows()[r - i].count(Square.X) == 1:
                            if board.square_is_occupied(1, c):
                                pass
                            else:
                                move = ((r + 2) % 4), c
                        elif board.get_columns()[c].count(Square.X) == 1:
                            move = r, ((c + 2) % 4)
            return move

        elif Game.round_count == 5:
            if move := self.check_fork(board):
                return move

            elif Game.move_list[1] in self.corners:
                for move in self.corners:
                    if board.square_is_occupied(*move):
                        pass
                    else:
                        return move
            elif move := self.two_blanks(board):
                return move

            else:
                return self.random_ints(board)

        else:
            if move := self.two_blanks(board):
                return move

            return self.random_ints(board)

    def win_or_block(self, board: Board) -> Optional[tuple[int, int]]:
        """Checks for a win or block. Selects the first found win position or a random block position if there are
        more than one block moves."""
        block_positions = []  # Makes a list of all possible blocking points on the board of the opponent

        lines = [board.get_rows(),
                 board.get_columns(),
                 list([board.get_right_diagonal()]),
                 list([board.get_left_diagonal()])
                 ]
        for indicator, line in enumerate(lines):

            for index_1, squares in enumerate(line):
                marker, count = Counter(squares).most_common(1)[0]
                if count == (len(squares) - 1) and marker is not Square.BLANK:
                    for index_2, square in enumerate(squares):
                        if indicator == 0:
                            if not board.square_is_occupied(index_1, index_2):
                                if marker is not Square.O:
                                    block_positions.append([index_1, index_2])
                                else:
                                    return index_1, index_2

                        elif indicator == 1:
                            if not board.square_is_occupied(index_2, index_1):
                                if marker is not Square.O:
                                    block_positions.append([index_2, index_1])
                                else:
                                    return index_2, index_1

                        elif indicator == 2:
                            if not board.square_is_occupied(index_2, index_2):
                                if marker is not Square.O:
                                    block_positions.append([index_2, index_2])

                                else:
                                    return index_2, index_2
                        else:
                            if not board.square_is_occupied(index_2, 2 - index_2):
                                if marker is not Square.O:
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
            return self.random_ints(board)

        if move := self.win_or_block(board):  # intermediate or hard mode always checks for win or block first
            return move

        if self.difficulty:  # hard mode
            if Game.go_first:  # strategy is based on if human player plays first or not (go_first is for human player)
                return self.defence_mode(board)
            else:
                return self.offence_mode(board)

        else:  # intermediate mode always checks for a fork first then for two blanks after two random moves
            if Game.round_count > 3:
                if move := self.check_fork(board):
                    return move
                if move := self.two_blanks(board):
                    return move
            return self.random_ints(board)


class Game:
    """
    The Game class contains all methods for managing and controling a series of Tic-Tac-Toe games. The two attributes,
    players and game board, require a list of Player Class objects and a Board Class object. These interact to create 
    the game on all levels: updating squares, checking for winners, displaying the board to the screen, tracking the
    moves, and creating strings for keeping tracking of winner information. The winner attributes use the player object
    to store key information on the current winner and display the winning information to the users. There is a mode 
    attribute which is used when the computer is a player that is necessary for the operating of the AI algorithm. The 
    class contains many methods for displaying information to the users, as well as getting input from the users with
    validation. The player stats are used in order to create a game session where multiple games can be played in 
    succession. 
    """
    move_list = []
    round_count = 0
    go_first = True  # When True, player 1 goes first and when False, player 2 goes first.

    def __init__(self):
        self.game_board = Board()  # Direct instance of a Board Class object to keep track of game information.
        self.players: [Player] = []

        self.winner = None  # The winner attributes with default settings reset when no winner
        self.win_index = 0  # these are updated when there is a winner.
        self.win_type = 'None'

    def print_welcome_box(self) -> None:
        """Prints the "Welcome to Tic Tac Toe" box."""
        print(WELCOME)

    def print_intro(self) -> None:
        """Prints a quick message to the user about the game session."""
        delay_effect([INTRO])

    def print_game_over(self) -> None:
        """Prints a flashing "Game Over" when a winner has been declared"""
        print()
        os.system('clear||cls')
        for _ in range(5):
            print(GAMEOVER.center(os.get_terminal_size().columns - 1), end='\r')
            sleep(0.75)
            os.system('clear||cls')
            sleep(0.5)
        print()
        self.print_board()

    def print_board(self) -> None:
        """Prints the current state of the game board. Printed line by line."""
        delay_effect([self.game_board.__str__()], 0.00075, False)

    def print_scoreboard(self) -> None:
        """Shows the player statistics for the game. Printed line by line."""
        delay_effect(surround_string([player.__str__() for player in self.players], "#", 25), 0.00075, False)

    def print_move(self, player: Player, row: int, column: int) -> None:
        """Returns a string for printing the last played square on the board by the current player."""
        delay_effect([f"\n{player.name} played the square in row {row + 1} and column {column + 1}.\n"])

    def print_first_player(self) -> None:
        """Prints who is plays first and their marker."""
        delay_effect([f'\n{self.players[-int(Game.go_first) + 1].name} plays first.'])
        input('\nPress Enter to start the game.')

    def add_player(self, player: Player) -> None:
        """Adds a player to the player list. Maximum of two players for each game session."""
        if len(self.players) < 2:
            self.players.append(player)

    def update_players(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player == self.winner:
                player.won()
            elif self.winner is not None:
                player.lost()

    def update_board(self, row: int, column: int, marker: Square) -> None:
        """Updates the board with the last played square."""
        self.game_board.update_square(row, column, marker)

    def _check_win(self, squares: list[Square]) -> Optional[Square]:
        """Checks if a line has all the same markers to see if the game has been won."""
        marker, count = Counter(squares).most_common(1)[0]
        if count == len(squares) and marker is not Square.BLANK:
            return marker

    def _check_rows(self) -> Optional[bool]:
        """Checks for winner in rows. Uses returned Square object to update the winner attributes. False if no Square
        object is assigned. """
        for r, row in enumerate(self.game_board.get_rows()):
            if winner := self._check_win(row):
                self._update_winner_info(winner, "row", r)
                return True

    def _check_columns(self) -> Optional[bool]:
        """Checks for winner in columns. Uses returned Square object to update winner attributes. False if no Square
        object is assigned. """
        for c, column in enumerate(self.game_board.get_columns()):
            if winner := self._check_win(column):
                self._update_winner_info(winner, "col", c)
                return True

    def _check_diagonals(self) -> Optional[bool]:
        """Checks for winner in diagonals. Uses returned Square object to update winner attributes. False if no
        Square object is assigned. """
        if winner := self._check_win(self.game_board.get_right_diagonal()):
            self._update_winner_info(winner, "right_diag")
            return True
        if winner := self._check_win(self.game_board.get_left_diagonal()):
            self._update_winner_info(winner, "left_diag")
            return True

    def _get_winner_with_marker(self, win_square: Square) -> Player:
        """Returns the winning player from the player list attribute using the player marker attribute."""
        for player in self.players:
            if player.marker == win_square:
                return player

    def _update_winner_info(self, win_marker: Square = 'None', win_type: str = 'None', win_index: int = 0) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        self.winner = self._get_winner_with_marker(win_marker)
        self.win_index = win_index + 1
        self.win_type = win_type

    def get_winner_info(self) -> None:
        """Displays the information of the winner of the game using the winner attributes."""
        winner_string = f"\nWinner winner chicken dinner. {self.winner.name} is the winner.\n{self.winner.marker} " \
                        f"wins in"
        win_type_dict = {
            "row": f"row {self.win_index}.",
            "col": f"column {self.win_index}.",
            "right_diag": "the right diagonal.",
            "left_diag": "the left diagonal."
        }
        winner_string = f"{winner_string} {win_type_dict[self.win_type]}\n"
        delay_effect(surround_string([winner_string], "#", 9), 0.00075,
                     False)  # customize the size of the box and speed of delay

    def check_for_winner(self) -> Optional[bool]:
        """Checks if the game has been won in a row, column or diagonal if a winning line is found. It will return
        the first found winning line starting by row, column, and then right and left diagonals."""
        check_winner_funcs = (
            self._check_rows,
            self._check_columns,
            self._check_diagonals
        )
        for f in check_winner_funcs:
            if winner_found := f():
                return winner_found

    def get_move(self, player: Player) -> Union[tuple[int, int], list[int]]:
        """Returns the currently played move of a row and then a column based on AI functionality 
        or from validated input from a player."""
        if isinstance(player, AIPlayer):
            board = self.game_board
            print("\nComputer is now thinking.")
            sleep(1.5)
            row, column = player.move(board)
        else:
            name = player.name
            row, column = self._prompt_move(name)  # Validated in the prompt_move function.
        return row, column

    def take_turn(self, player: Player) -> None:
        """Gets the row and column from the current player and updates the board tracker and game board for printing.
        Returns the indexed row and column."""
        row, column = self.get_move(player)
        # In Testing Mode do not clear the screen to see the moves of the AIplayer
        os.system('clear||cls')
        Game.move_list.append((row, column))
        self.update_board(row, column, player.marker)
        self.print_move(player, row, column)
        self.print_board()

    def _prompt_move(self, name: str) -> Union[tuple[int, int], list[int]]:
        """Validates and formats the user inputted row and column. Checks if the inputted position is occupied."""

        delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])

        row = self._prompt_int('row')
        column = self._prompt_int('column')

        while self.game_board.square_is_occupied(row, column):
            print("\nThe square is already occupied. Select another square.\n")
            row = self._prompt_int('row')
            column = self._prompt_int('column')

        return row, column

    def _prompt_int(self, value: str) -> int:
        """Returns two integers for a row and column move from the player input. Only allows 
        for 1, 2, or 3 with each integer corresponding to a row and then a column."""
        valid_input = {1, 2, 3}
        while True:
            try:
                input_value = int(input(f"Enter the {value}: "))
                if input_value in valid_input:
                    return input_value - 1  # Needed for 0 based index

                print(f"\nYou must enter 1, 2, or 3 only for the {value}.\n")

            except ValueError:
                print("\nYou must enter a number. Try again.\n")

    def _one_player(self) -> bool:
        """Sets the game to one or two players."""
        valid_input = {'1', '2', 'one', 'two'}
        while True:
            one_player = input("How many players? One or two: ").lower()
            if one_player in valid_input:
                return one_player in ['1', 'one']
            else:
                print('\nOnly one or two players are allowed.\n')

    def _select_difficulty_level(self) -> Optional[bool]:
        """Updates the difficulty level boolean when playing against the computer."""
        valid_input = ['1', 'easy', '2', 'intermediate', '3', 'hard']
        while True:
            level_of_difficulty = input("\nSelect the level of difficult, Easy, Intermediate or Hard: ").lower()
            if level_of_difficulty in valid_input[:2]:
                delay_effect(["\nYou are playing against the computer in easy mode."])
                return None
            elif level_of_difficulty in valid_input[2:4]:
                delay_effect(["\nYou are playing against the computer in intermediate mode."])
                return False
            elif level_of_difficulty in valid_input[4:]:
                delay_effect(["\nYou are playing against the computer in hard mode."])
                return True
            else:
                print(
                    f"\nThere is only easy, intermediate or hard mode.\nPlease select '1' for easy, '2' for "
                    f"intermediate or '3' for hard.")

    def create_players(self) -> None:
        """Creates two players of the Player class for game play and add the players to the player attribute."""
        # Checks for one or two players first. Player one is Ex by default. 
        # Player two is Oh by default. Computer is also Oh by default in one player games.
        one_player = self._one_player()

        name = input("\nPlayer one please enter the name of the player for X: ")
        self.add_player(Player(name, Square.X))

        if one_player:
            difficulty = self._select_difficulty_level()
            self.add_player(AIPlayer(difficulty=difficulty))
        else:
            name = input("\nPlayer two please enter the name of the player for O: ")
            self.add_player(Player(name, Square.O))

    def start_game(self) -> None:
        """Starts the game and creates two players from user input."""
        self.print_welcome_box()
        self.print_intro()
        self.create_players()
        self.print_first_player()
        self.print_board()
        self.play_game()

    def next_game(self) -> None:
        """Resets the board to blank squares, changes the the order of players, resets round count and
        move list, and starts a new game."""
        Game.round_count = 0
        Game.move_list.clear()
        Game.go_first = not Game.go_first
        self.game_board.reset_board()

        self.print_scoreboard()
        self.print_first_player()
        self.print_board()
        self.play_game()

    def play_game(self) -> None:
        """Main method for playing the game that terminates after all nine squares have been filled or a winner
        has been declared. Updates attributes of the Game and Player class with game information."""
        for i in range(9):
            Game.round_count += 1
            if Game.go_first:
                self.take_turn(self.players[i % 2])
            else:
                self.take_turn(self.players[i % 2 - 1])

            # Will start checking for winner after the fourth turn
            if i < 4:
                continue
            elif self.check_for_winner():
                sleep(0.25)
                self.print_game_over()
                self.update_players()
                self.get_winner_info()
                break
        else:
            draw_string = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"
            delay_effect(surround_string([draw_string], "#", 9), 0.00075, False)
            self._update_winner_info()
            self.update_players()


class TestGames(Game):

    def __init__(self):

        super().__init__()
        self.level = None
        self.games = None

    def start_test(self, level: str, games: int) -> None:
        """Tests the AIPlayer class by having one ai player against another ai player. Set the level of
        the first AI player to play against the computer in hard mode. Set the number of games to be tested.
        Only accepts parameters 'easy', 'intermediate' or 'hard'."""
        if games < 1:
            print("At least 1 test game needs to be run in order for the test to be complete.")
            return
        elif not isinstance(games, int):
            print("The number of games must be an integer and not a float or string.")
            return

        self.games = games

        if level == 'easy':
            difficulty = None
            self.level = 'easy'
        elif level == 'intermediate':
            difficulty = False
            self.level = 'easy'
        elif level == 'hard':
            difficulty = True
            self.level = 'hard'
        else:
            print("Only 'easy', 'intermediate', or 'hard is allowed for testing.")
            return

        if len(self.players) != 0:  # clear the player list in case of retesting at different level or multiply tests
            self.players.clear()

        #         AIPlayer.is_test = True
        self.add_player(AIPlayer(name=f'Computer {level.capitalize()}', marker=Square.X, difficulty=difficulty))
        self.add_player(AIPlayer(name='Computer Hard Mode', marker=Square.O, difficulty=True))

        # Since hard versus hard mode play the same strategy, there is no differentiation between X or O 
        # playing first. The AI hard strategy code is based on the AI player playing O, and thus
        # alternating who goes first will affect the code and cause an error or improper strategy moves.
        if self.level == 'hard':
            Game.go_first = not Game.go_first

        # Testing games
        for i in range(games):
            self.play_game()

            # Used for debugging, but now all errors seem to be fixed.
            if self.winner is not None and self.winner.marker == Square.X:
                print("EASY or INTERMEDIATE WON. You have a hole in your AI HARD mode strategy!")
                print(self.move_list)
                print(self.print_first_player())
                self.print_board()

            Game.round_count = 0
            Game.move_list.clear()
            # alternative who plays first to test both offensive and defensive strategy
            if self.level != 'hard':
                Game.go_first = not Game.go_first
            self.game_board.reset_board()

        # show the final statistics
        self.print_scoreboard()

    def play_game(self) -> None:
        """Same as play_game in the parent class without sending output to the terminal."""
        for i in range(9):
            Game.round_count += 1

            if Game.go_first:
                self.take_turn(self.players[i % 2])
            else:
                self.take_turn(self.players[i % 2 - 1])

            if i < 4:
                continue
            elif self.check_for_winner():
                self.update_players()
                break
        else:
            self._update_winner_info()
            self.update_players()

    def get_move(self, player: AIPlayer) -> Union[tuple[int, int], list[int]]:
        """Same as get_move in the parent class without the added effect of the computer 
        pausing to think and outputting a message to the terminal and calling the method
        for user input from the human player."""
        board = self.game_board

        row, column = player.move(board)

        return row, column

    def take_turn(self, player: AIPlayer) -> None:
        """Gets the row and column from the current player and updates the board tracker and game board for printing.
        Returns the indexed row and column."""
        row, column = self.get_move(player)
        Game.move_list.append((row, column))
        self.update_board(row, column, player.marker)


# Two static methods for setting up the game and command line window

def set_console_window_size(width: float, height: float) -> None:
    """Sets the console window to fit the board to the screen better."""
    # Check the platform (Windows or Unix-based)
    os.system('cls||clear')
    if os.name == 'nt':
        # Windows platform
        os.system(f'mode con: cols={width} lines={height}')
    else:
        # Unix-based platforms (Linux, macOS)
        os.system(f'printf "\033[8;{height};{width}t"')


def run_games() -> None:
    """
    The Main method for running a series of Tic-Tac-Toe games. Starts a game session that keeps track 
    of the two players statistics and allows for multiple plays. Creates a Game Object that manages the
    game from start to finish, including player creation and AI play.
    """
    games = Game()
    games.start_game()
    message = "\nYou must enter 'Yes' or 'No' only."
    while True:
        try:
            play_again = input("\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                games.next_game()
            elif play_again in ['no', 'n']:
                games.print_scoreboard()
                delay_effect(
                    ["\nGame session complete.\n\nThanks for playing Tic-Tac-Toe. See you in the next session.\n"])
                break
            else:
                print(message)

        except ValueError:
            print(message)


if __name__ == '__main__':
    set_console_window_size(85, 30)
    run_games()

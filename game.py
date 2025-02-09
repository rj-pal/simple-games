from collections import namedtuple, Counter
from typing import Tuple, List
from Player import Player
from Board import Board

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
         self.move_list: List = []
         self.round_count: int = 0
         self.go_first: bool = True
         self.board: List[List] = self.create_board()
         self.winner: TicTacToe.Player = None  # The winner attributes with default settings reset when no winner
         self.win_index: int = 0  # these are updated when there is a winner.
         self.win_type: str = 'None' 

         self.players = self.create_players()

    def create_board(self):
        return Board(3,3)

    def create_players(self) -> Tuple[Player, Player]:
        return (
            self.TicTacToePlayer("Player 1", "x"),
            self.TicTacToePlayer("Player 2", "o"),
        )

    def print_winner(self):
        print(f"Winning Player: {self.winner.name}")
        print(f"Playing {self.winner.marker}")
        print(f"Won in {self.win_type} {self.win_index}")

    # def get_rows(self) -> list[list]:
    #     """Returns a list of the rows of Square objects. It is the 2D game Board object list of lists."""
    #     return self.board

    # def get_columns(self) -> list[list]:
    #     """Returns a list of the columns of Square objects. It is a list of lists of each row position from
    #     the Board object using zipped row positions and mapped into a list for consistency with rows."""
    #     return list(map(list, zip(*self.board)))   
    
    # def get_left_diagonal(self) -> list:
    #     """Returns a list of the left diagonal of Square objects. It is a sliced list of the game Board object."""
    #     return list(self.board[i][-(i + 1)] for i in range(len(self.board)))
    
    # def get_right_diagonal(self) -> list:
    #     """Returns a list of the right diagonal of Square objects. It is a sliced list of the game Board object."""
    #     return list(self.board[i][i] for i in range(len(self.board)))

    # def square_is_occupied(self, row: int, column: int) -> bool:
    #     """Checks if a square is occupied by an Ex or Oh."""
    #     return self.board[row][column] != 0

    # def update_square(self, row: int, column: int, square: str) -> None:
    #     """Updates the square on the board to an Ex or Oh from the Square class."""
    #     self.board[row][column] = square

    # def update_board(self, row: int, column: int, marker: str) -> None:
    #     """Updates the board with the last played square."""
    #     self.board.update_square(row, column, marker)

    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()
        # for r, row in enumerate(self.board):
        #     for c in range(len(row)):
        #         self.board[r][c] = 0

    def update_player(self, name: str, marker: str) -> None:
        """Updates a player's name based on their marker ('x' or 'o')."""
        marker = marker.lower()    
        if marker not in {"x", "o"}:
            raise ValueError(f"Invalid marker '{marker}'. Must be 'x' or 'o'.")
        marker_to_index = {"x": 0, "o": 1}
        self.players[marker_to_index[marker.lower()]].name = name

    def update_players(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player == self.winner:
                player.won()
            elif self.winner is not None:
                player.lost()
    
    def _update_winner_info(self, win_marker: str = 'None', win_type: str = 'None', win_index: int = 0) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        for player in self.players:
            if player.marker == win_marker:
                self.winner = player
        self.win_index = win_index + 1
        self.win_type = win_type

    def check_for_winner(self): #-> Optional[bool]:
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

    def _check_win(self, squares: list): #-> Optional:
        """Checks if a line has all the same markers to see if the game has been won."""
        marker, count = Counter(squares).most_common(1)[0]
        if marker != 0 and count == 3:
            return marker

    def _check_rows(self): #-> Optional[bool]:
        """Checks for winner in rows. Uses returned Square object to update the winner attributes. False if no Square
        object is assigned. """
        for r, row in enumerate(self.board.get_rows()):
            if winner := self._check_win(row):
                self._update_winner_info(winner, "row", r)
                return True

    def _check_columns(self): #-> Optional[bool]:
        """Checks for winner in columns. Uses returned Square object to update winner attributes. False if no Square
        object is assigned. """
        for c, column in enumerate(self.board.get_columns()):
            if winner := self._check_win(column):
                self._update_winner_info(winner, "col", c)
                return True

    def _check_diagonals(self): #-> Optional[bool]:
        """Checks for winner in diagonals. Uses returned Square object to update winner attributes. False if no
        Square object is assigned. """
        if winner := self._check_win(self.board.get_right_diagonal()):
            self._update_winner_info(winner, "right_diag")
            return True
        if winner := self._check_win(self.board.get_left_diagonal()):
            self._update_winner_info(winner, "left_diag")
            return True

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


# print(board(3,3))
# exit()
# pair_list = []     
# for i in range(9):
#     pair_list.append(int_converter(i,3))
# print(pair_list)
# for pair in pair_list:
#     print(pair_converter(pair, 3))
# exit()

T = TicTacToe()
T.update_player("Joe", "x")
T.update_player("Mason", "O")
# T.update_player("", "x")
print(T.players)
print(T.check_for_winner())
T.print_winner()
print(T.board)

# print(T.board)
# print(T.get_columns())
# print(T.get_rows())
T.reset_board()
print(T.board)
# T.update_square(2, 2, 'X')

# T.update_players()
# print(T.players)
from typing import Tuple, List
from Player import Player
from Board import Board, WinChecker, winner_info
# import TicTacToeCLI as ttt

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
         self.winner: TicTacToe.Player = None  # The winner attributes with default settings reset when no winner
         self.win_marker: str = 'None'
         self.win_type: str = 'None'
         self.win: WinChecker = WinChecker(self.board)

         self.players = self.create_players()

    def create_board(self):
        return Board(3,3)

    def create_players(self) -> Tuple[Player, Player]:
        return (
            self.TicTacToePlayer("Player 1", "x"),
            self.TicTacToePlayer("Player 2", "o"),
        )
    @property
    def board_size(self):
        return self.board.rows * self.board.columns

    def print_winner(self):
        print(f"Winning Player: {self.winner.name}")
        print(f"Playing {self.winner.marker}")
        if self.win_index == -1:
             print(f"Won in {self.win_type}")
        else:
            print(f"Won in {self.win_type} {self.win_index + 1}")
    
    def print_stats(self):
        for player in self.players:
            print(player.__str__())

    def is_valid(self, row, col):
        return self.board.square_is_occupied(row, col)

    def make_move(self, row, col, marker):
        if not self.board.square_is_occupied(row, col):
            self.board.add_to_square(row, col, marker)
            self.move_list.append((row, col))
            self.round_count += 1
            return True
        return False
    
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()
    

    def update_player_info(self, name: str, marker: str) -> None:
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
            if player == self.winner:
                player.won()
            elif self.winner is not None:
                player.lost()
    
    def update_winner_info(self) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        win_marker, win_type, row, col = self.win.get_win_info()
        for player in self.players:
            if player.marker == win_marker:
                self.winner = player
        self.win_type = win_type
        marker_to_index = {"row": row, "column": col}
        self.win_index = marker_to_index.get(win_type, -1)

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


  # print(T.board)
    # print(T.players)
    

    # new_board = board_translator(T.board.board)
    # test = TicTacToeCLI(create_board(new_board))
    # test.print_board()


    # exit()
  

# print(board(3,3))
# exit()
# pair_list = []     
# for i in range(9):
#     pair_list.append(int_converter(i,3))
# print(pair_list)
# for pair in pair_list:
#     print(pair_converter(pair, 3))
# exit()

# T = TicTacToe()
# T.update_player("Joe", "x")
# T.update_player("Mason", "O")
# T.update_player("", "x")
# print(T.players)
# print(T.check_for_winner())
# T.print_winner()

# print(T.board)
# print(T.get_columns())
# print(T.get_rows())
# T.reset_board()
# print(T.board)
# T.update_square(2, 2, 'X')

# T.update_players()
# print(T.players)
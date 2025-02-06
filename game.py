from collections import namedtuple

def int_converter(number):
    return divmod(number, 3)

def pair_converter(pair):
    return pair[0]*3 + pair[1]

class TicTacToe:

    def __init__(self):
         self.move_list = []
         self.round_count = 0
         self.go_first = True
         self.board = [
            [0] * 3,
            [1] * 3,
            [0] * 3
        ]
         self.players: [Player] = []
         self.winner = True  # The winner attributes with default settings reset when no winner
         self.win_index = 0  # these are updated when there is a winner.
         self.win_type = 'None' 

    def get_rows(self) -> list[list]:
        """Returns a list of the rows of Square objects. It is the 2D game Board object list of lists."""
        return self.board

    def get_columns(self) -> list[list]:
        """Returns a list of the columns of Square objects. It is a list of lists of each row position from
        the Board object using zipped row positions and mapped into a list for consistency with rows."""
        return list(map(list, zip(*self.board)))   
    
    def get_left_diagonal(self) -> list:
        """Returns a list of the left diagonal of Square objects. It is a sliced list of the game Board object."""
        return list(self.board[i][-(i + 1)] for i in range(len(self.board)))

    def square_is_occupied(self, row: int, column: int) -> bool:
        """Checks if a square is occupied by an Ex or Oh."""
        return self.board[row][column] != 0

    def update_square(self, row: int, column: int, square: str) -> None:
        """Updates the square on the board to an Ex or Oh from the Square class."""
        self.board[row][column] = square

    def update_board(self, row: int, column: int, marker: str) -> None:
        """Updates the board with the last played square."""
        self.game_board.update_square(row, column, marker)


    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        for r, row in enumerate(self.board):
            for c in range(len(row)):
                self.board[r][c] = 0

    def add_player(self, name: str, marker: str) -> None:
        """Adds a player to the player list. Maximum of two players for each game session."""
        if len(self.players) < 2:
            player = self.Player(name, marker)
            self.players.append(player)

    def update_players(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player == self.winner:
                player.won()
            elif self.winner is not None:
                player.lost()

    class Player:
        def __init__(self, name: str, marker: str):
            self.name = name if name else f"Anonymous {self.marker}"
            self.marker = marker
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
        
        def __repr__(self) -> str:
            """Returns a string of information on current attributes of the player for information purposes only. Stored
            as a named tuple. """
            PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "played"])

            player_info = PlayerRepr(
                self.name,
                self.marker,
                self.win_count,
                self.lost_count,
                self.games_played
            )
            return str(player_info)

pair_list = []     
for i in range(9):
    pair_list.append(int_converter(i))
print(pair_list)
for pair in pair_list:
    print(pair_converter(pair))

T = TicTacToe()
# print(T.board)
# print(T.get_columns())
# print(T.get_rows())
T.reset_board()
T.update_square(2, 2, 'X')
T.add_player("Joe", "X")
T.update_players()
print(T.players)
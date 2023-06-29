import os
from itertools import chain
from enum import Enum
from typing import Union, Optional
from collections import Counter, namedtuple
from random import randint
from time import sleep

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
This is an online version of the classic game. Play multiple games per session.
X starts the game. Have fun!
"""

def delay_effect(strings: list[str], delay: float = 0.025):
    for string in strings:
        for char in string:
            print(char, end='', flush=True)
            sleep(delay)
        print()
        sleep(delay)
        
def surround(strings: list[str], symbol: str, offset: int=0) -> str:
    string_list = list(chain.from_iterable(
        string.split("\n") if "\n" in string
        else [string]
        for string in strings
        ))

    border = symbol * ( len(max(string_list, key=len)) + 2*offset)
    output_list = [
        border,
        *[string.center(len(border))for string in string_list],
        border
    ]

    return ["\n" + "\n".join([symbol + string + symbol for string in output_list]) + "\n"]


class Square(Enum):
    """Square Enum class are constants stored as a list to be printed line by line on a game board. A Square Enum is
    Blank, or a player marker Ex or Oh. """

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
    and prints the board as a string using a list of lists of Square objects. It has a board attribute, which is
    a 2D array of Square object, and a horizontal attribute for the row lines. Column lines are created during
    printing of the board using the join method.
    """

    def __init__(self):
        self.board = [
            [Square.BLANK] * 3,
            [Square.BLANK] * 3,
            [Square.BLANK] * 3
        ]

        self.horizontal_line = "* " * 18 + "*"

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

    def create_row(self, row: list[list[Square]]) -> str:
        """Returns a string of a single row of the board from current state of the board attribute."""
        return "\n".join(["*".join(line).center(os.get_terminal_size().columns - 1) for line in zip(*row)])

    def create_board(self) -> str:
        """Returns a string of the complete board created row by row using create_row method for printing."""
        return f"\n{self.horizontal_line.center(os.get_terminal_size().columns - 1)}\n".join(
            [self.create_row([square.value for square in row]) for row in self.board])

    def __str__(self) -> str:
        """Returns full string representation of the board for printing in the Game Class."""
        return self.create_board()

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the board for information purposes only."""
        return f'Board:\n{str(self.board)}\nHorizontal line:\n{self.horizontal_line}'


class Player:
    def __init__(self, name: str, marker: Square, is_computer: bool = False):
        self.marker = marker
        self.name = name if name else f"Anonymous {self.marker}"
        self.is_computer = is_computer
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
        player_string = f"\n{self.name} is playing {self.marker}.\nWin: {self.win_count}, Loss: {self.lost_count}, " \
               f"Draw: {self.get_draw_count()}\n"
        return player_string
    

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the player for information purposes only. Stored
        as a named tuple. """
        PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "played", "is_computer"])

        player_info = PlayerRepr(
            self.name,
            self.marker.name,
            self.win_count,
            self.lost_count,
            self.games_played,
            self.is_computer
        )
        return str(player_info)


class Game:

    def __init__(self):
        self.players: [Player] = []
        self.go_first = True  # when True, player 1 goes first and when False, player 2 goes first.
        self.game_board = Board()  # direct instance of a Board Class object to keep track of game information.
        self.hard_mode = True  # used to keep on basic block or win strategy for the computer player.
        self.winner = None
        self.win_index = 0
        self.win_type = 'None'

    def welcome_box(self) -> None:
        """Prints the "Welcome to Tic Tac Toe" box."""
        print(WELCOME)
        
    def intro(self) -> None:
        delay_effect([INTRO])

    def print_scoreboard(self) -> None:
        """Shows the player statistics for the game."""
        delay_effect(surround([player.__str__() for player in self.players], "#", 20), 0.0025)

    def print_board(self) -> None:
        """Prints the current state of the game board."""
        delay_effect([self.game_board.__str__()], 0.00075)

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

    def _get_rows(self) -> list[list[Square]]:
        """Returns a list of the rows of Square objects. It is the 2D game Board object list of lists."""
        return self.game_board.board

    def _get_columns(self) -> list[list[Square]]:
        """Returns a list of the columns of Square objects. It is a list of lists of each row position from
        the Board object using zipped row positions and mapped into a list for consistency with rows."""
        return list(map(list, zip(*self.game_board.board)))

    def _get_right_diagonal(self) -> list[Square]:
        """Returns a list of the right diagonal of Square objects. It is a sliced list of the game Board object."""
        return list(self.game_board.board[i][i] for i in range(len(self.game_board.board)))

    def _get_left_diagonal(self) -> list[Square]:
        """Returns a list of the left diagonal of Square objects. It is a sliced list of the game Board object."""
        return list(self.game_board.board[i][-(i + 1)] for i in range(len(self.game_board.board)))

    def _check_win(self, squares: list[Square]) -> Optional[Square]:
        """Checks if a line has all the same markers to see if the game has been won."""
        marker, count = Counter(squares).most_common(1)[0]
        if count == len(squares) and marker is not Square.BLANK:
            return marker

    def _check_rows(self) -> bool:
        """Checks for winner in rows. Uses returned Square object to update the winner attributes. False if no Square
        object is assigned. """
        for r, row in enumerate(self._get_rows()):
            if winner := self._check_win(row):
                self._update_winner_info(winner, "row", r)
                return True

    def _check_columns(self) -> bool:
        """Checks for winner in columns. Uses returned Square object to update winner attributes. False if no Square
        object is assigned. """
        for c, column in enumerate(self._get_columns()):
            if winner := self._check_win(column):
                self._update_winner_info(winner, "col", c)
                return True

    def _check_diagonals(self) -> bool:
        """Checks for winner in diagonals. Uses returned Square object to update winner attributes. False if no
        Square object is assigned. """
        if winner := self._check_win(self._get_right_diagonal()):
            self._update_winner_info(winner, "right_diag")
            return True
        if winner := self._check_win(self._get_left_diagonal()):
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
        delay_effect([f"{winner_string} {win_type_dict[self.win_type]}"], 0.025)

    def check_for_winner(self) -> bool:
        """Checks if the game has been won in a row, column or diagonal. Returns boolean."""
        check_winner_funcs = (
            self._check_rows,
            self._check_columns,
            self._check_diagonals
        )
        for f in check_winner_funcs:
            if winner_found := f():
                return winner_found

    def take_turn(self, player: Player) -> None:
        """Gets the row and column from the current player and updates the board tracker and game board for printing.
        Returns the indexed row and column. Returns tuple of integers. """

        row, column = self.prompt_move(player)  # validated in the prompt_move function
        os.system('clear||cls')
        self.update_board(row, column, player.marker)
        self.print_move(player, row, column)
        self.print_board()

    def _prompt_int(self, value: str) -> int:
        valid_input = {1, 2, 3}
        while True:
            try:
                input_value = int(input(f"Enter the {value}: "))
                if input_value in valid_input:
                    return input_value - 1  # Needed for 0 based index

                print(f"\nYou must enter 1, 2, or 3 only for the {value}.")

            except ValueError:
                print("\nYou must enter a number. Try again.")

    def _get_ints(self) -> Union[tuple[int, int], list[int]]:
        print("\nComputer is now thinking.")
        sleep(1.25)

        if self.hard_mode:
            block_positions = []  # makes a list of all possible blocking points on the board of the opponent

            # checks rows, columns, and diagonals for any block positions against the opponent winning,
            # or for winning moves the computer has.prioritizes the win as soon as a winning move is found.
            # logic for control flow depends on the position of each check: rows are in the 0 index position,
            # columns in 1, right diagonal in 2 and left diagonal in 3. Diagonals needed to be double wrapped in
            # lists because rows and columns are lists of lists of Square Objects, which are also lists. This trip

            lines = [self._get_rows(),
                     self._get_columns(),
                     list([self._get_right_diagonal()]),
                     list([self._get_left_diagonal()])
                     ]
            for indicator, line in enumerate(lines):

                for index_1, squares in enumerate(line):
                    marker, count = Counter(squares).most_common(1)[0]
                    if count == (len(squares) - 1) and marker is not Square.BLANK:
                        for index_2, square in enumerate(squares):
                            if indicator == 0:
                                if not self.game_board.square_is_occupied(index_1, index_2):
                                    if marker is not Square.O:
                                        block_positions.append([index_1, index_2])
                                    else:
                                        return index_1, index_2
                            elif indicator == 1:
                                if not self.game_board.square_is_occupied(index_2, index_1):
                                    if marker is not Square.O:
                                        block_positions.append([index_2, index_1])
                                    else:
                                        return index_2, index_1
                            elif indicator == 2:
                                if not self.game_board.square_is_occupied(index_2, index_2):
                                    if marker is not Square.O:
                                        block_positions.append([index_2, index_2])
                                        print(index_2, index_2)
                                    else:
                                        return index_2, index_2
                            else:
                                if not self.game_board.square_is_occupied(index_2, 2 - index_2):
                                    if marker is not Square.O:
                                        block_positions.append([index_2, 2 - index_2])
                                        print(index_2, 2 - index_2)

                                    else:
                                        return index_2, 2 - index_2
            if block_positions:
                # use randomly selected block position from max of three for variety sake
                return block_positions[randint(0, len(block_positions) - 1)]

        # all moves in easy mode are randomly selected,or on hard mode when there is no blocking or winning move
        row = randint(0, 2)
        column = randint(0, 2)
        while self.game_board.square_is_occupied(row, column):
            row = randint(0, 2)
            column = randint(0, 2)
        return row, column

    def prompt_move(self, player: Player) -> Union[tuple[int, int], list[int]]:
        """Validates and formats the user inputted row and column. Checks if the inputted position is occupied."""
        if player.is_computer:
            return self._get_ints()

        delay_effect([f"\nIt is {player.name}'s turn. Select a row and column\n"])

        row = self._prompt_int('row')
        column = self._prompt_int('column')

        while self.game_board.square_is_occupied(row, column):
            print("\nThe square is already occupied. Select another square.")
            row = self._prompt_int('row')
            column = self._prompt_int('column')

        return row, column

    def _one_player(self) -> bool:
        valid_input = {'1', '2', 'one', 'two'}
        while True:
            one_player = input("How many players? One or two: ").lower()
            if one_player in valid_input:
                return one_player in ['1', 'one']
            else:
                print('\nOnly one or two players are allowed.')

    def _select_difficulty_level(self) -> None:
        """Updates the difficulty level boolean when playing against the computer."""
        valid_input = ['1', 'easy', '2', 'hard']
        while True:
            level_of_difficulty = input("\nSelect the level of difficult, Easy or Hard: ").lower()
            if level_of_difficulty in valid_input[:2]:
                self.hard_mode = False
                delay_effect(["\nYou are playing against the computer in easy mode."])
                return
            elif level_of_difficulty in valid_input[2:]:
                delay_effect(["\nYou are playing against the computer in hard mode."])
                return
            else:
                print(f"\nThere is only easy or hard mode. Please select '1' for easy and '2' for hard.")

    def player_order(self) -> None:
        """Prints who is playing what marker and who plays first."""
        delay_effect([f'\n{self.players[-int(self.go_first) + 1].name} plays first.'])
        input('\nPress Enter to start the game.')

    def create_players(self) -> None:
        """Creates two players of the Player class for game play and add the players to the player attribute."""
        one_player = self._one_player()

        # Player one is Ex by default
        name = input("\nPlayer one please enter the name of the player for X: ")
        self.add_player(Player(name, Square.X))

        # Player two is Oh by default. Computer is also Oh by default in one player games
        if one_player:
            self.add_player(Player('Computer', Square.O, True))
            self._select_difficulty_level()
            return
        name = input("\nPlayer two please enter the name of the player for O: ")
        self.add_player(Player(name, Square.O))

    def start_game(self) -> None:
        """Starts the game and creates two players from user input."""
        self.welcome_box()
        self.intro()
        self.create_players()
        self.player_order()
        self.print_board()

    def next_game(self) -> None:
        """Resets the board to blank squares, changes the the order of players, and starts a new game."""
        self.print_scoreboard()
        self.game_board.reset_board()
        self.go_first = not self.go_first
        self.player_order()
        self.print_board()
        self.play_game()

    def print_move(self, player: Player, row: int, column: int) -> None:
        """Returns a string for printing the last played square on the board by the current player."""
        delay_effect([f"\n{player.name} played the square in row {row + 1} and column {column + 1}.\n"])

    def play_game(self) -> None:
        """Main method for playing the game that terminates after all nine squares have been filled or a winner
        has been declared."""
        for i in range(9):
            if self.go_first:
                self.take_turn(self.players[i % 2])
            else:
                self.take_turn(self.players[i % 2 - 1])

            # will start checking for winner after the fourth turn
            if i > 3 and self.check_for_winner():
                self.update_players()
                self.get_winner_info()
                return

        delay_effect(["\nCATS GAME. There was no winner so there will be no chicken dinner."], 0.025)
        self._update_winner_info()
        self.update_players()


def run_games():
    """Starts a game session that keeps track of the two players statistics and allows for multiple plays."""
    games = Game()
    games.start_game()
    games.play_game()
    message = "\nYou must enter 'Yes' or 'No' only."
    while True:
        try:
            play_again = input("\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                games.next_game()
            elif play_again in ['no', 'n']:
                games.print_scoreboard()
                delay_effect(["\nGAME OVER\nThanks for playing tic-tac-toe. See you again soon.\n"])
                break
            else:
                print(message)

        except ValueError:
            print(message)


if __name__ == '__main__':
    run_games()

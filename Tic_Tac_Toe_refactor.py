import os
from enum import Enum
from typing import Union
from collections import Counter, namedtuple
from random import randint
from time import sleep
 

# For Bolding
# BOLD_START = '\033[1m'
# BOLD_END = '\033[0m'    
    
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
 
class Square(Enum):
    """Blank square or marker on the board used by the two players. Square is one of Blank, Ex, or Oh."""
    
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
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'Name: {self.name}\nValue: {self.value}'
    
class Board:
 
    def __init__(self):
        self.board = [
            [Square.BLANK] * 3,
            [Square.BLANK] * 3, 
            [Square.BLANK] * 3
         ]
        
        self.horizontal_line = "* " * 18 + "*"

        
#     def get_horizontal(self) -> str:
#         return "* " * 18 + "*"
    
#     @staticmethod
#     def get_vertical() -> str:
#         return BOLD_START + "*" + BOLD_END
 
    def square_is_occupied(self, row: int, column: int) -> bool:
        """Checks if a square is occupied by an Ex or Oh. Returns bool."""
        return self.board[row][column] != Square.BLANK
 
    def update_square(self, row: int, column: int, square: Square) -> None:
        """Updates the square on the board to Ex, Oh, or Blank from the Square class."""
        self.board[row][column] = square     
        
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        for r, row in enumerate(self.board):
            for c in range(len(row)):
                self.board[r][c] = Square.BLANK
 
    def create_row(self, row: list[list[str]]) -> str:
        """Returns a string of a row of the board from current state of the board. Returns str."""
        return "\n".join(["*".join(line).center(os.get_terminal_size().columns-1) for line in zip(*row)])

    def create_board(self) -> str:
        """Returns a strong of the complete board created row by row for printing."""
        return f"\n{self.horizontal_line.center(os.get_terminal_size().columns-1)}\n".join(
            [self.create_row([square.value for square in row]) for row in self.board])
               
    def __str__(self):
        """Returns full string representation of the board"""
        return self.create_board()
#         return f"\n{self.horizontal.center(os.get_terminal_size().columns-1)}\n".join(
#             [self.print_row([square.value for square in row]) for row in self.board])
    
    def __repr__(self):
        """Returns board information on current attributes"""
        return f'Board:\n{str(self.board)}\nHorizontal line:\n{self.horizontal_line}'

    
class Player:
    def __init__(self, name: str, marker: Square, is_computer: bool = False):
        self.marker = marker
        self.name = name if name else f"Anonymous {self.marker}"
        self.is_computer = is_computer
        self.win_count = 0
        self.lost_count = 0
        self.games_played = 0
 
    def get_draw_count(self) -> int:
        return self.games_played - (self.win_count + self.lost_count)
 
    def game_played(self) -> None:
        self.games_played += 1
    
    def lost(self) -> None:
        self.lost_count += 1     
 
    def won(self) -> None:
        self.win_count += 1    
    
    def __str__(self):
        return f"\n{self.name} is playing {self.marker}.\nWin: {self.win_count}, Loss: {self.lost_count}, Draw: {self.get_draw_count()}"
          
    def __repr__(self):
        """This isn't really necessary"""
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
        self.players: Player = []
        self.go_first = True  # when True, player 1 goes first and when False, player 2 goes first
        self.game_board = Board()
        self.winner = None
        self.win_index = 0
        self.win_type = 'None'
 
    def welcome_box(self) -> None:
        """Prints the "Welcome to Tic Tac Toe" box"""
        print(WELCOME)
 
    def print_scoreboard(self) -> None:
        """Shows the player statistics for the game. Returns None."""
        for player in self.players:
            print(player)
 
    def print_board(self) -> None:
        print(self.game_board)
 
    def add_player(self, player: Player) -> None:
        if len(self.players) < 2:
            self.players.append(player)
 
    def update_players(self) -> None:
        """Updates the game statistics on the two players."""
        for player in self.players:
            player.game_played()
            if player == self.winner:
                player.won()
            else:
                player.lost()
 
    def update_board(self, row: int, column: int, marker: Square) -> None:
        """Updates the board with the last played square."""
        self.game_board.update_square(row, column, marker)
 
    def _check_win(self, squares: list[Square]) -> (int, Square):
        """Checks if a line has all the same markers to see if the game has been won."""
        marker, count = Counter(squares).most_common(1)[0]

        if count == len(squares) and marker is not Square.BLANK:
            return marker
   
 
    def _get_winner_info(self):
        winner_string = f"\nWinner winner chicken dinner. {self.winner.name} is the winner.\n{self.winner.marker} wins in"
        win_type_dict = {
            "row": f"row {self.win_index}.",
            "col": f"column {self.win_index}.",
            "right_diag": "the right diagonal.",
            "left_diag": "the left diagonal."
        }

        print(f"{winner_string} {win_type_dict[self.win_type]}")
    
    
    def _check_rows(self) -> (Square, str, int):
        for r, row in enumerate(self.game_board.board):
            if winner := self._check_win(row):
                self._update_winner_info(winner, "row", r)
                return True   
 
    def _check_columns(self) -> (Square, str, int):
        for c, column in enumerate(zip(*self.game_board.board)):
            if winner := self._check_win(column):
                self._update_winner_info(winner, "col", c)
                return True
    
    def _check_diagonals(self):
        right_diagonal = [self.game_board.board[i][i] for i in range(len(self.game_board.board))]
        if winner := self._check_win(right_diagonal):
            self._update_winner_info(winner, "right_diag")
            return True
        left_diagonal = [self.game_board.board[i][-(i + 1)] for i in range(len(self.game_board.board))]
        if winner := self._check_win(left_diagonal):
            self._update_winner_info(winner, "left_diag")
            return True
           
 
    def _get_winner_with_marker(self, win_marker: Square) -> Player:
        for player in self.players:
            if player.marker == win_marker:
                return player
            
    def _update_winner_info(self, win_marker: str = 'None', win_type: str = 'None', win_index: int = 0):
        self.winner = self._get_winner_with_marker(win_marker)
        self.win_index = win_index + 1
        self.win_type = win_type
    
 
    def check_for_winner(self) -> bool:
        """Checks if the game has been won in a row, column or diagonal. Returns boolean."""
 
        check_funcs = (
            self._check_rows,
            self._check_columns,
            self._check_diagonals
        )
        for f in check_funcs:
            if winner := f():
#                 self.winner = self._get_winner_with_marker(winner)
                return winner
                
#         return False
        
  
    def take_turn(self, player: Player) -> None:
        """Gets the row and column from the current player and updates the board tracker and game board for printing.
        Returns the indexed row and column. Returns tuple of integers. """
 
        row, column = self.prompt_move(player)  # validated in the prompt_move function
        # Experiment with console clearing
        os.system('cls||clear')
        self.update_board(row, column, player.marker)
        self.print_board()
        self.print_move(player, row, column)
 
    @staticmethod
    def _prompt_int(value: str) -> int:
        valid_input = {1, 2, 3}
        while True:
            try:
                input_value = int(input(f"Enter the {value}: "))
                if input_value in valid_input:
                    return input_value - 1  # Need for 0 based index
                
                print(f"\nYou must enter 1, 2, or 3 only for the {value}.")
 
            except ValueError:
                print("\nYou must enter a number. Try again.")
    
    def _get_ints(self) -> tuple([int, int]):
        print("\nComputer is now thinking.")
        sleep(1.25)
        
        block_positions = []
              
        rows = self.game_board.board
        columns = zip(*self.game_board.board)

        
        straight_lines = [rows, columns]

        
        for indicator, line in enumerate(straight_lines):
            for index_1, squares in enumerate(line):
                marker, count = Counter(squares).most_common(1)[0]
                if count == (len(squares) - 1) and marker is not Square.BLANK:
                    for index_2, square in enumerate(squares):
                        if indicator == 0:
                            if not self.game_board.square_is_occupied(index_1, index_2):
                                print(index_1, index_2)
                                sleep(2)
                                if marker is not Square.O:
                                    block_positions.append([index_1, index_2])
                                else:
                                    return index_1, index_2
                        else:
                            if not self.game_board.square_is_occupied(index_2, index_1):
                                print(index_2, index_1)
                                sleep(2)
                                if marker is not Square.O:
                                    block_positions.append([index_2, index_1])
                                else:
                                    return index_2, index_1
        
        
        right_diagonal = [self.game_board.board[i][i] for i in range(len(self.game_board.board))]

        left_diagonal = [self.game_board.board[i][-(i + 1)] for i in range(len(self.game_board.board))]
        diagonal_lines = [right_diagonal, left_diagonal]
        for indicator, squares in enumerate(diagonal_lines):
            
            marker, count = Counter(squares).most_common(1)[0]
            if count == (len(squares) - 1) and marker is not Square.BLANK:
                for index, square in enumerate(squares):
                    if indicator == 0:
                       
                        if not self.game_board.square_is_occupied(index, index):
                           
                            if marker is not Square.O:
                                block_positions.append([index, index])
                            else:
                                return index, index
                    else:
                        if not self.game_board.square_is_occupied(index, 2 - index):
                           
                            if marker is not Square.O:
                                block_positions.append([index, 2 - index])
                            else:
                                return index, 2 - index
                            
            
        
        
        if block_positions:
            return block_positions[randint(0, len(block_positions) - 1)]
        
        row = randint(0, 2)
        column = randint(0, 2)
        while self.game_board.square_is_occupied(row, column):
            print("Still thinking.")
            sleep(1.25)
            row = randint(0, 2)
            column = randint(0, 2)
        return row, column
 
    def prompt_move(self, player: Player) -> tuple([int, int]):
        """Validates and formats the user inputted row and column. Checks if the inputted position is occupied."""
        
        if player.is_computer:
            return self._get_ints()
        
        print(f"\nIt is {player.name}'s turn. Select a row and column\n")
 
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
            one_player = input("\nHow many players? One or two: ").lower()
            if one_player in valid_input:
                return one_player in ['1', 'one']
            else:
                print('\nOnly one or two players are allowed.')
      
    def player_order(self):
        print('\n')
        for player in self.players:
            print(f'{player.name} is playing {player.marker.name}.')
            
        if self.go_first:
            print(f'{self.players[0].name} plays first.')
        else:
            print(f'{self.players[1].name} plays first.')
        
        input('\nPress Enter to start the game.')
    
    def create_players(self) -> tuple[Player]:
        """Creates two players of the Player class for game play. Returns a tuple of two Players."""
        one_player = self._one_player()
        
        # Player one is Ex by default
        name = input("\nPlayer one please enter the name of the player for X: ")
        self.add_player(Player(name, Square.X))
        
        # Player two is Oh by default. Computer is also O by default in one player games
        if one_player:
            self.add_player(Player('Computer', Square.O, True))
            return
        name = input("\nPlayer two please enter the name of the player for O: ")
        self.add_player(Player(name, Square.O))
        
 
    def start_game(self) -> None:
        """Starts the game and creates two players from user input. Returns None."""
        self.welcome_box()
        self.create_players()
        self.player_order()
        self.print_board()
 
    def next_game(self) -> None:
        """Resets the squares to zero array and board to blank squares. Returns None."""
        self.print_scoreboard()
        self.game_board.reset_board()
        self.go_first = not self.go_first
        self.player_order()
        self.print_board()
        self.play_game()
 
    def print_move(self, player: Player, row: int, column: int) -> str:
        """Returns a string for printing the last played square on the board by the current player."""
        print(f"\n{player.name} played the square in row {row + 1} and column {column + 1}.\n", end=' ')
 
    def play_game(self) -> None:
        """Main method for playing the game that terminates after all nine squares have been filled or a winner has
        been declared. Returns None. """
        for i in range(9):
            if self.go_first:
                self.take_turn(self.players[i % 2])
            else:
                self.take_turn(self.players[i % 2 - 1])
 
            # will start checking for winner after the fourth turn
            if i > 3 and self.check_for_winner():
                self.update_players()
                self._get_winner_info()
                return
           
        print("\nCATS GAME. There was no winner so there will be no chicken dinner.")
        self._update_winner_info()
        self.update_players()
#         for player in self.players:
#             player.game_played()

                
def run_games():
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
                print("\nGAME OVER\nThanks for playing tic-tac-toe. See you again soon.\n")
                break
            else:
                print(message)
 
        except ValueError:
            print(message)
 
 
if __name__ == '__main__':
    run_games()
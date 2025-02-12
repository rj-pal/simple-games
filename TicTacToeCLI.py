from enum import Enum
from itertools import chain
from time import sleep
import os
from Game import TicTacToe, winner_info

class Square(Enum):
    """Represents a single Tic Tac Toe square: Blank, X, or O."""
    BLANK = ["            "] * 5
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
        return self.name

    def __repr__(self) -> str:
        return f'Name: {self.name}\nValue: {self.value}'

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

horizontal_line = "* " * 18 + "*"

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('clear||cls')

def delay_effect(strings: list[str], delay: float = 0.025, word_flush: bool = True) -> None:
    """Creates the effect of the words or characters printed one letter or line at a time. 
    Word_flush True delays each character. False delays each complete line in a list. """
    #     Used when testing so that can play the games quicker
    if delay != 0:
        delay = 0
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


# def surround_string(strings: list[str], symbol: str, offset: int = 0) -> list[str]:
#     """Creates a bordered box around a given string list."""
#     string_list = list(chain.from_iterable(s.split("\n") if "\n" in s else [s] for s in strings))
#     border = symbol * (len(max(string_list, key=len)) + 2 * offset)
#     output_list = [border, *[s.center(len(border)) for s in string_list], border]
#     return ["\n" + "\n".join([symbol + s + symbol for s in output_list]) + "\n"]

def get_player_names() -> None:
        """Creates two players of the Player class for game play and add the players to the player attribute."""
        # Checks for one or two players first. Player one is Ex by default. 
        # Player two is Oh by default. Computer is also Oh by default in one player games.
        # one_player = self._one_player()

        name_x = input("\nPlayer one please enter the name of the player for X: ")
        # self.add_player(Player(name, Square.X))

        # if one_player:
        #     difficulty = self._select_difficulty_level()
        #     self.add_player(AIPlayer(difficulty=difficulty))
        # else:
        name_y = input("\nPlayer two please enter the name of the player for O: ")
            # self.add_player(Player(name, Square.O))
        return name_x, name_y


def one_player() -> bool:
        """Sets the game to one or two players."""
        valid_input = {'1', '2', 'one', 'two'}
        while True:
            one_player = input("How many players? One or two: ").lower()
            if one_player in valid_input:
                return one_player in ['1', 'one']
            else:
                print('\nOnly one or two players are allowed.\n')

def prompt_int(value: str) -> int:
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

def prompt_move(): # -> Union[tuple[int, int], list[int]]:
        """Validates and formats the user inputted row and column. Checks if the inputted position is occupied."""

        row = prompt_int('row')
        column = prompt_int('column')

        return row, column

def board_translator(raw_board: list[list[int | str]]) -> list[list[Square]]:
    """Converts a raw board with 0, 'x', 'o' into Square enum values."""
    mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O}
    return [[mapping[cell] for cell in row] for row in raw_board]

def create_row(row: list[list[Square]]) -> str:
    """Returns a string of a single row of the board from current state of the board attribute."""
    return "\n".join(["*".join(line).center(os.get_terminal_size().columns - 1) for line in zip(*row)])

def create_board(game_board) -> str:
    """Returns a string of the complete board created row by row using _create_row method for printing."""
    return f"\n{horizontal_line.center(os.get_terminal_size().columns - 1)}\n".join(
        [create_row([square.value for square in row]) for row in game_board])

def print_board(game_board) -> None:
    """Prints the current state of the game board. Printed line by line."""
    game_board = board_translator(game_board)
    delay_effect([create_board(game_board)], 0.00075, False)

def print_start_game():
     print(WELCOME)
     print(delay_effect([INTRO]))

def print_first_prompt(name):
     delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])

def print_second_prompt(name):
    print("\nThe square is already occupied. Select another square.")
    delay_effect([f"\nIt is {name}'s turn again. Select a free sqaure.\n"])

def print_scoreboard(player_list) -> None:
        """Shows the player statistics for the game. Printed line by line."""
        delay_effect(surround_string([player.__str__() for player in player_list], "#", 25), 0.00075, False)
   

def set_up_game():
    print_start_game()
    if one_player():
        x, y = get_player_names()
    else:
        x, y = get_player_names()
    Game = TicTacToe()
    Game.update_player_info(x, "x")
    Game.update_player_info(y, "o")

    return Game

def play_game(Game) -> None:
        # moves = [(1, 1, 'x'), (0, 1, 'o'), (0,0, "x"), (2,2, "o"), (2,0,"x"), (2,1,"o"), (1,0,"x")]
        for i in range(Game.board_size):
            Game.round_count += 1  
            player = Game.players[i % 2]
            name = player.get_player_name()
            print_first_prompt(name)
            while True:
                r, c = prompt_move()
                if Game.make_move(r, c, player.marker):
                    break
                else:
                    print_second_prompt(name)
            
            # game_board = board_translator(Game.board.get_board())
            print_board(Game.board.get_board())

            if i >= 4 and Game.win.check_for_winner():
                winner_info(*Game.win.get_win_info())
                print(Game.move_list)
                Game.update_winner_info()
                Game.update_players_stats()
                Game.print_winner()
                print(Game.print_stats())
                break
    
        else:
             print("Tie Game")

def play_again():
     message = "\nYou must enter 'Yes' or 'No' only."
     while True:
        try:
            play_again = input("\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                return True
            elif play_again in ['no', 'n']:
                delay_effect(
                    ["\nGame session complete.\n\nThanks for playing Tic-Tac-Toe. See you in the next session.\n"])
                return False
            else:
                print(message)

        except ValueError:
            print(message)

if __name__ == '__main__':
    Game = set_up_game()
    play_game(Game)
    print_scoreboard(Game.players)
    multiplay = play_again()
    while multiplay:
         Game.reset_board()
         play_game(Game)
         multiplay = play_again()
         print_scoreboard(Game.players)


              
         
    
    
    


  
    exit()


# class TicTacToeBoard:
#     """Represents the Tic Tac Toe board."""
#     def __init__(self, board):
#         self.board = board
#         self.horizontal_line = "-" * (os.get_terminal_size().columns - 1)

#     def __str__(self) -> str:
#         return create_board(self.board)

#     def __repr__(self) -> str:
#         return f'Board:\n{self.board}\nHorizontal line:\n{self.horizontal_line}'


# class TicTacToeCLI:
#     """Command-line interface for Tic Tac Toe."""
#     def __init__(self, board, players=None, go_first=None):
#         self.board = board
#         self.players = players
#         self.go_first = go_first

#     def print_welcome_box(self) -> None:
#         """Displays the welcome banner."""
#         print(WELCOME)

#     def print_intro(self) -> None:
#         """Displays the game introduction."""
#         delay_effect([INTRO])

#     def print_game_over(self) -> None:
#         """Flashes the game over banner."""
#         clear_screen()
#         for _ in range(5):
#             print(GAMEOVER.center(os.get_terminal_size().columns - 1), end='\r')
#             sleep(0.75)
#             clear_screen()
#             sleep(0.5)

#     def print_board(self) -> None:
#         """Prints the current state of the board."""
#         delay_effect([str(self.board)], 0.00075, False)

#     def print_scoreboard(self) -> None:
#         """Displays the scoreboard with a border."""
#         delay_effect(surround_string([str(p) for p in self.players], "#", 25), 0.00075, False)

#     def print_move(self, player, row: int, column: int) -> None:
#         """Announces the last move."""
#         delay_effect([f"\n{player.name} played row {row + 1}, column {column + 1}.\n"])

#     def print_first_player(self) -> None:
#         """Announces the first player."""
#         delay_effect([f'\n{self.players[-int(self.go_first) + 1].name} plays first.'])
#         input('\nPress Enter to start the game.')




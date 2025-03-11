import os
from time import sleep
from typing import Optional
import utils.display as GameCLI
from games.Game import TicTacToe
from utils.strings import BOARDLINE_TICTAC, WELCOME_TICTACTOE, INTRO_TICTACTOE, GAMEOVER, THINKING

# class TicTacToeCLI(GameCLI):

#     WELCOME = WELCOME_TICTACTOE
#     INTRO = INTRO_TICTACTOE
#     GAMEOVER = GAMEOVER
#     ONE = "X"
#     TWO = "O"

# WELCOME_TICTACTOE = """
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#    *                                                                         *
#    *                                                                         *
#    *     *       *   * * *   *       * * *    *  *      *   *     * * *      *
#    *      *  *  *    * *     *      *        *    *    *  *  *    * *        *
#    *       *   *     * * *   * * *   * * *    *  *    *       *   * * *      *
#    *                                                                         *
#    *                                                                         *
#    *      * * *   *  *                                                       *
#    *        *    *    *                                                      *
#    *        *     *  *                                                       *
#    *                                                                         *
#    *                                                                         *
#    *      * * *   *    * *     * * *    *     * *     * * *   * *   * * *    *
#    *        *     *   *          *     * *   *          *    *   *  * *      *
#    *        *     *    * *       *    *   *   * *       *     * *   * * *    *
#    *                                                                         *
#    *                                                                         *
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# """

# GAMEOVER = """
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#    *                                                                         *
#    *                                                                         *
#    *               * * *        **        *       *    * * * *               *
#    *              *            *  *       * *   * *    *                     *
#    *              *   * *     *    *      *   *   *    * * *                 * 
#    *              *     *    *      *     *       *    *                     *
#    *               * * *    *        *    *       *    * * * *               *
#    *                                                                         *
#    *                                                                         *
#    *                *  *     *       *    * * * *     *  *  *                *
#    *              *      *    *     *     *           *      *               *
#    *              *      *     *   *      * * *       *  *  *                *
#    *              *      *      * *       *           *      *               *
#    *                *  *         *        * * * *     *       *              *
#    *                                                                         *
#    *                                                                         *
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# """

# INTRO = """
# This is an online version of the classic game. Play multiple games per session
# against and opponent or the computer. X starts the game.
# """
# THINKING = "\nComputer is now thinking."
# DRAW = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"

# LINE = "* " * 18 + "*" # for Tic Tac Toe


# def set_console_window_size(width: float, height: float) -> None:
#     """Sets the console window to fit the board to the screen better."""
#     # Check the platform (Windows or Unix-based)
#     os.system('cls||clear')
#     if os.name == 'nt':
#         # Windows platform
#         os.system(f'mode con: cols={width} lines={height}')
#     else:
#         # Unix-based platforms (Linux, macOS)
#         os.system(f'printf "\033[8;{height};{width}t"')


# def clear_screen() -> None:
#     """Clears the terminal screen."""
#     os.system('clear||cls')


# def delay_effect(strings: list[str],
#                  delay: float = 0.025,
#                  word_flush: bool = True) -> None:
#     """Creates the effect of the words or characters printed one letter or line at a time. 
#     Word_flush True delays each character. False delays each complete line in a list. """
#         # Used when testing so that can play the games quicker
#     # if delay != 0:
#     #     delay = 0
#     for string in strings:
#         for char in string:
#             print(char, end='', flush=word_flush)
#             sleep(delay)
#         print()
#         sleep(delay)


# def surround_string(strings: list[str],
#                     symbol: str,
#                     offset: int = 0) -> list[str]:
#     """Creates a border around any group of sentences. Used to create the scoreboard for the players."""
#     string_list = list(
#         chain.from_iterable(
#             string.split("\n") if "\n" in string else [string]
#             for string in strings))

#     border = symbol * (len(max(string_list, key=len)) + 2 * offset)
#     output_list = [
#         border, *[string.center(len(border)) for string in string_list], border
#     ]

#     return [
#         "\n" + "\n".join([symbol + string + symbol
#                           for string in output_list]) + "\n"
#     ]


# def get_player_names() -> None:
#     """Creates two players of the Player class for game play and add the players to the player attribute."""

#     name_x = input(
#         "\nPlayer one please enter the name of the player for X or press enter: "
#     )

#     name_y = input(
#         "\nPlayer two please enter the name of the player for O or press enter: "
#     )

#     return name_x, name_y


# def get_player_name() -> None:
#     """Creates two players of the Player class for game play and add the players to the player attribute."""
#     name_x = input(
#         "\nPlayer one please enter the name of the player for X or press enter: "
#     )
#     return name_x


# def one_player() -> bool:
#     """Sets the game to one or two players."""
#     valid_input = {'1', '2', 'one', 'two'}
#     while True:
#         one_player = input("How many players? One or two: ").lower()
#         if one_player in valid_input:
#             return one_player in ['1', 'one']
#         else:
#             print('\nOnly one or two players are allowed.\n')


def select_difficulty_level() -> Optional[bool]:
    """Updates the difficulty level boolean when playing against the computer."""
    valid_input = ['1', 'easy', '2', 'intermediate', '3', 'hard']
    while True:
        level_of_difficulty = input(
            "\nSelect the level of difficult for the AI: Easy, Intermediate or Hard: "
        ).lower()
        if level_of_difficulty in valid_input[:2]:
            GameCLI.delay_effect(
                ["\nYou are playing against the computer in easy mode."])
            return None
        elif level_of_difficulty in valid_input[2:4]:
            GameCLI.delay_effect([
                "\nYou are playing against the computer in intermediate mode."
            ])
            return False
        elif level_of_difficulty in valid_input[4:]:
            GameCLI.delay_effect(
                ["\nYou are playing against the computer in hard mode."])
            return True
        else:
            print(
                "\nThere is only easy, intermediate or hard mode.\nPlease select '1' for easy, '2' for "
                "intermediate or '3' for hard.")


# def prompt_int(value: str) -> int:
#     """Returns two integers for a row and column move from the player input. Only allows 
#         for 1, 2, or 3 with each integer corresponding to a row and then a column."""
#     valid_input = {1, 2, 3}
#     while True:
#         try:
#             input_value = int(input(f"Enter the {value}: "))
#             if input_value in valid_input:
#                 return input_value - 1  # Needed for 0 based index

#             print(f"\nYou must enter 1, 2, or 3 only for the {value}.\n")

#         except ValueError:
#             print("\nYou must enter a number. Try again.\n")


# def prompt_move():  # -> Union[tuple[int, int], list[int]]:
#     """Validates and formats the user inputted row and column. Checks if the inputted position is occupied."""

#     row = prompt_int('row')
#     column = prompt_int('column')

#     return row, column

# MAINFUNCTION
# def board_translator(raw_board: list[list[int, str]]) -> list[list[Square]]:
#     """Converts a raw board with 0, 'x', 'o' into Square enum values."""
#     mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y}
#     return [[mapping[cell] for cell in row] for row in raw_board]

# MAIN FUNTION
# def create_row(row: list[list[Square]]) -> str:
#     """Returns a string of a single row of the board from current state of the board attribute."""
#     return "\n".join([
#         "*".join(line).center(os.get_terminal_size().columns - 1)
#         for line in zip(*row)
#     ])

# Function with no centring
# def create_row(row: list[list[str]]) -> str:
#     """Returns a string of a single row of the board with elements in red, but not the '*' separator."""
#     return "\n".join([
#         "*".join(line)
#         for line in zip(*row)
#     ])

# Test function
# def create_row(row: list[list[str]]) -> str:
#     """Returns a string of a single row of the board with 'line' in red."""
#     return "\n".join([
#         f"\033[31m{'*'.join(line)}\033[0m".center(os.get_terminal_size().columns - 1)
#         for line in zip(*row)
#     ])

# MAIN FUNCTION
# def create_board(game_board) -> str:
#     """Returns a string of the complete board created row by row using _create_row method for printing."""
#     return f"\n{LINE.center(os.get_terminal_size().columns - 1)}\n".join(
#         [create_row([square.value for square in row]) for row in game_board])

# Function with no centring
# def create_board(game_board) -> str:
#     """Returns a string of the complete board created row by row using _create_row method for printing."""
#     return f"\n{LINE}\n".join(
#         [create_row([square.value for square in row]) for row in game_board])


# def print_board(game_board) -> None:
#     """Prints the current state of the game board. Printed line by line."""
#     game_board = board_translator(game_board)
#     delay_effect([create_board(game_board)], 0.00075, False)


# def print_current_move(name: str, row: int, column: int) -> None:
#     """Returns a string for printing the last played square on the board by the current player."""
#     delay_effect([
#         f"\n{name} played the square in row {row + 1} and column {column + 1}.\n"
#     ])


# def print_start_game():
#     print(WELCOME_TICTACTOE)
#     delay_effect([INTRO])


# def print_game_over() -> None:
#     """Prints a flashing "Game Over" when a winner has been declared"""
#     print()
#     clear_screen()
#     for _ in range(5):
#         print(GAMEOVER.center(os.get_terminal_size().columns - 1), end='\r')
#         sleep(0.75)
#         clear_screen()
#         sleep(0.5)
#     print()


# def print_first_player(name: str) -> None:
#     """Prints who is plays first and their marker."""
#     Display.delay_effect([f'\n{name} plays first.'])
#     input('\nPress Enter to start the game.')


# def print_player_turn_prompt(name: str):
#     Display.delay_effect([f"\nIt is {name}'s turn. Select a row and column\n"])


# def print_square_occupied_prompt(name: str):
#     print("\nThe square is already occupied. Select another square.")
#     Display.delay_effect([f"\nIt is {name}'s turn again. Select a free sqaure.\n"])

# def print_current_move(name: str, row: int, column: int) -> None:
#     """Returns a string for printing the last played square on the board by the current player."""
#     Display.delay_effect([
#         f"\n{name} played the square in row {row + 1} and column {column + 1}.\n"
#     ])

# def print_scoreboard(player_list) -> None:
#     """Shows the player statistics for the game. Printed line by line."""
#     Display.delay_effect(
#         Display.surround_string([player.__str__() for player in player_list], "#", 25),
#         0.00075, False)


# def print_winner_info(name: str, marker: str, win_type: str, win_index: int) -> None:
#     """Displays the information of the winner of the game using the winner attributes."""
#     if all(info is None for info in (name, marker, win_type)):
#         draw_string = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"
#         Display.delay_effect(Display.surround_string([draw_string], "#", 9), 0.00075, False)
#     else:

#         winner_string = f"\nWinner winner chicken dinner. {name} is the winner.\n{marker.upper()} " \
#                         f"wins in"
#         win_type_dict = {
#             "row": f"row {win_index + 1}.",
#             "column": f"column {win_index + 1}.",
#             "right_diagonal": "the right diagonal.",
#             "left_diagonal": "the left diagonal."
#         }
#         winner_string = f"{winner_string} {win_type_dict[win_type]}\n"
#         Display.delay_effect(Display.surround_string([winner_string], "#", 9), 0.00075,
#                      False)  # customize the size of the box and speed of delay


def set_up_game():
    game = TicTacToe()
    if GameCLI.one_player():
        difficulty = select_difficulty_level()
        name_dictionary = {
            None: "CPU Easy",
            False: "CPU Intermediate",
            True: "CPU Hard"
        }
        game.create_ai_player(name=name_dictionary[difficulty],
                              difficulty=difficulty)
        x = GameCLI.get_player_name()
        game.update_player_name(x, "x")

    else:
        x, y = GameCLI.get_player_names()
        game.update_player_name(x, "x")
        game.update_player_name(y, "o")

    return game


def play_game(game) -> None:
    for i in range(game.board_size):
        # print(game.round_count)
        if game.go_first:
            player = game.players[i % 2]
        else:
            player = game.players[i % 2 - 1]

        name = player.get_player_name()
        if i == 0:
            GameCLI.print_first_player(name)
            GameCLI.clear_screen()

        if isinstance(player, TicTacToe.TicTacToePlayer):

            GameCLI.print_player_turn_prompt(name)
            while True:
                row, col = GameCLI.prompt_move()
                if game.make_move(row, col, player.marker):
                    break
                else:
                    GameCLI.print_square_occupied_prompt(name)
        elif isinstance(player, TicTacToe.AIPlayer):
            print(THINKING)
            sleep(1.5)
            row, col = player.move(game.board)
            game.make_move(row, col, player.marker)

        GameCLI.clear_screen()
        GameCLI.print_current_move(name, row, col)
        GameCLI.print_board(game.board.get_board(), BOARDLINE_TICTAC)

        if i >= 4 and game.check_winner():
            GameCLI.print_game_over(GAMEOVER)
            GameCLI.print_board(game.board.get_board(), BOARDLINE_TICTAC)
            break
    
    
    game.update_winner_info()
    game.update_players_stats()
    winner = game.get_winner_attributes()
    GameCLI.print_winner_info(*winner)
    # game.print_winner()
    # print(game.move_list)
    game.reset_game_state()


def play_again():
    message = "\nYou must enter 'Yes' or 'No' only."
    while True:
        try:
            play_again = input(
                "\nWould you like to play again? Enter yes or no: ").lower()
            if play_again in ['yes', 'y']:
                return True
            elif play_again in ['no', 'n']:
                GameCLI.delay_effect([
                    "\nGame session complete.\n\nThanks for playing Tic-Tac-Toe. See you in the next session.\n"
                ])
                return False
            else:
                print(message)

        except ValueError:
            print(message)


def run():
    GameCLI.set_console_window_size(85, 30) # console dimensions: width, height
    GameCLI.print_start_game(WELCOME_TICTACTOE, INTRO_TICTACTOE)
    game = set_up_game()
    # play_game(Game)
    # multiplay = play_again()
    # print_scoreboard(Game.players)
    multiplay = True
    while multiplay:
        # GameCLI.clear_screen()
        play_game(game)
        multiplay = play_again()
        GameCLI.print_scoreboard(game.players)
        game.reset_board()
    exit()

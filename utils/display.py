import os
from time import sleep
from itertools import chain
from utils.square import Square
from typing import Union

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


def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('clear||cls')


def delay_effect(strings: list[str],
                 delay: float = 0.025,
                 word_flush: bool = True) -> None:
    """Creates the effect of the words or characters printed one letter or line at a time. 
    Word_flush True delays each character. False delays each complete line in a list. """
        # Used when testing so that can play the games quicker
    if delay != 0:
        delay = 0
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)


def surround_string(strings: list[str],
                    symbol: str,
                    offset: int = 0) -> list[str]:
    """Creates a border around any group of sentences. Used to create the scoreboard for the players."""
    string_list = list(
        chain.from_iterable(
            string.split("\n") if "\n" in string else [string]
            for string in strings))

    border = symbol * (len(max(string_list, key=len)) + 2 * offset)
    output_list = [
        border, *[string.center(len(border)) for string in string_list], border
    ]

    return [
        "\n" + "\n".join([symbol + string + symbol
                          for string in output_list]) + "\n"
    ]


def board_translator(raw_board: list[list[int, str]]) -> list[list[Square]]:
    """Converts a raw board with 0, 'x', 'o', 'r', 'y' into Square enum values."""
    mapping = {0: Square.BLANK, "x": Square.X, "o": Square.O, "r": Square.R, "y": Square.Y}
    return [[mapping[cell] for cell in row] for row in raw_board]


def create_row(row: list[list[Square]]) -> str:
    """Returns a string of a single row of the board from current state of the board attribute."""
    return "\n".join([
        "*".join(line).center(os.get_terminal_size().columns - 1)
        for line in zip(*row)
    ])

def create_board(game_board: list[list[Union[int, str]]], line: str) -> str:
    """Returns a string of the complete board created row by row using _create_row method for printing."""
    return f"\n{line.center(os.get_terminal_size().columns - 1)}\n".join(
        [create_row([square.value for square in row]) for row in game_board])

def print_board(game_board: list[list[Union[int, str]]], line: str) -> None:
    """Prints the current state of the game board. Printed line by line."""
    game_board = board_translator(game_board)
    delay_effect([create_board(game_board, line)], 0.00075, False)

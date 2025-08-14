"""
console.py 
Author: Robert Pal
Updated: 2025-08-14

This module contains general helper functions for managing the console in Command Line Applications.
"""
import os
from time import sleep
from typing import Union

# ==== Helper functions for console and screen management at os level in controlling overall command line display ====
def clear_screen() -> None:
    """Clears all printed input on terminal screen for display purposes."""
    os.system('cls' if os.name == 'nt' else 'clear')


def set_console_window_size(width: float, height: float) -> None:
    """Sets the console window size to fit the board better for both Windows."""
    os.system('cls||clear')
    # Make it compliant for Linux/MacOS and Windows systems
    if os.name == 'nt':
        os.system(f'mode con: cols={width} lines={height}')
    else:
        os.system(f'printf "\033[8;{height};{width}t"')


# ==== Helper for functions for string management in creating typewriter effect on output to user  ====
def delay_effect(strings: Union[list[str], str], delay: float = 0.015, word_flush: bool = True) -> None:
    """
    Creates the effect of printing line by line or character by character. Speed of printing can be changed with delay parameter.
    When word_flush is true, each character or letter will print one by one according to the delay speed.
    When word_flush is false, each individual line will print one by one according to the delay speed.
    Requires a list of strings to be displayed. If a string is passed, each character will be printed on its onw line. 
    """
    # Used for testing to speed up output
    # if delay != 0:
    #     delay = 0  
    for string in strings:
        for char in string:
            print(char, end='', flush=word_flush)
            sleep(delay)
        print()
        sleep(delay)

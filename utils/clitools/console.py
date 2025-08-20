"""
console.py 
Author: Robert Pal
Updated: 2025-08-19

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
    """Set the console window size.

    This function adjusts the window dimensions for both Windows and Linux/MacOS systems to better fit the game board display.

    Args:
        width: The desired width for the console window.
        height: The desired height for the console window.
    """
    os.system('cls||clear')
    # Make it compliant for Linux/MacOS and Windows systems
    if os.name == 'nt':
        os.system(f'mode con: cols={width} lines={height}')
    else:
        os.system(f'printf "\033[8;{height};{width}t"')


# ==== Helper for functions for string management in creating typewriter effect on output to user  ====
def delay_effect(strings: Union[list[str], str], delay: float = 0.015, word_flush: bool = True) -> None:
    """Create a typewriter effect for printing text.

    This function prints either line by line or character by character, with the speed controlled by the `delay` parameter.

    Args:
        strings: A single string or a list of strings to be displayed.
        delay: The speed of the printing effect. Defaults to 0.015 seconds.
        word_flush: If True, prints character by character. If False, prints line by line. Defaults to True.
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

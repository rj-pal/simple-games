"""
games.py 
Author: Robert Pal
Updated: 2025-08-05

This module contains three game engines.
"""

from typing import Union, Optional
from copy import deepcopy
from time import sleep
from utils.errors import *

def int_converter(number, columns):
    return divmod(number, columns)

def pair_converter(pair, columns):
    return pair[0]*columns + pair[1]

# def board(rows: int, columns: int):
#     board = []
#     for i in range(rows):
#         if i == 1:
#             board.append(["x" for _ in range(columns)])
#         else:
#             board.append([0 for _ in range(columns)])
#     return board

            
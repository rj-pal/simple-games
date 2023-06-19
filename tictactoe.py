import os
from enum import Enum


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



class Marker(Enum):
    """Content of a cell or Marker used by a Player."""
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

    def get_string(self) -> str:
        return f"'{self.name}'"
    
class Player:

    # marker must be 1 or 2 for tic-tac-toe game
    def __init__(self, name: str, marker: int):
        self.name = name
        self.marker = marker
        self.win_count = 0
        self.games_played = 0

    def get_marker_type(self) -> str:
        """Returns a string for the game play mark 'X' or 'O'"""
        if self.marker == 1:
            return "'X'"
        elif self.marker == 2:
            return "'O'"
        else:
            return "Unknown marker for tic-tac-toe"

    @classmethod
    def construct_player(cls, name: str, marker: int):
        """Class Method to initiate a Player Object that has a default name built in for empty strings."""
        if type(name) is not str:
            print("Error in Player Name")
            return

        if type(marker) is not int:
            print("Error in Player Marker")
            return

        if not name:
            name = 'Anonymous' + str(marker)

        return Player(name, marker)


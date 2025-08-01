"""
string.py 
Author: Robert Pal
Updated: 2025-08-01

This module contains all user-facing string messages for the games Tic Tac Toe, Connect 4 and Solitaire used in the Command Line Application. 
The strings are stored as constants and used for displaying information or states of game play, including board configurations. All strings are 
for display directly to the user in game play for each game.
"""

# ==== Full Screen Game Message Strings ====

# ---- Game Start Banners ----
# A large ASCII art banner displayed at the start of the Tic Tac Toe game.
WELCOME_TICTACTOE = """
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
# A large ASCII art banner displayed at the start of the Connect 4 game.
WELCOME_CONNECT4 = """
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
   *       * * *    *  *   *    *   *    *  * * *   * * *  * * *    * *      *
   *      *        *    *  *  * *   *  * *  * *    *         *     *  * *    *
   *       * * *    *  *   *    *   *    *  * * *   * * *    *        *      *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
# A large ASCII art banner displayed at the start of the Solitaire game.
WELCOME_SOLITAIRE = """
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
   *       * * *    *  *     *       *   * * *    *     *   *  *    * * *    *
   *        *      *    *    *       *     *     * *    *   *  *    * *      *
   *      * * *     *  *     * * *   *     *    *   *   *   *   *   * * *    *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
# ---- Game Outcome Banners ----
# A large ASCII art banner displayed when any game concludes or a player wins.
GAMEOVER = [
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *",
    "*                                                                         *",
    "*                                                                         *",
    "*               * * *        **        *       *    * * * *               *",
    "*              *            *  *       * *   * *    *                     *",
    "*              *   * *     *    *      *   *   *    * * *                 *",
    "*              *     *    *      *     *       *    *                     *",
    "*               * * *    *        *    *       *    * * * *               *",
    "*                                                                         *",
    "*                                                                         *",
    "*                *  *     *       *    * * * *     *  *  *                *",
    "*              *      *    *     *     *           *      *               *",
    "*              *      *     *   *      * * *       *  *  *                *",
    "*              *      *      * *       *           *      *               *",
    "*                *  *         *        * * * *     *       *              *",
    "*                                                                         *",
    "*                                                                         *",
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
]
# A large ASCII art banner displayed when the player 'X' wins in Tic Tac Toe.
XWINS = [
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *",
    "*                                                                         *",
    "*                                                                         *",
    "*                            *       *                                    *",
    "*                              *   *                                      *",
    "*                                *                                        *",
    "*                              *   *                                      *",
    "*                            *       *                                    *",
    "*                                                                         *",
    "*         *             *     * * *      *       *       * * *            *",
    "*         *             *       *        *  *    *      *     *           *",
    "*          *     *     *        *        *    *  *        *               *",
    "*           *  *   *  *         *        *       *      *    *            *",
    "*            *       *        * * *      *       *       * * *            *",
    "*                                                                         *",
    "*                                                                         *",
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
]
# A large ASCII art banner displayed when the player 'O' wins in Tic Tac Toe.
OWINS = [
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *",
    "*                                                                         *",
    "*                                                                         *",
    "*                            *   *                                        *",
    "*                          *       *                                      *",
    "*                          *       *                                      *",
    "*                          *       *                                      *",
    "*                            *   *                                        *",
    "*                                                                         *",
    "*         *             *     * * *      *       *       * * *            *",
    "*         *             *       *        *  *    *      *     *           *",
    "*          *     *     *        *        *    *  *        *               *",
    "*           *  *   *  *         *        *       *      *    *            *",
    "*            *       *        * * *      *       *       * * *            *",
    "*                                                                         *",
    "*                                                                         *",
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
]
# A large ASCII art banner displayed when the Red player wins in Connect 4.
REDWINS = [
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *",
    "*                                                                         *",
    "*                                                                         *",
    "*                 *  *  *        *  *  *      *  * *                      *",
    "*                 *      *       *            *      *                    *",
    "*                 *  *  *        * * *        *       *                   *",
    "*                 *      *       *            *      *                    *",
    "*                 *       *      *  *  *      *  * *                      *",
    "*                                                                         *",
    "*          *             *     * * *     *       *       * * *            *",
    "*          *             *       *       *  *    *      *     *           *",
    "*           *     *     *        *       *    *  *        *               *",
    "*            *  *   *  *         *       *       *      *    *            *",
    "*             *       *        * * *     *       *       * * *            *",
    "*                                                                         *",
    "*                                                                         *",
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
]
# A large ASCII art banner displayed when the Yellow player wins in Connect 4.
YELLOWWINS = [
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *",
    "*                                                                         *",
    "*                                                                         *",
    "*   *       *    *  *  *   *        *          * *      *             *   *",
    "*   *       *    *         *        *        *     *    *             *   *",
    "*    *  *  *     * * *     *        *       *       *    *     *     *    *",
    "*       *        *         *        *        *     *      *  *   *  *     *",
    "*       *        *  *  *   * *  *   * *  *    * * *        *       *      *",
    "*                                                                         *",
    "*         *             *     * * *      *       *       * * *            *",
    "*         *             *       *        *  *    *      *     *           *",
    "*          *     *     *        *        *    *  *        *               *",
    "*           *  *   *  *         *        *       *      *    *            *",
    "*            *       *        * * *      *       *       * * *            *",
    "*                                                                         *",
    "*                                                                         *",
    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
]
# ==== Game Play Message Strings ====
# Menu start options lising all available games for play
SIMPLE_GAMES_START = "Welcome to Simple Games.\n\n1. Tic Tac Toe\n2. Connect 4\n3. Solitaire"

# Introduction and basic game flow for Tic Tac Toe
INTRO_TICTACTOE = """
This is an online version of the classic game. Play multiple games per session
against an opponent or the computer. X starts the game.
"""
# Introduction and basic game flow for Connect 4
INTRO_CONNECT4 = """
This is an online version of the classic game. Play a single game
against an opponent or the computer. Red starts the game.
"""
# Introduction and basic game flow for Solitaire
INTRO_SOLITAIRE = """
THIS GAME IS STILL IN DEVELOPMENT. YOU MAY ENCOUNTER BUGS OR ERRORS WHILE PLAYING.\n
This is an online version of the classic game Klondike Solitaire. Play a single game. 
You can play single draw or three draw solitaire.
"""
# Message for simulating computer thinking of move selection
THINKING = "\nComputer is now thinking."

# ==== Tic Tac Toe Borderline String ====
# Horizontal border line for the Tic Tac Toe board display.
BOARDLINE_TICTACTOE = "* " * 18 + "*"  # for Tic Tac Toe

# ==== Connect 4 Borderline and Board Label Strings ====
# Horizontal separator lines for the Connect 4 board display.
BOARDLINE_CONNECT4 = ("-" * 12 + "+") * 6 + "-" * 12
BOARDLINE_CONNECT4_THIN = (
    " -" * 5 +
    " - +") * 5 + " - " * 6 + "-"  # for Connect 4 alternative version

# List of single-digit column names for Connect 4.
column_names = ["1", "2", "3", "4", "5", "6", "7"]
# List of full word column names for Connect 4.
column_names_full_word = [
    "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"
]

board_length = len(
    BOARDLINE_CONNECT4
)  # This constant stores the calculated length of BOARDLINE_CONNECT4 for seven column game configs.
#
#  Formatted string for Connect 4 column headers (1-7), aligned to the board length.
COL_NAMES_CONNECT4 = " ".join(f"{w:^12}"
                              for w in column_names).ljust(board_length)

# ==== Dictionary of Game Strings or Game Bundles   ====
# A collection of strings specific to the Tic Tac Toe game.
tictactoe_strings = {
    "welcome": WELCOME_TICTACTOE,
    "intro": INTRO_TICTACTOE,
    "boardline": BOARDLINE_TICTACTOE
}
# A collection of strings specific to the Connect 4 game.
connect4_strings = {
    "welcome": WELCOME_CONNECT4,
    "intro": INTRO_CONNECT4,
    "boardline": BOARDLINE_CONNECT4,
    "boardlabels": COL_NAMES_CONNECT4
}
# A collection of strings specific to the Solitaire game.
solitaire_strings = {
    "welcome": WELCOME_SOLITAIRE,
    "intro": INTRO_SOLITAIRE,
}

# A collection of general utility strings used across multiple games or scenarios.
other_strings = {
    "gameover": GAMEOVER,
    "thinking": THINKING,
    "x": XWINS,
    "o": OWINS,
    "r": REDWINS,
    "y": YELLOWWINS
}

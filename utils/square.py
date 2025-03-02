from enum import Enum
from colorama import Fore, Style

class Square(Enum):
    """Represents a single square as ASCII String."""
    BLANK = ["            "] * 5
    
    R = [
        Fore.RED + "    ****    " + Style.RESET_ALL, 
        Fore.RED + "  ********  " + Style.RESET_ALL, 
        Fore.RED + " ********** " + Style.RESET_ALL, 
        Fore.RED + "  ********  " + Style.RESET_ALL,
        Fore.RED + "    ****    " + Style.RESET_ALL
    ]
    
    Y = [
    Fore.LIGHTYELLOW_EX + "    ****    " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + "  ********  " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + " ********** " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + "  ********  " + Style.RESET_ALL,
    Fore.LIGHTYELLOW_EX + "    ****    " + Style.RESET_ALL
   ]
    
    B = [
    Fore.BLUE + "    ****    " + Style.RESET_ALL, 
    Fore.BLUE + "  ********  " + Style.RESET_ALL, 
    Fore.BLUE + " ********** " + Style.RESET_ALL, 
    Fore.BLUE + "  ********  " + Style.RESET_ALL,
    Fore.BLUE + "    ****    " + Style.RESET_ALL
   ]

    O = [
        "    *  *    ", "  *      *  ", " *        * ", "  *      *  ", "    *  *    "
    ]
    X = [
        "  *       * ", "    *   *   ", "      *     ", "    *   *   ", "  *       * "
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

GAMEOVER = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *               * * *        **        *       *    * * * *               *
   *              *            *  *       * *   * *    *                     *
   *              *   * *     *    *      *   *   *    * * *                 * 
   *              *     *    *      *     *       *    *                     *
   *               * * *    *        *    *       *    * * * *               *
   *                                                                         *
   *                                                                         *
   *                *  *     *       *    * * * *     *  *  *                *
   *              *      *    *     *     *           *      *               *
   *              *      *     *   *      * * *       *  *  *                *
   *              *      *      * *       *           *      *               *
   *                *  *         *        * * * *     *       *              *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

INTRO = """
This is an online version of the classic game. Play multiple games per session
against and opponent or the computer. X starts the game.
"""
THINKING = "\nComputer is now thinking."
DRAW = "\nCATS GAME.\n There was no winner so there will be no chicken dinner.\n"

# horizontal_line = "* " * 18 + "*" # for Tic Tac Toe
horizontal_line = "* " * 44 + "*" # for Tic Tac Toe

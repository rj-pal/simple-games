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

REDWINS = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *             *  *  *            *  *  *         *  * *                   *
   *             *      *           *               *      *                 *
   *             *  *  *            * * *           *       *                *
   *             *      *           *               *      *                 *
   *             *       *          *  *  *         *  * *                   *
   *                                                                         *
   *            *             *     * * *     *       *       * * *          *
   *            *             *       *       *  *    *      *     *         *
   *             *     *     *        *       *    *  *        *             *
   *              *  *   *  *         *       *       *      *    *          *
   *               *       *        * * *     *       *       * * *          *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

INTRO_TICTACTOE = """
This is an online version of the classic game. Play multiple games per session
against and opponent or the computer. X starts the game.
"""

INTRO_CONNECT4 = """
This is an online version of the classic game. Play multiple games per session
against and opponent or the computer. Red starts the game.
"""

THINKING = "\nComputer is now thinking."

BOARDLINE_TICTACTOE = "* " * 18 + "*" # for Tic Tac Toe

BOARDLINE_CONNECT4 = ("-" * 12 + "+") * 6 + "-" * 12   #(" -" * 5 + " - +") * 5 + " - " * 6 + "-" # for Connect 4

SIMPLE_GAMES_START = "Welcome to Simple Games.\n\n1. Tic Tac Toe\n2. Connect 4\n3. Solitaire"

tictactoe_strings = {
    "welcome": WELCOME_TICTACTOE,
    "intro": INTRO_TICTACTOE,
    "boardline": BOARDLINE_TICTACTOE
}

connect4_strings = {
    "welcome": WELCOME_CONNECT4,
    "intro": INTRO_CONNECT4,
    "boardline": BOARDLINE_CONNECT4
}

other_strings = {
    "gameover": GAMEOVER,
    "thinking": THINKING,
    "redwinner": REDWINS
}
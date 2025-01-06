# Tic Tac Toe
Tic-Tac-Toe Game for Command Line written in Python (requires Python 3.9 or higher)
***
This is simple Tic-Tac-Toe game with original algorithms for game play including keeping track of squares and checking for winner all created by me 🔥

It also includes simple 'AI' capabilities so that a single player can also play against the computer. There are three modes: easy, intermediate and hard. In easy mode, the computer will play a blind strategy by selecting each move randomly. Intermediate mode runs a random play and block strategy. Hard mode runs a strategy that will guarantee that the computer never looses🏆  

The best you can hope for is a draw 😁

All ascii art and game board are also original work by me ❤️

### AI Test Notebook

I performed some test of the 'AI' where the computer would play in hard mode against itself in easy, intermediate and hard mode. As expected, the computer in hard mode never lost against itself! When the computer played against itself in hard mode, there were only draws and no wins! This was crucial to validate my hard mode logic.

I wrote a TestAI class to perform the tests which modified the code to allow the game to create two computer players. It validated that the computer mode worked properly and that there was a clear difference in the outcomes of the three different modes of play.

### Some Info on the Code Itself

The impetus for this command line project was for learning more deeply about lists and list manipulation, like using list combining and unpacking using methods like zip. All the printing for the game board and pieces, as well as keeping track of moves and checking for wins are based upon lists.

The idea for the game board squares was to have a generic list for ex, oh, blank and  a vertical line where the board is printed in tuples made from 
the generic lists one row and one line at a time. The general format for a row is square, line, sqaure, line, square. A 2D array is used to keep track 
of what type of square should be printed (ex, oh or blank). Each row is stored in a list and the zip function is used to produce each row. 

'AI' capabilities were added after the functionality of the game play was confirmed. The 'hard' mode logic is coded using only basic boolean logic and was extracted from a close examination of tic tac toe through individual play against myself.

### License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

***

Hope you enjoy my version of a classic game!

If you like it, give my repo a 🌟

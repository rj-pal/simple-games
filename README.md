# Tic Tac Toe
Tic-Tac-Toe Game for Command Line written in Python

* Updated with refactoring and computer player capabilities.

This is simple Tic-Tac-Toe game with algorithms for game play, keeping track of squares, and checking for winner all created by me. The ascii art 
and game board are also original work by me. 

The basis for printing the game board and keeping track of everything is all based upon lists. The reason was to practice building, combining and 
unpacking lists by using list methods like zip and 2D lists. 

The idea for the game board squares was to have a generic list for ex, oh, blank and  a vertical line where the board is printed in tuples made from 
the generic lists one row and one line at a time. The general format for a row is square, line, sqaure, line, square. The 2D array is used to keep track 
of what type of square should be printed (ex, oh or blank). Each row is stored in a list and the zip function is used to produce each row.

The idea for keeping track of the plays made by players and checking a winner uses lists. As stated above, the status of a sqaure is kept in a 2D list 
that is updated everytime a player makes a move. To check for a winner, the 2D array is examined and lists for the columns and diagonals are created 
(the rows are already in the array) by looping through the list of lists and generating line lists for checking each time a player makes a move (starting 
after the 5th move). Each line (row, column or diagnoal list) is checked for a count of 3, and ex and oh are checked with the integer 1 for ex and 2 for oh
(0 is for blank). The game ends when a winner is found, but the main method for running games allows for two players to play again and the program keeps 
track of the wins and loses until the games are terminated. The players also are able to enter their names or an empty entry gets assigned a default name.

Hope you enjoy my version of a classic game!

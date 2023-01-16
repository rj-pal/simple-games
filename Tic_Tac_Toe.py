# Each row is printed one at at a time by zippping 5 lists: 3 squares and 2 vertical lines
# Each row is labelled postions and will be updated using the update 
# Each sqaure is 12 spaces wide and 8 spaces long
# Default square is blank and can be updated to an ex or oh depending on the move

BOLD = '\033[1m'
BOLD_START = '\033[1m'
BOLD_END = '\033[0m'

vertical = ["*", "*", "*", "*", "*", "*", "*", "*", "*"]
blank = ["              ", "              ", "              ", "              ", "              ", "              ", "              ", "              ",  "              "]
oh = ["              ", "              ", "     ****     ", "   *      *   ", "   *      *   ", "   *      *   ", "     ****     ", "              ", "              ",]
ex = ["              ", "              ", "   *       *  ", "     *   *    ", "       *      ", "     *   *    ", "   *       *  ", "              ", "              "]
line = "* * * * * * * * * * * * * * * * * * * * * * * * *"

a = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
b = "*                                                                         *"
c = "*                                                                         *"
d = "*     *       *   * * *   *       * * *    *  *      *   *     * * *      *"
e = "*      *  *  *    * *     *      *        *    *    *  *  *    * *        *"
f = "*       *   *     * * *   * * *   * * *    *  *    *       *   * * *      *"
g = "*                                                                         *"
h = "*                                                                         *"
i = "*      * * *   *  *                                                       *"
j = "*        *    *    *                                                      *"
k = "*        *     *  *                                                       *"
l = "*                                                                         *"
m = "*                                                                         *"
n = "*      * * *   *    * *     * * *    *     * *     * * *   * *   * * *    *"
o = "*        *     *   *          *     * *   *          *    *   *  * *      *" 
p = "*        *     *    * *       *    *   *   * *       *     * *   * * *    *"
q = "*                                                                         *"
r = "*                                                                         *"
s = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

welcome = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s]

    
class Board:
    
    def __init__(self):
        
        self.top_positions = [blank, vertical, blank, vertical, blank]
        self.middle_positions = [blank, vertical, blank, vertical, blank]
        self.bottom_positions = [blank, vertical, blank, vertical, blank]
        
        self.positions = [self.top_positions, self.middle_positions, self.bottom_positions]
        
    def update_row(self, row: int, column: int, marker: int) -> None:
        '''Updates the square on the board to Ex, Oh, or Blank. Returns None.'''
        
        square_value = blank
        if marker == 1:
            square_value = ex
        elif marker == 2:
            square_value = oh
        
        # multiply the column index by 2 because a column occupies every even position in a position list (odd indexes are the vertical lines)
        column = column * 2
        
        if row == 0:
            self.top_positions[column] = square_value
        elif row == 1: 
            self.middle_positions[column] = square_value
        else:
            self.bottom_positions[column] = square_value
        
    
    def print_line(self, positions: list) -> None:
        '''Prints a row of the board from a list of the current position. Returns None.'''
        squares = list(zip(*positions))
        for square in squares:
            print(BOLD_START + square[0] + BOLD_END, square[1], BOLD_START + square[2] + BOLD_END, square[3], BOLD_START + square[4] + BOLD_END)        
#             Non-bolded Ex and Ohs
#             print(square[0], square[1], square[2], square[3], square[4])        
    
    def print_board(self) -> None:
        '''Prints the board row by row by from the positions list of current positions for each row. Returns None.'''
        for index, position in enumerate(self.positions):
            self.print_line(position)
            
            # for printing the horiztonal lines on the board
            if index != 2:
                print(line)
                
    def reset_board(self) -> None:
        '''Sets each square in the board to a blank. Returns None.'''
        for i in range(3):
            for j in range(3):
                self.update_row(i, j, 0)

# Alternative algorithm for resetting the board                
#         for row in self.positions:
#             for i in range(0, 5, 2):
#                 row[i] = blank
                
    
# 0 is empty, 1 is ex, and 2 is oh

class Player:
    
    # marker must be 1 or 2 for tic-tac-toe game
    def __init__(self, name: str, marker: int):
        self.name = name
        self.marker = marker
        self.win_count = 0
        self.games_played = 0
        
    def get_marker_type(self) -> str:
        if self.marker == 1:
            return "'X'"
        elif self.marker == 2:
            return "'O'"
        else:
            return "Unknown marker for tic-tac-toe"
        
    @classmethod
    def construct_player(cls, name: str, marker: int):
        
        if type(name) is not str:
            print("Error")
            return
        
        if type(marker) is not int:
            print("Error")
            return
        
        if not name:
            name = 'Anonymous' + str(marker)
        
        return Player(name, marker)
    
class Game:
    
    def __init__(self):
        self.is_over = False
        self.squares = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_1 = None
        self.player_2 = None
#         self.game_board = Board()

    
    def is_free(self, row, column) -> bool:
        '''Checks if a sqaure on the board is free or occupied. Returns boolean.'''
        return self.squares[row][column] == 0


    def reset_squares(self) -> None:
        '''Sets all the values in the board tracker to blank or zero. Returns None.'''
        for row in range(3):
            for square in range(3):
                self.squares[row][square] = 0

    def update_player(self, marker) -> None:
        '''Updates the game statistics on the two players. Returns None.'''
        self.player_1.games_played += 1
        self.player_2.games_played += 1
        if marker == 1:
            self.player_1.win_count += 1
        else:
            self.player_2.win_count += 1
            
    def player_scoreboard(self) -> None:
        '''Shows the player statisics for the game. Returns None.'''
        print(f"{self.player_1.name}\nWin: {self.player_1.win_count}, Loss: {self.player_1.games_played - self.player_1.win_count}")
        print(f"{self.player_2.name}\nWin: {self.player_2.win_count}, Loss: {self.player_2.games_played - self.player_2.win_count}\n")

        
    def update_square(self, row: int, column: int, marker: int) -> None:
        '''Updates the board tracker to Ex, Oh, or Blank. Returns None.'''
        self.squares[row][column] = marker
        
    def check_line(self, line, ex_or_oh) -> bool:
        '''Checks if a row has all the same markers to see if the game has been won. Returns boolean.'''
        # takes the 3-element array and counts the marker number - a count of 3 means there is a winner
        return line.count(ex_or_oh) == 3
        
    def check_for_winner(self) -> bool:
        '''Checks if the game has been won in a row, column or diagonal. Returns boolean.'''
        
        # these lists represent the columns or vertical lines and the two diagonal lines on the board
        # elements will be added to them as the function iterates through each row in the 2D array 
        down_one = []
        down_two = []
        down_three = []
        diagonal_right = []
        diagonal_left = []
        
        # added to a list for easy iteration when checking each line for a winner
        line_checker = [down_one, down_two, down_three, diagonal_right, diagonal_left]
        
        # Strings for winner printing
        ex_winner = f"{self.player_1.name} is the winner.\n{self.player_1.get_marker_type()} wins in"
        oh_winner = f"{self.player_2.name} is the winner.\n{self.player_2.get_marker_type()} wins in"
            
        # row is the index in a 2D array that represents the horizontal lines on the board - each row as an array
        # check the row for a winner first - if no winner, add each sqaure in the row to the other lines' (vertical and diagonal) arrays
        for row, line in enumerate(self.squares):
                 
            if self.check_line(line, 1):
                print(ex_winner, "row", str(row + 1) + ".")
                self.update_player(1)
                return True
            elif self.check_line(line, 2):
                print(oh_winner, "row", str(row + 1) + ".")
                self.update_player(2)
                return True
            
            # column is the index in a 2D array that represents the vertical lines on the board - each column as an array
            # each square is added to a line array based on the corresponding column index - for both vertical and diagonal lines
            # both the row and column indexes are needed to add the appropriate square to the diagonal lines
            for column, square in enumerate(line):
                if column == 0:
                    down_one.append(square)
                    if row == 0:
                        diagonal_right.append(square)
                    elif row == 2:
                        diagonal_left.append(square)
                elif column == 1:
                    down_two.append(square)
                    if row == 1:
                        diagonal_right.append(square)
                        diagonal_left.append(square)
                else:
                    down_three.append(square)
                    if row == 0:
                        diagonal_left.append(square)
                    elif row == 2:
                        diagonal_right.append(square)
        # this final loop checks each vertical and horizontal line on the board for a winner        
        for location, line in enumerate(line_checker):
            # generate some add ons to the winner strings depending on the location in the line checker list
            # the structure of the list: columns 1 to 3, followed by diagonal in the right direction and diagonal in the left direction
            if location < 3:
                winning_line = f"column {location + 1}"
            elif location == 3:
                winning_line = f"in the right diagonal"
            else:
                winning_line = f"in the left diagonal"
            
            if self.check_line(line, 1):
                print("Winner winner chicken dinner")
                print(ex_winner, winning_line + ".")
                self.update_player(1)
                return True
            elif self.check_line(line, 2):
                print("Winner winner chicken dinner")
                print(oh_winner, winning_line + ".")
                self.update_player(2)
                return True  

        return False

        
    def take_turn(self, player) -> tuple([int, int, int]):
        '''Gets the row and column from the current player and updates the board tracker, and returns the indexed row and colmn and marker for the board class. Returns tuple of integers.'''
        row, column = self.enter_square()
        ex_or_oh = player.marker
        
        self.update_square(row, column, ex_or_oh)

        # TO INCLUDE IF GAME CLASS accepts BOARD CLASS Object       
#         self.game_board.update_row(row, column, ex_or_oh)      
#         self.game_board.print_board()

        return row, column, ex_or_oh


    def enter_square(self) -> tuple([int, int]):
        '''Validates and formats the user inputted row and column to update the square position to Ex or Oh and checks if the inputted position is occupied. Return tuple of integers.'''
        valid_input = {1, 2, 3}
        while True:  
            try:
                row = int(input("Enter the row: "))
                
                if row not in valid_input:
                    print("\nYou must enter 1, 2, or 3 only for the row. Try to selet a square again.\n")
                    continue
      
            except ValueError:
                print("\nYou must enter a number. Start again.\n")
                continue
            
            
            try:
                column = int(input("Enter the column: "))
                
                if column not in valid_input:
                    print("\nYou must enter 1, 2, or 3 only for the column. Try to selet a square again.\n")
                    continue
            except ValueError:
                print("\nYou must enter a number. Start again.\n")
                continue
                
            
            # Subtract 1 from each for list indexing in other methods as user input is from 1 to 3
            row = row - 1
            column = column - 1

            if self.is_free(row, column):
                break
            else:
                print("\nThe square is already occupied. Select another square.\n")

        return row, column
    
    def create_players(self) -> tuple([Player(str, int), Player(str, int)]):
        '''Creates two players of the Player class for game play. Returns a tuple of two Players.'''
        
        name = input("Enter the name of player one: ")
        
        # Player one is Ex by default
        player_1 = Player.construct_player(name, 1)
        
        name = input("Enter the name of player two: ")
        
        # Player two is Oh by default
        player_2 = Player.construct_player(name, 2)
        
        return player_1, player_2
    
    
    def start_game(self) -> None:
        '''Starts the game and creates two players from user input. Returns None.'''
        self.welcome_box()   
        self.player_1, self.player_2 = self.create_players()
    
    
    def play_game(self) -> None:
        '''Main method for playing the game that terminates after all nine sqaures have been filled or a winner has been delcared. Returns None.'''
        
        for i in range(9):
            if i % 2 == 0:
                print(f"\nIt is {self.player_1.name}'s turn.\n")
                row, column, marker = g.take_turn(self.player_1)
                last_played = f"\n{self.player_1.name} played the square in row {row + 1} and column {column + 1}."
            else:
                print(f"\nIt is {self.player_2.name}'s turn.\n")
                row, column, marker = g.take_turn(self.player_2)
                last_played = f"\n{self.player_2.name} played the square in row {row + 1} and column {column + 1}."


            b.update_row(row, column, marker)
            b.print_board()
            
            # will start checiking for winner after the fourth turn 
            if i > 3 and g.check_for_winner():
                print("GAME OVER\n")
                break
            elif i == 8:
                print("CATS GAME. There was no winner so there will be no chicken dinner.\n")
                break

            print(last_played, "Who's Next?")    
        
            
    def welcome_box(self) -> None:
        '''Prints the "Welcome to Tic Tac Toe" box'''
        print()
        for line in welcome:
            print(line)
        print()
            
            
if __name__ == '__main__':
    b = Board()
    g = Game()
    g.start_game()
    g.play_game()
    message = "\nYou must enter 'Yes' or 'No' only.\n"
    while True:
        try:
            play_again = input("Would you like to play again? Enter yes or no: ").lower()
            print()
            if play_again == 'yes' or play_again == 'y':
                g.reset_squares()
                b.reset_board()
                g.player_scoreboard()
                g.play_game()
            elif play_again == 'no' or play_again == 'n':
                print("Thanks for playing tic-tac-toe. See you again soon.")
                break
            else:
                print(message)

        except ValueError:
            print(message)
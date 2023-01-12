# Each row is printed one at at a time by zippping 5 lists: 3 squares and 2 vertical lines
# Each row is labelled postions and will be updated using the update 
# Each sqaure is 12 spaces wide and 8 spaces long
# Default square is blank and can be updated to an ex or oh depending on the move

BOLD_START = '\033[1m'
BOLD_END = '\033[0m'
END = '\033[0m'
CYAN = '\033[96m'
vertical = ["*", "*", "*", "*", "*", "*", "*", "*"]

# vertical = ["*", "*", "*", "*", "*", "*", "*", "*"]
blank = ["            ", "            ", "            ", "            ", "            ", "            ", "            ",  "            "]
oh = ["            ", CYAN + "    ****    " + END, CYAN + "  *      *  " + END, CYAN + "  *      *  " + END, CYAN + "  *      *  " + END, CYAN + "    ****    " + END, "            "]
ex = ["            ", "  *       * ", "    *   *   ", "      *     ", "    *   *   ", "  *       * ", "            "]
line = "* * * * * * * * * * * * * * * * * * * * * *"

    
class Board:
    
    def __init__(self):
        
        self.top_positions = [blank, vertical, blank, vertical, blank]
        self.middle_positions = [blank, vertical, blank, vertical, blank]
        self.bottom_positions = [blank, vertical, blank, vertical, blank]
        
        self.positions = [self.top_positions, self.middle_positions, self.bottom_positions]
        
    def update_row(self, row: int, column: int, marker: int) -> None:
        
        square_value = oh
        if marker == 1:
            square_value = ex
        elif marker == 0:
            square_value = blank
            
        column = column * 2
        
        if row == 0:
            self.top_positions[column] = square_value
        elif row == 1: 
            self.middle_positions[column] = square_value
        else:
            self.bottom_positions[column] = square_value
        
    
    def print_line(self, positions):
        squares = list(zip(*positions))
        for square in squares:
            print(BOLD_START + square[0] + BOLD_END, square[1], BOLD_START + square[2] + BOLD_END, square[3], BOLD_START + square[4] + BOLD_END)        
    
    def print_board(self):
        for index, position in enumerate(self.positions):
            self.print_line(position)
            if index != 2:
                print(line)
                
    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.update_row(i, j, 0)
#         for row in self.positions:
#             for i in range(0, 5, 2):
#                 row[i] = blank
                
    
# 0 is empty, 1 is ex, and 2 is oh
default_squares = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# default_squares = [[1, 1, 1], [2, 0, 1], [0, 0, 0]]

class Player:
    
    # marker must be 1 or 2
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker
        self.win_count = 0
        
    def get_marker_type(self):
        if self.marker == 1:
            return "'X'"
        elif self.marker == 2:
            return "'O'"
        else:
            return "Unknown maker for tic-tac-toe"
        
    @classmethod
    def construct_player(cls, name, marker):
        
        if type(name) is not str:
            print("Error")
            return
        
        if type(marker) is not int:
            print("Error")
            return
        
        return Player(name, marker)
    
class Game:
    
    def __init__(self):
        self.is_over = False
        self.squares = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_1 = None
        self.player_2 = None
#         self.game_board = Board()

    
    def is_free(self, row, column):

        return self.squares[row][column] == 0


    def reset_squares(self) -> None:
        print("Called")
        print(default_squares)
        self.squares = default_squares
        print(self.squares)

        
    def update_square(self, row: int, column: int, marker: int) -> None:   
        self.squares[row][column] = marker
        
    def check_line(self, line, ex_or_oh):
        return line.count(ex_or_oh) == 3
        
    def check_for_winner(self):
        
        down_one = list()
        down_two = list()
        down_three = list()
        diagonal_right = list()
        diagonal_left = list()
        
        line_checker = [down_one, down_two, down_three, diagonal_right, diagonal_left]
        
        for row, line in enumerate(self.squares):
            
            # String for winner printing
            ex_winner = f"{self.player_1.name} is the winner.\n{self.player_1.get_marker_type()} wins in"
            oh_winner = f"{self.player_2.name} is the winner.\n{self.player_2.get_marker_type()} wins in"
            
            if self.check_line(line, 1):
                print(ex_winner,"row", row + 1)
                return True
            elif self.check_line(line, 2):
                print(oh_winner,"row", row + 1)
                return True
            
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
                        
            for location, line in enumerate(line_checker):
                if location < 3:
                    winning_line = f"column {location + 1}"
                elif location == 3:
                    winning_line = f"in the right diagonal"
                else:
                    winning_line = f"in the left diagonal"
                    
                if self.check_line(line, 1):
                    print("Winner winner chicken dinner")
                    print(ex_winner, winning_line)
                    return True
                elif self.check_line(line, 2):
                    print("Winner winner chicken dinner")
                    print(oh_winner, winning_line)
                    return True
                
                        
            
          
        ### Counts the columns TOO EARLY -> doesn't work using sets here
        
#         if len(down_one) == 1:
#             print("Winner in column 1 ")
#             return True
        
#         elif len(down_two) == 1:
#             print("Winner in column 2 ")
#             return True
        
#         elif len(down_three) == 1:
#             print("Winner in column 3 ")
#             return True
        
#         else:
#             return False    

        
    def take_turn(self, player) -> tuple:  
        row, column = self.enter_square()
        ex_or_oh = player.marker
        
        self.update_square(row, column, ex_or_oh)

        # TO INCLUDE IF GAME CLASS accepts BOARD CLASS Object
        
#         self.game_board.update_row(row, column, ex_or_oh)
        
#         self.game_board.print_board()

        # OLD TESTING CODE HERE

#         marker = 1
#         if player == oh:
#             marker = 2
#             update_square(row, column, marker)
#         else:
#             update_square(row, column, marker)

        return row, column, ex_or_oh


    def enter_square(self) -> tuple:   
        while True:  
            valid_input = {1, 2, 3}
            row = int(input("Enter the row: "))
            if row not in valid_input:
                print("You must enter 1, 2, or 3 only for the row. Start again.")
                continue
            
            column = int(input("Enter the column: "))
            if column not in valid_input:
                print("You must enter 1, 2, or 3 only for the column. Start again")
                continue

            row = row - 1
            column = column - 1

            if self.is_free(row, column):
                break
            else:
                print("The square is already occupied. Start again")

        return row, column
    
    def create_players(self):
        name = input("Enter the name of player one: ")
        # Player one is Ex by default
        player_1 = Player.construct_player(name, 1)
        
        # Player two is Oh by default
        name = input("Enter the name of player two: ")
        player_2 = Player.construct_player(name, 2)
        
        return player_1, player_2
    
    def play_game(self):
        
        self.player_1, self.player_2 = self.create_players()
        
        for i in range(9):
            if i % 2 == 0:
                row, column, marker = g.take_turn(self.player_1)
            else:
                row, column, marker = g.take_turn(self.player_2)

            b.update_row(row, column, marker)
            b.print_board()

            if i > 3 and g.check_for_winner():
                print("GAME OVER")
                break

            print("Who's Next?")
            
            
b = Board()
b.reset_board()
g = Game()
g.play_game()
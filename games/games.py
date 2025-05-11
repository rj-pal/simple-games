from collections import Counter
from random import choice, randint
from typing import Tuple, List, Union, Optional
from copy import deepcopy
from core.board import Board, LineChecker
from core.deck import CardDeck, CardStack, CardQueue
from core.player import Player
from time import sleep

def int_converter(number, columns):
    return divmod(number, columns)

def pair_converter(pair, columns):
    return pair[0]*columns + pair[1]

def board(rows: int, columns: int):
    board = []
    for i in range(rows):
        if i == 1:
            board.append(["x" for _ in range(columns)])
        else:
            board.append([0 for _ in range(columns)])
    return board

class Solitare:

    def __init__(self, size: int=7):
        self._size = size
        self._klondike_value = 3
        self.card_deck = CardDeck() # Used for dealing initial cards and as the waste pile
        self.tableau = self.make_tableau()
        self.foundation_piles = self.make_foundation_piles()
        self.draw_pile = self.make_draw_pile()
        self.waste_pile = self.card_deck.get_empty_card_stack()

    @property
    def size(self):
        return self._size
    
    @property
    def klondike_value(self):
        """Klondike value to determine if the draw is 1 or 3."""
        return self._klondike_value

    @klondike_value.setter
    def klondike_value(self, value):
        if value not in {1, 3}:
            raise ValueError("klondike_value must be either 1 or 3")
        self._klondike_value = value

    ### IS IT NECESSARY?
    @klondike_value.deleter
    def klondike_value(self):
        raise AttributeError("Cannot delete the klondike_value attribute")
    
    def check_move(self, from_card, to_card):
        # check King move to empty stack
        if from_card.value == 13 and to_card is None:
            return True
        # check all other possible moves
        return (to_card.is_black != from_card.is_black) and (to_card.value == from_card.value + 1)
    
    def check_win(self):
        return all(pile.size == 13 for pile in self.foundation_piles.values())
    
    def push_card_back_to_stock_pile(self):
        if self.card_deck.size != 0:
            self.draw_pile.push(self.card_deck.deck.pop()) 

    def draw(self, klondike_value=1):
        """Draw a card from the stock pile and flip it over for move."""

        # No drawing from empty stock pile in main move.
        if self.draw_pile.is_empty():
            print("Invalid move. Cannot draw from an empty stock pile.")
            print(input("Press ENTER or RETURN."))
            return False
        
        for _ in range(self._klondike_value):
            # flip card will return False if the second or third flip is from emtpy stock pile
            if self.flip_card_draw_pile():
                self.waste_pile.push(self.draw_pile.pop())
            else:
                break
        
        return True
       
        # # When top card is face up, a draw will add it to the waste pile, or back to the initial card deck
        # if self.draw_pile.peek().visible:
        #     self.card_deck.add_card(self.draw_pile.pop())
        # # Flip over the top card from teh stock pile
        # self.flip_card_draw_pile()
        # print(self.draw_pile.peek())
        # print(self.draw_pile)
        # return True

    
    def move_to_foundation(self, stack_number: int=-1, from_tableu: bool=False):
        """Move a card from the waste pile or tableau to the foundation pile of the selected card's suit. Defaults to move from waste pile."""

        def check_foundation_move(from_pile):
            """Validates and moves card from stock pile or tabelau stack to the appropriate foundation pile."""
            # Get the foundation pile that corresponds to the suit of the card
            card = from_pile.peek()
            foundation_pile = self.foundation_piles[card.suit]
            print("HERE")
            print(card)
            if foundation_pile.is_empty():
                if card.value == 1:
                    foundation_pile.push(from_pile.pop())
                    return True
            elif card.value == foundation_pile.peek().value + 1:
                foundation_pile.push(from_pile.pop())
                return True      
            return False
        
        # check for empty waste pile/tableau stack or validate and make move
        if from_tableu:
            if self.tableau[stack_number].is_empty():
                print("Invalid move. Cannot move from an empty tableau stack.")
                return False  
            if check_foundation_move(from_pile=self.tableau[stack_number]):
                if not self.tableau[stack_number].is_empty():
                    self.flip_card_tableau(stack_number)
                return True      
        else:
            if self.waste_pile.is_empty():
                print("Invalid move. Cannot move from an empty stock pile.")
                return False 
            return check_foundation_move(from_pile=self.waste_pile)
        return False
            ### ADD ERROR HANDLING MAYBE???
            # tableau_stack = self.get_tableau()[stack_number]
            

            #     if not tableau_stack.is_empty():
            #         self.flip_card_tableau(stack_number)
            #     return True
            # else:
            #     return False


    def build(self, position):
        # No building from a waste pile that has not been drawn from or is empty
        if not self.waste_pile.peek().visible:
            return False
        # Get the stack you want to build to and validate it
        if 0 <= position < self.size:
            # card_stack = self.get_tableau()[position]
            # Set an empty stack to None to allow for moving a King to the tableau stack
            if self.tableau[position].is_empty():
                table_card = None
            else:
                table_card = self.tableau[position].peek()
            waste_card = self.waste_pile.peek()
            # Validate move
            if self.check_move(from_card=waste_card, to_card=table_card):
                # Move card from stock to tableau and top card from the waste pile to the stock pile
                self.tableau[position].push(self.waste_pile.pop())
                # self.push_card_back_to_stock_pile()
                return True
        return False
    
    def transfer(self, from_position, to_position, number_of_cards=1):
        if 0 <= from_position < self.size and 0 <= to_position < self.size:
            from_card_stack = self.tableau[from_position]

            if from_card_stack.size < number_of_cards:
                print(f"Invalid move. There are not enough cards in this stack to transfer {number_of_cards} cards.")
                print(input("ENTER TO CONTINUE"))
                return False
            
            temp_card = from_card_stack.head.next

            for _ in range(number_of_cards - 1):
                if temp_card.next.value.visible:
                    temp_card = temp_card.next
                else:
                    print(f"Invalid move. There are not enough cards face up cards in this stack to transfer {number_of_cards} cards.")
                    print(input("ENTER TO CONTINUE"))
                    return False
                
            print(temp_card.value)
            print(input("ENTER TO CONTINUE"))
            to_card_stack = self.tableau[to_position]
            
            if to_card_stack.is_empty():
                to_card = None
            else:
                to_card = to_card_stack.peek()
            
            from_card = temp_card.value
            
            if self.check_move(from_card, to_card):
                temp_stack = CardStack()
                for _ in range(number_of_cards):
                    temp_stack.push(from_card_stack.pop())
                while not temp_stack.is_empty():
                    to_card_stack.push(temp_stack.pop())
                if not from_card_stack.is_empty() and not from_card_stack.head.next.value.visible:
                    from_card_stack.head.next.value.flip_card()
                return True
            else:
                return False

    
    def make_tableau(self):
        tableau = []
        self.card_deck.shuffle_deck()
        for i in range(self.size):
            card_stack = self.card_deck.deal_cards(i + 1)
            card_stack.head.next.value.flip_card()
            tableau.append(card_stack)
            self.card_deck.shuffle_deck()  
        return tableau

    def make_foundation_piles(self):
        SUITS = ("S", "H", "D", "C")
        foundation_piles = {}
        for suit in SUITS:
            card_stack = self.card_deck.get_empty_card_stack()
            card_stack.suit = suit
            foundation_piles[suit] = card_stack
        return foundation_piles
       

    def make_draw_pile(self):
        draw_pile = self.card_deck.pile()
        return draw_pile
    

    def get_deck(self):
        return self.card_deck
        
    def get_tableau(self):
        return self.tableau
       
    def get_tableau_for_print(self):
        
        return [card_stack.to_list()[::-1] for card_stack in self.tableau]
        
    def get_foundation_piles(self):
       
        return self.foundation_piles
    
    def check_stock_pile(self):
        return self.draw_pile.is_empty()
    
    def get_stock_pile(self):
        return self.draw_pile
    
    def get_waste_pile(self):
        return self.waste_pile
    
    def show_tableau(self):
        for card_stack in self.tableau:
            print(card_stack)

    def show_foundation_piles(self):
        for card_stack in self.get_foundation_piles():
            print(card_stack)

    def show_stock_pile(self):
        print(self.get_stock_pile())

    def show_waste_pile(self):
        waste_pile = []
        temp_card = self.get_waste_pile().head.next
        for _ in range(self._klondike_value):
            if temp_card is not None:
                waste_pile.append(temp_card.value)
            else:
                break
            
            temp_card = temp_card.next
        return waste_pile[::-1]
        

        # while display_number > 0:
        #     if pile.is_empty():
        #         break
        #     else:
        #         print(temp_card.value)
        #         temp_card = temp_card.next
        #         display_number -= 1

    def flip_card_draw_pile(self):
        if self.draw_pile.is_empty():
            return False
        self.draw_pile.head.next.value.flip_card()
        return True

    def flip_card_tableau(self, stack_number):
        if self.tableau[stack_number].is_empty():
            return False
        self.tableau[stack_number].head.next.value.flip_card()
        return True

class ConnectFour:

    def __init__(self, connect_value: int=4, rows: int=6, columns: int=7):
         self.connect_value = connect_value
         self.rows = rows
         self.columns = columns
         self.board: List[List] = self.create_board()
         self.move_list: List = []
         self.height_list: List = [self.rows] * self.columns
         self.size_list: List = [0] * self.rows
         self.round_count: int = 0
         self.go_first: bool = True
         self.winner_name: str = None  # All winner attributes default to None when no winner or based on Winchecker
         self.winner_marker: str = None
         self.win_type: str = None
         self.win_row: int = -1
         self.win_column: int = -1
         self.__win: LineChecker = self.ConnectFourWinChecker(self.board)
         self.players = self.create_human_players() # Default to two player mode

    def create_board(self):
        return Board(self.rows, self.columns)

    def create_human_players(self) -> Tuple[Player, Player]:
        return (
            self.ConnectFourPlayer("Player 1", "r"),
            self.ConnectFourPlayer("Player 2", "y"),
        )
    def create_ai_player(self, difficulty: Optional[bool]=True) -> Tuple[Player, Player]:
        self.players = (
            self.ConnectFourPlayer("Player 1", "r"),
            self.AIPlayer(difficulty=difficulty, game=self),
        )

    # def add_two_hard_move_ai_players_for_testing(self):
    #     self.players = (
    #         self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=True, hard_test=True),
    #         self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=True, hard_test=True),
    #     )

    # def add_ai_players_for_testing(self, difficulty_one: bool, difficulty_two: bool):
    #     self.players = (
    #         self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=difficulty_one),
    #         self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=difficulty_two),
    #     )

    @property
    def board_size(self):
        return self.rows * self.columns

    def print_winner(self):
        print(f"Winning Player: {self.winner_name}")
        print(f"Playing {self.winner_marker}")
        print(f"Won in {self.win_type} at row {self.win_row + 1} and column {self.win_column + 1}.")
    
    def get_winner_attributes(self):
        return self.winner_name, self.winner_marker, self.win_type, self.win_row, self.win_column
    
    def print_stats(self):
        for player in self.players:
            print(player.__str__())

    def is_valid(self, row, col):
        if 0 <= col < self.columns: # validate the move is on the board
            return not self.board.square_is_occupied(row, col)
        return False

    def make_move(self, col, marker):
        for row in range(self.rows - 1, -1, -1):
            if self.is_valid(row, col):
                self.board.add_to_square(row, col, marker)
                self.move_list.append((row, col))
                self.height_list[col] = row
                self.size_list[row] += 1
                self.round_count += 1
                return True
        return False
    
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()

    def reset_game_state(self):
        self.reset_board()
        self.reset_winner()
        self.move_list = []
        self.round_count = 0
        self.go_first = not self.go_first

    # def update_ai_player_level(self, difficulty: bool):
    #     for player in self.players:
    #         if isinstance(player, self.AIPlayer): 
    #             player.difficulty = difficulty

    def update_player_name(self, name: str, marker: str) -> None:
        """Updates a player's name based on their marker ('r' or 'y')."""
        marker = marker.lower()    
        if marker not in {"r", "y"}:
            raise ValueError(f"Invalid marker '{marker}'. Must be 'r' or 'y'.")
        marker_to_index = {"r": 0, "y": 1}
        self.players[marker_to_index[marker.lower()]].name = name

    def update_players_stats(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player.name == self.winner_name:
                player.won()
            elif self.winner_name is not None:
                player.lost()
    
    def update_winner_info(self) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        winner_info = self.get_winner_info()
        for player in self.players:
            if player.marker == winner_info["marker"]:
                self.winner_name = player.name
                self.winner_marker = player.marker
        self.win_type = winner_info["type"]
        self.win_row = winner_info["row"]
        self.win_column = winner_info["column"]

    def check_winner(self):
        return self.__win._check_for_winner()

    def get_winner_info(self):
        return self.__win.get_win_info()
    
    def reset_winner(self):
        self.__win.reset_win_info()
        self.winner_name = None
        self.winner_marker = None
        self.win_type = None
        self.win_row = -1
        self.win_column = -1
        
    class ConnectFourWinChecker(LineChecker):
        def __init__(self, board, win_value=4):
            super().__init__(board, win_value)

        def _check_full_rows(self, win_value: int) -> Optional[tuple]:
            for r, row in enumerate(self._board.get_rows()):
                for i in range(4):
                    row_slice = row[i:i + 4]
                    if winner := LineChecker.check_all_same(row_slice):
                        return winner, "row", r, i
    
        def _check_full_columns(self, win_value: int) -> Optional[tuple]:
            for c, column in enumerate(self._board.get_columns()):
                for i in range(3):
                    col_slice = column[i:i + 4]
                    if winner := LineChecker.check_all_same(col_slice):

                        return winner, "column", i, c
        
        def _check_diagonals(self, win_value: int) -> Optional[tuple]:
            for l, line in enumerate(self._board.get_diagonals(win_value, "right")):
                if winner := LineChecker.check_all_same(line):
                    r, c = int_converter(l, self._board.columns - win_value + 1)
                    return winner, "right_diagonal", r, c
            for l, line in enumerate(self._board.get_diagonals(win_value, "left")):
                if winner := LineChecker.check_all_same(line):
                    r, c = int_converter(l, self._board.columns - win_value + 1)
                    c = self._board.columns - 1 - c
                    return winner, "left_diagonal", r, c


    class ConnectFourPlayer(Player):
        def __init__(self, name: str = "Me", marker: str = "r"):
            super().__init__(name, marker)  # Initialize the name first
            self.marker = marker  # Use the property setter for validation
            self.marker_name = self._get_marker_name()

        @Player.name.setter
        def name(self, value):
            """Ensure name is assigned for empty string."""
            if not value:
                value = f"Anonymous {self.marker.capitalize()}"
            self._name = value  # Directly set the private attribute

        @Player.marker.setter
        def marker(self, value):
            """Ensure marker is only 'r' or 'y'."""
            if value not in {"r", "y", "R", "Y"}:
                raise ValueError(f"Invalid marker: {value}. Must be 'r' or 'y'.")
            self._marker = value.lower()  # Directly set the private attribute
            self.marker_name = self._get_marker_name()  # Update marker_name when marker changes
        
        def _get_marker_name(self):
            """Determine the marker name based on the marker value."""
            return "Red" if self._marker == "r" else "Yellow"
        

    class AIPlayer(Player):

        def __init__(self, name: str = "CPU", marker: str = "y", difficulty: bool = False, game: 'ConnectFour' = None):
            """AIPlayer is a child class of Player"""
            super().__init__(name, marker)
            self.game = game
            self.score = 0
        
        def get_random_column(self): 
                return randint(0, self.game.columns - 1)

        def random_int(self) -> tuple[int, int]:
            """Selects any open random positions on the board. Returns row and column index."""
            column = self.get_random_column()
            while self.game.board.square_is_occupied(0, column):
                column = self.get_random_column()

            return column

        def move(self):
 
            if (move:= self.win_or_block()) is not None:
                print("Played WIN or BLOCK")
                print(f"Computer's move {move}")
                # sleep(5)
                return move 
            print(self.game.height_list)
            print(self.game.size_list)
            # print("Played RANDOM")
            # sleep(5)
            return self.random_int()

        # def get_empty_move_positions(self):
        #     for column in range(self.game.board.columns):
        #         return [(self.game.height_list[column] - 1, column) for column in range(self.game.board.columns)]
             
        def win_or_block(self):
            block_position = -1
            horizontal_midpoint = self.game.board.columns // 2

            def marker_check(line):
                if marker := LineChecker.check_all_same(line):
                    if marker == 'y':
                            return True
                    elif marker == 'r':
                        return False
                return None

            def check_and_update(line, row, column):
                if not line:
                    return None
                nonlocal block_position
                win_or_block = marker_check(line)
                if win_or_block is True:
                    return column  # Winning move
                elif win_or_block is False:
                    block_position = column  # Possible block move
                return None
            
            def left_right_pattern(line, square):
                if not (line and square):
                    return None
                line.append(square)
                return line
            
            def star_pattern_check(row, row_height, column):
                diagonal_line = self.game.board.get_diagonal_segment
                down_left = self.game.board.get_square_value(row_height, column - 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row - 1, col=column + 1, length = 2, up=True, right=True), 
                        down_left
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                down_right = self.game.board.get_square_value(row_height, column + 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row - 1, col=column - 1, length = 2, up=True, right=False), 
                        down_right
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                up_right = self.game.board.get_square_value(row - 1, column + 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row_height, col=column - 1, length = 2, up=False, right=False), 
                        up_right
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                up_left = self.game.board.get_square_value(row - 1, column - 1)
                one_two_pattern = left_right_pattern(
                        diagonal_line(row=row_height, col=column + 1, length = 2, up=False, right=True), 
                        up_left
                    )
                if move := check_and_update(one_two_pattern, row, column):
                        return move
                return None
            
            def down_check(row_height, column):
                column_line = self.game.board.get_column_segment
                if (move := check_and_update(column_line(row=row_height, col=column, length = 3), row, column)) is not None:
                    print(f"WON in DOWN COL at move {move}")
                    return move
                
                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row_height, col=column + 1, length = 3, up=False, right=True), row, column)) is not None:
                    print(f"WON in DOWN Diag Right {move}")
                    return move
                if (move := check_and_update(diagonal_line(row=row_height, col=column - 1, length = 3, up=False, right=False), row, column)) is not None:
                    print(f"WON in DOWN Diag Left {move}")
                    return move
                return None
            
            def right_and_up_check(row, column):
                row_line = self.game.board.get_row_segment
                if (move := check_and_update(row_line(row=row, col=column + 1, length=3), row, column)):
                    return move
                
                # One-two pattern
                one_two_pattern = left_right_pattern(
                    row_line(row=row, col=column + 1, length = 2), 
                    left_value
                )
                if (move := check_and_update(one_two_pattern, row, column)):
                    return move

                # Two-one pattern
                two_one_pattern = left_right_pattern(
                    row_line(row=row, col=column - 2, length=2),
                    right_value
                )
                if (move := check_and_update(two_one_pattern, row, column)):
                    return move
                
                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row - 1, col=column + 1, length=3, up=True, right=True), row, column)):
                    return move
                
                return None
                
            def left_and_up_check(row, column):
                row_line = self.game.board.get_row_segment
                if (move := check_and_update(row_line(row=row, col=column - 1, length = 3, right=False), row, column)) is not None:
                    return move
                
                # One-two pattern here
                one_two_pattern = left_right_pattern(
                    row_line(row=row, col=column + 1, length = 2), 
                    left_value
                )
                
                if (move := check_and_update(one_two_pattern, row, column)) is not None:
                    return move
                # Two-one pattern here
                two_one_pattern = left_right_pattern(
                    row_line(row=row, col=column - 2, length = 2), 
                    right_value
                )
                if (move := check_and_update(two_one_pattern, row, column)) is not None:
                        return move
                
                diagonal_line = self.game.board.get_diagonal_segment
                if (move := check_and_update(diagonal_line(row=row - 1, col=column - 1, length = 3, up=True, right=False), row, column)) is not None:
                    return move
                
                return None

            for column, row_height in enumerate(self.game.height_list):
                # Check if column is full; height list at 0 means the top row is occupied and there are no moves in the column
                if row_height == 0:
                    continue 
    
                # Update the row to the current open position in the column
                row = row_height - 1
    
                # Check for three in a row down, down-right and down left starting from vertical mid-point
                if row_height <= self.game.board.rows // 2:
                    if move := down_check(row_height, column):
                        print(f"WON in DOWN {move}")
                        return move
                
                # Check all diagonal directions with one-two or two-one patterns
                if move:= star_pattern_check(row, row_height, column):
                    print(f"Won in a Star at {move}")
                    return move
                
                left_value = self.game.board.get_square_value(row, column - 1)
                right_value = self.game.board.get_square_value(row, column + 1)

                # Check if both neighbors of current open position in the column are either out of bounds or empty to avoid unnecessary checks
                if (left_value == 0 or left_value is None) and (right_value == 0 or right_value is None):
                    continue
                    
                if column <= horizontal_midpoint: 
                    # Check row right combinations and up-right diagonal
                    if move := right_and_up_check(row, column):
                        print(f"WON in ROW RIGHT at Col {move}")
                        return move
        
                if column >= horizontal_midpoint:
                    # Check row left combinations and up-left diagonal
                    if (move := left_and_up_check(row, column)) is not None:
                        print(f"WON in ROW LEFT at Col {move}")
                        return move
       
            return block_position if block_position != -1 else None
            
class TicTacToe:

    def __init__(self):
         self.board: List[List] = self.create_board()
         self.move_list: List = []
         self.round_count: int = 0
         self.go_first: bool = True
         self.winner_name: str = None  # All winner attributes default to None when no winner or based on Winchecker
         self.winner_marker: str = None
         self.win_type: str = None
         self.win_index: int = None
         self.__win: LineChecker = LineChecker(self.board, 3)
         self.players = self.create_human_players() # Default to two player mode

    def create_board(self):
        return Board(3,3)

    def create_human_players(self) -> Tuple[Player, Player]:
        return (
            self.TicTacToePlayer("Player 1", "x"),
            self.TicTacToePlayer("Player 2", "o"),
        )
    def create_ai_player(self, name: Optional[str], difficulty: Optional[bool]) -> Tuple[Player, Player]:
        self.players = (
            self.TicTacToePlayer("Player 1", "x"),
            self.AIPlayer(name=name, difficulty=difficulty, game=self),
        )

    def add_two_hard_move_ai_players_for_testing(self):
        self.players = (
            self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=True, hard_test=True),
            self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=True, hard_test=True),
        )

    def add_ai_players_for_testing(self, difficulty_one: bool, difficulty_two: bool):
        self.players = (
            self.AITestPlayer(name="AI one", marker="x", game=self, difficulty=difficulty_one),
            self.AITestPlayer(name="AI two", marker="o", game=self, difficulty=difficulty_two),
        )

    @property
    def board_size(self):
        return self.board.rows * self.board.columns

    def print_winner(self):
        print(f"Winning Player: {self.winner_name}")
        print(f"Playing {self.winner_marker}")
        if self.win_index == -1:
             print(f"Won in {self.win_type}")
        else:
            print(f"Won in {self.win_type} {self.win_index + 1}")
    
    def get_winner_attributes(self):
        return self.winner_name, self.winner_marker, self.win_type, self.win_index
    
    def print_stats(self):
        for player in self.players:
            print(player.__str__())

    def is_valid(self, row, col):
        if 0 <= (row * col) < self.board_size: # validate the move is on the board
            return not self.board.square_is_occupied(row, col)
        return False

    def make_move(self, row, col, marker):
        if self.is_valid(row, col):
            self.board.add_to_square(row, col, marker)
            self.move_list.append((row, col))
            self.round_count += 1
            return True
        return False
    
    def reset_board(self) -> None:
        """Sets each square in the board to a blank."""
        self.board.reset_board()

    def reset_game_state(self):
        self.reset_board()
        self.reset_winner()
        self.move_list = []
        self.round_count = 0
        self.go_first = not self.go_first

    def update_ai_player_level(self, difficulty: bool):
        for player in self.players:
            if isinstance(player, self.AIPlayer): 
                player.difficulty = difficulty

    def update_player_name(self, name: str, marker: str) -> None:
        """Updates a player's name based on their marker ('x' or 'o')."""
        marker = marker.lower()    
        if marker not in {"x", "o"}:
            raise ValueError(f"Invalid marker '{marker}'. Must be 'x' or 'o'.")
        marker_to_index = {"x": 0, "o": 1}
        self.players[marker_to_index[marker.lower()]].name = name

    def update_players_stats(self) -> None:
        """Updates the game statistics on the two players based on if there is a winner or not."""
        for player in self.players:
            player.game_played()
            if player.name == self.winner_name:
                player.won()
            elif self.winner_name is not None:
                player.lost()
    
    def update_winner_info(self) -> None:
        """Updates the winner attributes to store information on the current winner. Resets to default values if
        there is no winner. """
        winner_info = self.get_winner_info() # returns dictionary with keys: marker, type, row, column
        for player in self.players:
            if player.marker == winner_info["marker"]:
                self.winner_name = player.name
                self.winner_marker = player.marker
        self.win_type = winner_info["type"]
        # marker_to_index = {"row": row, "column": col}
        self.win_index = winner_info.get(self.win_type, -1)

    def check_winner(self):
        return self.__win._check_for_winner()

    def get_winner_info(self):
        return self.__win.get_win_info()
    
    def reset_winner(self):
        self.__win.reset_win_info()
        self.winner_name = None
        self.winner_marker = None
        self.win_type = None
        self.win_index = None
        

    class TicTacToePlayer(Player):

        def __init__(self, name: str = None, marker: str = None):
            super().__init__(name, marker)  # Initialize the name first
            self.marker = marker  # Use the property setter for validation

        @Player.name.setter
        def name(self, value):
            """Ensure name is assigned for empty string."""
            if not value:
                value = f"Anonymous {self.marker.capitalize()}"
            self._name = value  # Directly set the private attribute

        @Player.marker.setter
        def marker(self, value):
            """Ensure marker is only 'x' or 'o'."""
            if value not in {"x", "o", "X", "O"}:
                raise ValueError(f"Invalid marker: {value}. Must be 'x' or 'o'.")
            self._marker = value.lower()  # Directly set the private attribute

    class AIPlayer(Player):

        def __init__(self, name: str = 'CPU', marker: str = "o", difficulty: bool = False, game: 'TicTacToe' = None):
            """AIPlayer is a child class of Player and contains all the functionality for a one-player game
            against the computer. The computer player has three modes: easy, intermediate and hard.
            The computer is defaulted to name 'Computer' and marker 'O'"""
            super().__init__(name, marker)
            self.game = game
            self._difficulty = None  # Backing private attribute
            self.difficulty = difficulty  # None is easy mode, False is intermediate mode, True is hard mode
            self.corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            self.insides = [(0, 1), (1, 0), (1, 2), (2, 1)]

        @property
        def difficulty(self) -> Optional[bool]:
            """Getter for the difficulty attribute."""
            return self._difficulty

        @difficulty.setter
        def difficulty(self, value: Optional[bool]) -> None:
            """Setter for the difficulty attribute, ensuring it's True, False, or None."""
            if value not in {True, False, None}:
                raise ValueError("Difficulty must be True, False, or None.")
            self._difficulty = value
        

        def get_fork_index(self, lines: list[Union[str, int]]) -> Optional[Union[int, bool]]:
            """Finds the position of a branch of a fork. Returns an integer of the row or column index
            if there is a column or row with a branch of a fork. Returns True if there is a diagonal fork 
            branch position. Returns None if no fork branch is found."""
            for index, line in enumerate(lines):
                fork = Counter(line)
                if fork["o"] == 1 and fork[0] == 2:
                    if len(lines) == 1:  # this is for the two diagonals which are just a 1x3 matrix
                        return True
                    else:
                        return index
            else:
                return

        def check_fork(self, board: Board) -> Optional[tuple[int, int]]:
            """Checks for forks on the board that allows the computer to make a move where it will have 
            a winning position in two or more lines. The function searches the board for any fork branches.
            If there is an intersection of two branches, the fork is added to a list, and randomly selects a fork.
            Returns the row and column position of the selected fork, or else return None if there are no forks."""
            fork_row_index = None
            fork_column_index = None
            fork_diagonal_right = None
            fork_diagonal_left = None
            # list of all potential forks on a board after a given move by a human player
            fork_positions = []

            rows = self.game.board.get_rows()
            columns = self.game.board.get_columns()

            # check rows, columns and two diagonals to get an index of any fork position for row/col,
            # or T/F for diagonal fork position
            fork_row_index = self.get_fork_index(rows)
            fork_column_index = self.get_fork_index(columns)
            fork_diagonal_right = self.get_fork_index(
                self.game.board.get_diagonals(3, "right"))  # get_fork_index only accepts a list of lines or 2D array
            fork_diagonal_left = self.get_fork_index(self.game.board.get_diagonals(3, "left"))

            # check for all forks: a fork is the intersection of a row and column or an intersection of a row or column
            # and a diagonal. For any fork in a row and column intersection or a row and diagonal intersection
            if fork_row_index is not None:
                if fork_column_index is not None:
                    if not self.game.board.square_is_occupied(fork_row_index, fork_column_index):
                        fork_positions.append([fork_row_index, fork_column_index])
                # row and right diagonal fork has the same column position as the row
                if fork_diagonal_right:
                    if not self.game.board.square_is_occupied(fork_row_index, fork_row_index):
                        fork_positions.append([fork_row_index, fork_row_index])
                        # row and left diagonal fork has the opposite column position as the row reflected through
                        # the centre horizontal line
                if fork_diagonal_left:
                    if not self.game.board.square_is_occupied(fork_row_index, 2 - fork_row_index):
                        fork_positions.append([fork_row_index, 2 - fork_row_index])

            # for any fork in a column and diagonal intersection    
            if fork_column_index is not None:
                # column and right diagonal fork has the same row position as the column
                if fork_diagonal_right:
                    if not self.game.board.square_is_occupied(fork_column_index, fork_column_index):
                        fork_positions.append([fork_column_index, fork_column_index])
                # column and left diagonal fork has the opposite row position as the column reflected through
                # the centre vertical line
                if fork_diagonal_left:
                    if not self.game.board.square_is_occupied(2 - fork_column_index, fork_column_index):
                        fork_positions.append([2 - fork_column_index, fork_column_index])

            # for a fork in the diagonal intersection: the centre is the intersection
            if fork_diagonal_right and fork_diagonal_left:
                fork_positions.append([1, 1])

            if fork_positions:  # selects a random fork position if there is more than one fork or just the one
                return fork_positions[randint(0, len(fork_positions) - 1)]
            else:
                return  # no forks were found

        def two_blanks(self, board) -> Optional[tuple[int, int]]:
            """Finds any line with two blanks and one 'O' marker. Used as alternative to random 
            integers and allows for possibility of victory. Returns row and column index else None."""
            rows = self.game.board.get_rows()
            columns = self.game.board.get_columns()
            diagonals = [self.game.board.get_diagonals(3, "right")[0],
                        self.game.board.get_diagonals(3, "left")[0]]  # right diagonal is index 0, and left is index 1
            
            line_checker = LineChecker.two_blanks # use static method that finds a row with two blanks and an 'o' marker

            # returns the first found unoccupied square in a line with two blanks for intermediate mode or for possible hard mode win
            for index, row in enumerate(rows):
                check_row = line_checker(row, "o", 1)
                if check_row:
                    col = choice(check_row["o"][0]["window_indices"])
                    return index, col
                
            for index, col in enumerate(columns):
                check_col = line_checker(col, "o", 1)
                if check_col:
                    row = choice(check_col["o"][0]["window_indices"])
                    return row, index
                
            for index, diag in enumerate(diagonals):
                check_diag = line_checker(diag, "o", 1)
                if check_diag:
                    window_indices = check_diag["o"][0]["window_indices"] 
                    if index == 0:  # Right diagonal
                        row = col = choice(window_indices)
                    else:  # Left diagonal
                        row = choice(window_indices)
                        col = 2 - row

                    return row, col

        def random_ints(self, board: Board) -> tuple[int, int]:
            """Selects any open random positions on the board. Returns row and column index."""
            row = randint(0, 2)
            column = randint(0, 2)
            while self.game.board.square_is_occupied(row, column):
                # print(f"Row {row}, Col {column}")
                row = randint(0, 2)
                column = randint(0, 2)

            return row, column

        def defence_mode(self, board: Board) -> tuple[int, int]:
            """AI strategy for when the computer plays second. Strategy is based on the first move
            by the human player. The AI always optimizes for a win or draw. Returns optimal move."""
            

            def assert_test(two_ints: tuple[int, int]):
                assert len(two_ints) == 2
                a, b = two_ints
                assert a is not None
                assert b is not None 


            r, c = self.game.move_list[0]
            if self.game.round_count == 1:

                if (r, c) == (1, 1):
                    move = choice(self.corners)
                    # print(*move)
                    assert move is not None
                    assert_test(move)
                    # move = choice(self.corners)
                else:
                    move = 1, 1
                
                return move

            elif self.game.round_count == 3:
                if (r, c) == (1, 1):
                    # Only triggered when the opposite corner to the move in previous round was played by player X
                    for corner in self.corners:
                        if not self.game.board.square_is_occupied(*corner):  # randomly select one of the two free corners
                            move = corner
                            assert move is not None
                            assert_test(move)
                            return move#corner
                elif (r, c) in self.corners:
                    if not self.game.board.square_is_occupied((r + 2) % 4, (c + 2) % 4):
                        move = (r + 2) % 4, (c + 2) % 4
                        assert_test(move)
                        assert move is not None
                        return move#(r + 2) % 4, (c + 2) % 4
                    else:
                        move = choice(self.insides)
                        assert_test(move)
                        assert move is not None
                        return move#choice(self.insides)
                elif (r, c) in self.insides:
                    r1, c1 = self.game.move_list[2]
                    if (r1, c1) in self.insides:
                        if r == 1:
                            move = choice([0, 2]), c
                            assert move is not None
                            assert_test(move)
                            return move#choice([0, 2]), c
                        else:
                            move = r, choice([0, 2])
                            assert move is not None
                            assert_test(move)
                            return move#r, choice([0, 2])
                    else:
                        if r == 1:
                            move = r1, c
                            assert move is not None
                            assert_test(move)
                            return r1, c
                        else:
                            move = r, c1
                            assert move is not None
                            assert_test(move)
                            return r, c1

            elif self.game.round_count == 5:
                if (r, c) == (1, 1):
                    r, c = self.game.move_list[4]
                    # find a two blank strategy and place in same row or column as the last x move
                    if self.game.board.get_rows()[r].count(0) == 1:
                        move = r, (c + 2) % 4
                        assert move is not None
                        assert_test(move)
                    elif self.game.board.get_columns()[c].count(0) == 1:
                        move = (r + 2) % 4, c
                        assert move is not None
                        assert_test(move)

                elif (r, c) in self.corners:
# Might need this two blank strategy to keep win alive
                    # if move := self.two_blanks(self.game.board):
                    #     return move

                    for corner in self.corners:
                        if not self.game.board.square_is_occupied(*corner):
                            move = corner
                            assert move is not None
                            assert_test(move)

                elif move := self.two_blanks(self.game.board):
                    assert move is not None
                    assert_test(move)
                    return move

                else:
                    print("IM HERE!!!!")
                    print(self.game.move_list)
                    print(self.game.board)
                    move = self.random_ints(self.game.board)
                    print(f"MOVE {move}")
                return move
            
            else:
                if move := self.two_blanks(self.game.board):
                    assert move is not None
                    assert_test(move)
                    return move
                else:
                    move = self.random_ints(self.game.board)

                    assert move is not None
                    assert_test(move)
                    return move#self.random_ints(self.game.board)

        def offence_mode(self, board: Board) -> tuple[int, int]:
            """AI strategy for when the computer plays first. Strategy is based on the first move by the
            computer and human player. The AI always optimizes for a win or draw. Returns optimal move."""
            # for testing purposes so hard mode can play versus hard mode used by TestGame class; otherwise, ignored
            # if self.game.round_count % 2 == 0:
            #     return self.defence_mode(self.game.board)

            if self.game.round_count == 0:
                # Only allow for corner or centre start to guarantee a win or draw
                starts = self.corners + [(1, 1)]
                return choice(starts)  # add element of randomness to first move

            elif self.game.round_count == 2:
                r, c = self.game.move_list[0]
                if (r, c) == (1, 1):
                    if self.game.move_list[1] not in self.corners:
                        move = choice(self.corners)
                    else:
                        r, c = self.game.move_list[1]
                        move = (r + 2) % 4, (c + 2) % 4

                elif (r, c) in self.corners:
                    if self.game.move_list[1] == (1, 1):
                        # print("HERE")

                        # move = (r + 2) % 4, c
                        move = (r + 2) % 4, (c + 2) % 4

                    elif self.game.move_list[1] in self.corners:
                        for corner in self.corners:
                            if self.game.board.square_is_occupied(*corner):
                                pass
                            else:
                                move = corner

                    elif self.game.move_list[1] in self.insides:
                        for i in range(3):
                            if self.game.board.get_rows()[r - i].count("x") == 1:
                                if self.game.board.square_is_occupied(1, c):
                                    pass
                                else:
                                    move = ((r + 2) % 4), c
                            elif self.game.board.get_columns()[c].count("x") == 1:
                                move = r, ((c + 2) % 4)
                return move

            elif self.game.round_count == 4:
                if move := self.check_fork(self.game.board):
                    return move

                elif self.game.move_list[1] in self.corners:
                    for move in self.corners:
                        if self.game.board.square_is_occupied(*move):
                            pass
                        else:
                            return move
                elif move := self.two_blanks(self.game.board):
                    return move

                else:
                    return self.random_ints(self.game.board)

            else:
                if move := self.two_blanks(self.game.board):
                    return move

                return self.random_ints(self.game.board)

        def win_or_block(self, board: Board) -> Optional[tuple[int, int]]:
            """Checks for a win or block. Selects the first found win position or a random block position if there are
            more than one block moves."""
            block_positions = []  # Makes a list of all possible blocking points on the board of the opponent

            lines = [self.game.board.get_rows(),
                    self.game.board.get_columns(),
                    self.game.board.get_diagonals(3, "right"),
                    self.game.board.get_diagonals(3, "left")
                    ]
            
            line_checker = LineChecker.line_check

            def get_blank_index(line_checker_dictionary): # guarantees the index for each function call below
                if found_blank := line_checker_dictionary.get("o"):
                    return found_blank[0]["first_index"]
                return line_checker_dictionary.get("x")[0]["first_index"]
            

            for indicator, line in enumerate(lines): # check top to bottom rows, columns, right and left diagonals

                for index, squares in enumerate(line):
                    # check for one blank and two marker pattern 
                    check_line = line_checker(squares, target_element=0, target_count=1, other_element="any", other_count=2, window_size=3)  
                    if check_line: # if line checker dictionary is not empty, it must have found either an 'o' or 'x' only 
                        blank_index = get_blank_index(check_line)
                        if indicator == 0: # 0 indicates the line of squares is a row, so index is row index and blank_index is the column index
                            if "o" in check_line.keys():
                                return index, blank_index
                            else:  
                                block_positions.append([index, blank_index])

                        elif indicator == 1: # 1 indicates the line of squares is a column
                                if "o" in check_line.keys():
                                    return blank_index, index
                                else: 
                                    block_positions.append([blank_index, index])
                        
                        elif indicator == 2: # 2 indicates the line of squares is a right diagonal
                                if "o" in check_line.keys():
                                    return blank_index, blank_index
                                else:
                                    block_positions.append([blank_index, blank_index])

                        else: # 3 or else indicates the line of squares is a left diagonal
                                if "o" in check_line.keys():
                                    return blank_index, 2 - blank_index
                                else: 
                                    block_positions.append([blank_index, 2 - blank_index])
            if block_positions:
                # Use randomly selected block position from max of three for variety sake
                return block_positions[randint(0, len(block_positions) - 1)]
            else:
                return None

        def move(self, board: Board) -> Union[tuple[int, int], list[int]]:
            """Selects a move for the AI player based on the play mode of easy, intermediate or hard. """
            if self.difficulty is None:  # easy mode
                result = self.random_ints(self.game.board)
                assert result is not None 
                return result
                # return self.random_ints(self.game.board)

            if move := self.win_or_block(self.game.board):  # intermediate or hard mode always checks for win or block first
                return move
                # result = move
                # assert result is not None 
                # return result
            

            if self.difficulty:  # hard mode
                if self.game.go_first:  # strategy is based on if human player plays first or not (go_first is for human player
                    
                    result = self.defence_mode(self.game.board)
                    assert result is not None 
                    return result
                    # return self.defence_mode(self.game.board)
                else:

                    result = self.offence_mode(self.game.board)
                    assert result is not None 
                    return result
                    # return self.offence_mode(self.game.board)

            else:  # intermediate mode always checks for a fork first then for two blanks after two random moves
                if self.game.round_count > 3:
                    if move := self.check_fork(self.game.board):
                        return move
                    if move := self.two_blanks(self.game.board):
                        return move
                return self.random_ints(self.game.board)
    
    class AITestPlayer(AIPlayer):

        def __init__(self, name: str = 'Computer', marker: str = "o", difficulty: bool = False, game: 'TicTacToe' = None, hard_test: bool = False):
            """AIPlayer is a child class of Player and contains all the functionality for a one-player game
            against the computer. The computer player has three modes: easy, intermediate and hard.
            The computer is defaulted to name 'Computer' and marker 'O'"""
            super().__init__(name, marker, difficulty, game)
            self.hard_test = hard_test

        def move(self, board: Board) -> Union[tuple[int, int], list[int]]:
            """Selects a move for the AI player based on the play mode of easy, intermediate or hard. """
            if self.difficulty is None:  # easy mode
                result = self.random_ints(self.game.board)
                return result

            if result := self.win_or_block(self.game.board):  # intermediate or hard mode always checks for win or block first
                return result
               

            if self.difficulty:  # hard mode
                if self.game.go_first:  # strategy is based on if human player plays first or not (go_first is for human player)
                    if self.hard_test and (self.game.round_count % 2 == 0):
                        return self.offence_mode(self.game.board)
                    return self.defence_mode(self.game.board)
                else:
                    if self.hard_test and (self.game.round_count % 2 == 1):
                        return self.defence_mode(self.game.board)

                    return self.offence_mode(self.game.board)

            else:  # intermediate mode always checks for a fork first then for two blanks after two random moves
                if self.game.round_count > 3:
                    if move := self.check_fork(self.game.board):
                        return move
                    if move := self.two_blanks(self.game.board):
                        return move
                return self.random_ints(self.game.board)
            
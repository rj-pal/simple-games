from cli import TicTacToeCLI, ConnectFourCLI
from games.games import Solitare, ConnectFour, TicTacToe, EmptyDrawPileError, EmptyFoundationPileError
from utils.game_options import GameOptions
from utils.clitools import clear_screen, delay_effect, print_menu_screen, menu_select
from utils.strings import SIMPLE_GAMES_START
from core.board import LineChecker, Board
import unicodedata

# def get_display_width(text):
#     """Calculate the display width of a string, considering emoji width."""
#     return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)

# def pad_to_width(text, width=8):
#     """Pad a string to a fixed width, considering emoji and special characters."""
#     text_width = get_display_width(text)
#     return text + " " * (width - text_width)

# def print_tableau(tableau):
#     tableau_lists = [card_stack.to_list()[::-1] for card_stack in tableau]
#     max_height = max(len(stack) for stack in tableau_lists)
    
    # # Pad each list so all columns have the same number of rows
    # padded_tableau = [card_list + [" " * 15] * (max_height - len(card_list)) for card_list in tableau_lists]

    # for row in zip(*padded_tableau):
    #     print(" ".join(pad_to_width(word, 15) for word in row))

# def unicode_bordered_card(card):
#     width = len(card) + 2
#     top_bottom = "╭" + "─" * width + "╮"
#     middle = f"│ {card} │"
#     bottom = "╰" + "─" * width + "╯"
#     return f"{top_bottom}\n{middle}\n{bottom}"

# def print_tableau(tableau):
#     tableau_lists = [card_stack.to_list()[::-1] for card_stack in tableau]
#     max_height = max(len(stack) for stack in tableau_lists)
#     padded_tableau = [card_list + [" " * 15] * (max_height - len(card_list)) for card_list in tableau_lists]
#     for row in zip(*padded_tableau):
#         print(" ".join(word.rjust(15) for word in row)) 

def print_tableau(tableau):
    def normalize_cards_in_stack(card_stack, width=12):
        new_card_stack = []
        for card in card_stack:
            if card == "🎴":
                card = card.center(11)
            elif card == " ":
                card = card.center(width)
            else:
                card = card.center(width + 1)
            new_card_stack.append(card)
        return new_card_stack
    
    def print_labels(column_width=17):
        print("TABLEAU")
        tableau_labels = ["Stack 1", "Stack 2", "Stack 3", "Stack 4", "Stack 5", "Stack 6", "Stack 7"]
        print()
        for label in tableau_labels:
            print(f"{label:^{column_width}}", end='')
        print()
        print(" " * 4 + (" -------" + " " * 9) * 7 )

    # Change my stack to a list
    tableau_lists = tableau #[card_stack.to_list()[::-1] for card_stack in tableau]
    
    # Get the longest card stack to add blank cards for padding of column stacks 
    max_height = max(len(stack) for stack in tableau_lists)

    # Ensure all card stacks are the same length
    padded_tableau = [stack + [" "] * (max_height - len(stack)) for stack in tableau_lists]

    # Ensure all cards are padded to the same size for alignment in columns
    padded_cards_and_tableau = [normalize_cards_in_stack(card_stack) for card_stack in padded_tableau]
    
    # Print name and labels for tableau
    print_labels()

    column_space = " " * 5
    for row in zip(*padded_cards_and_tableau):
        print(column_space.join(card for card in row))

def print_foundation_piles(piles):
    print("FOUNDATION PILES\n")
    top_cards = [card_stack.top_card() if card_stack.is_empty() else card_stack.top_card().face for card_stack in piles.values()]
    print("   |   ".join(top_cards))

def print_draw_pile(pile):
    print("STOCK PILE")
    print()
    if not pile:
        print("🎴".center(6))
        
    else:
        print("⚔️".center(6))

def print_waste_pile(pile):
    # print("WASTE PILE")#.rjust(26))
    # print()
    if len(pile) == 0:
        print("⚔️".center(6))
    else:
        for card in pile:
            print(card)

    return
    for i, card in enumerate(pile):
        blank = " ".ljust(8)
        play_now = "Playing: ".ljust(8)
        if i == len(pile) - 1:
            # print(card, " < - Now Playing")
            print(play_now, card.face.rjust(10))
        else:
            # print(card)
            print(blank, card.face.rjust(10))
    # temp_card = pile.head.next
    # while display_number > 0:
    #     if pile.is_empty():
    #         break
    #     else:
    #         print(temp_card.value)
    #         temp_card = temp_card.next
    #         display_number -= 1
    
        

    

def print_card_table(tableau, piles, pile):#, fixed_height):
    print_foundation_piles(piles)
    print()
    print_tableau(tableau)#, fixed_height)
    print()
    print_draw_pile(pile)
    print()
   

def run_game():
    clear_screen()
    test = Solitare(klondike_value=3)
    # print(test.size)
    # exit()
    def stack_validator():
        while True:
            try:
                # minus one for zero indexing
                position = int(input("Enter the card stack number: ")) - 1
                if position in range(7):
                    return position
                print("Invalid stack number. Enter only 1 to 7. Try again.\n")
            except ValueError:
                print("Invalid input. Enter only 1 to 7. Try again.\n")
            except (EOFError, KeyboardInterrupt):
                print("\nInput terminated. Exiting program.")
                exit(1)

    def move_validator():
        while True:
            try:
                move = int(input("Enter your response: "))
                if move in {1, 2, 3, 4, 5}:
                    return move
                else:
                    print("Invalid move option. Please enter a number between 1 and 5. Try again.\n")
            except ValueError:
                print("Invalid input. Enter only a number between 1 and 5. Try again\n")
            except (EOFError, KeyboardInterrupt):
                print("\nInput terminated. Exiting program.")
                exit(1)

    def suit_validator():
        suit_dictionary = {1: "S", 2: "H", 3: "D", 4: "C"}
        while True:
            try:
                suit = int(input("Press 1: for Spade, 2 for Heart, 3 for Diamond, 4 for Club: "))
                if suit in {1, 2, 3, 4, 5}:
                    return suit_dictionary[suit]
                else:
                    print("Invalid suit option. Please enter a number between 1 and 4 to get the correct foundation pile. Try again.\n")
            except ValueError:
                print("Invalid input. Enter only a number between 1 and 4. Try again\n")
            except (EOFError, KeyboardInterrupt):
                print("\nInput terminated. Exiting program.")
                exit(1)

    def number_of_cards_validator():
        while True:
            try:
                number_of_cards = int(input())
                if number_of_cards in range(1, 15):
                    return number_of_cards
                print("There are only 14 cards possible in a stack. Please enter only 1 to 14. Try again.")
            except ValueError:
                print("Invalid input. Enter only a number between 1 and 14. Try again\n")
            except (EOFError, KeyboardInterrupt):
                print("\nInput terminated. Exiting program.")
                exit(1)

    
    for i in range(30):
        print(f"Round {i + 1}\n")
        for i in test.foundation_piles.values():
            print(i.top_card())
        tab = test.get_tableau_for_print()
        fp = test.get_foundation_piles()
        draw = test.check_stock_pile()
        
        print_card_table(tab, fp, draw)


        # WASTE PILE
        # print(test.card_deck.deck) 
        # print_waste_pile(pile=test.get_waste_pile(), display_number=3)
        print_waste_pile(pile=test.show_waste_pile())
        # print(test.show_stock_pile())
        
        print("\nPress 1: To build to the tableau from the waste pile.\nPress 2: To move one or more cards on the tableau.\n" \
                    "Press 3: To build to the foundation piles from the waste pile or tableau.\nPress 4: To move a card from the foundation pile.\n" \
                    "Press 5: To draw from the stock pile to the waste pile.\nPress 6: To reset the stock pile.\n3")
        move = move_validator()
        if move == 1:
            stack_number = stack_validator()
            
            if test.build(stack_number):
                print("\nMove successful\n.")
                
            else:
                print("\nInvalid move")
                    
            input("Press ENTER or RETURN to Continue.")
        elif move == 2:
          
            print("\nFirst enter the stack you wish to move from: ")
            from_stack = stack_validator()

            print("\nNext, enter the stack you wish to move to: ")
            to_stack = stack_validator()
            
            print(f"\nNow, how many cards you wish to move from stack {from_stack + 1} to stack {to_stack + 1}: ")
            number_of_cards = number_of_cards_validator()
                     
            if test.transfer(from_stack, to_stack, number_of_cards):
                print("\nMove successful\n")
                print(input("Press Enter or Return to Continue."))
            else:
                print("\nInvalid move")
                print(input("Press Enter or Return to Continue."))
        elif move == 3:
            while True:
                location = int(input("Press 1: To move a card from waste pile.\nPress 2: To move from the tableau.\nEnter your response: "))
                if location not in {1,2}:
                    print("\nInvalid entry. Try again.\n")
                else:
                    break
            if location == 1:

                if test.move_to_foundation():
                    print("\nMove successful\n")
                    
                else:
                    print("\nInvalid move.")
                          
            elif location == 2:
                column = stack_validator()
                if test.move_to_foundation(column, True):
                    print("\nMove successful\n")

                else:
                    print("Invalid move")
            input("Press ENTER or RETURN to Continue.")  
        elif move == 4:
            try:
                print("\nSelect the foundation pile you wish to take from to return to the tableau.\n")
                suit = suit_validator()
                print("\nNow, enter the stack you wish to move to: ")
                stack_number = stack_validator()
                if test.move_from_foundation(suit=suit, stack_number=stack_number):
                    print("\nMove successful\n") 
                else:
                    print("\nInvalid move.")
            except EmptyFoundationPileError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")              
        elif move == 5:
            try:
                if test.draw():
                    print("\nMove successful\n")             
            except EmptyDrawPileError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")
            
        if test.check_win():
            print("You Win!")

        clear_screen()    



# Solitaire Testing
def main():
    run_game()
    exit()
#     test = Solitare()
#     # test.make_tableau()
#     test.show_tableau()
#     # print(test.card_deck.size)
#     # test.make_foundation_piles()
#     test.show_foundation_piles()
#     # test.make_draw_pile()
#     test.show_stock_pile()
#     # print(test.card_deck.size)
#     test_card = test.get_tableau()[0].remove_from()
#     print(test_card)
#     print(test_card.value)
#     print(test_card.visible)
#     print(test_card.suit)
#     print(test_card.is_black)
#     exit()
    
# def main():
#     ConnectFourCLI.run()
#     # run_game()
#     exit()
#     print_menu_screen()
#     valid_game_options  = GameOptions.values()
#     choice = menu_select(valid_game_options)
    
#     if choice == GameOptions.TIC_TAC_TOE.value:
#         TicTacToeCLI.run()
#     elif choice == GameOptions.CONNECT_FOUR.value:
#         ConnectFourCLI.run()
#     elif choice == GameOptions.SOLITAIRE.value:
#         run_game()
#     else:
#         raise ValueError("Invalid choice. See you next time.")
#     exit()

if __name__ == '__main__':
    main()

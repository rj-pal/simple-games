from cli import TicTacToeCLI, ConnectFourCLI
from games.game import Solitare, ConnectFour, TicTacToe
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
    tableau_lists = [card_stack.to_list()[::-1] for card_stack in tableau]
    max_height = max(len(stack) for stack in tableau_lists)
    
    # Ensure each stack is padded with properly spaced empty strings
    max_card_length = max(len(card) for stack in tableau_lists for card in stack)
    print(max_card_length)
    padded_tableau = [stack + [" "] * (max_height - len(stack)) for stack in tableau_lists]
    # padded_tableau.insert(0, ["Stack 1", "Stack 2", "Stack 3", "Stack 4", "Stack 5", "Stack 6", "Stack 7"])
   
    

    for row in zip(*padded_tableau):
        # print("  ".join(card.ljust(15) if card else " " * 15 for card in row))
        print("  ".join(card.center(15) if card else " " * 15 for card in row))
        
        # print(" ".join(card.rjust(max_card_length) for card in row))


def print_foundation_piles(piles):
    top_cards = [card_stack.peek() if card_stack.is_empty() else card_stack.peek().face for card_stack in piles.values()]
    # top_cards = [card_stack.peek() if card_stack.is_empty() else card_stack.peek().face for card_stack in piles]
    print(" | ".join(top_cards))

def print_draw_pile(pile):
    print(pile.peek())

def print_card_table(tableau, piles, pile):
    print_foundation_piles(piles)
    print()
    print_tableau(tableau)
    print()
    print_draw_pile(pile)

def run_game():
    test = Solitare()
    # print(test.size)
    # exit()
    def stack_validator():
        while True:
            position = int(input("Enter the card stack number: ")) - 1
            if position in range(7):
                return position
            print("Invalid entry. Enter only 1 to 7. Try again.\n")

    
    for _ in range(15):
        tab = test.get_tableau()
        fp = test.get_foundation_piles()
        draw = test.get_stock_pile()
        # test.show_foundation_piles()
        # print(tab)
        # print(fp)
        print_card_table(tab, fp, draw)
        
        print()
        move = int(input("\nPress 1: To build to the tableau.\nPress 2: To build to the foundation piles.\n" \
                         "Press 3: To turn top card from the stock pile to the waste pile.\nPress 4: To move stock to tableau\nEnter your response: "))
        if move == 1:
            stack_number = stack_validator()
            
            if test.build(stack_number):
                print("Move successful")
                
            else:
                print("Invalid move")
                    
            # test.flip_card_draw_pile()
            input("ENTER to Continue")
        elif move == 2:
            while True:
                location = int(input("Press 1 to move a card from stock pile or press 2 to move from the tableau: "))
                if location not in {1,2}:
                    print("Invalid entry. Try again.\n")
                else:
                    break
            if location == 1:

                if test.move_to_foundation():
                    print("Move successful")
                    draw.head.next.value.flip_card()
                    
                else:
                    print("Invalid move.")
                          
            elif location == 2:
                column = stack_validator()
                if test.move_to_foundation(column, False):
                    print("Move successful")
                    test.flip_card_tableau(column)
                    # draw.head.next.value.flip_card()
                else:
                    print("Invalid move")
            input("ENTER to Continue")
                       
        elif move == 3:
            if test.draw():
                test.flip_card_draw_pile()
                
                input("ENTER to Continue")
            else:
                print("ERROR OCCURRED")
            

        elif move == 4:
            print("\nFirst enter the stack you wish to move from.")
            from_stack = stack_validator()

            print("\nNext, enter the stack you wish to move to.")
            to_stack = stack_validator()
            
            print(f"Now, how many cards you wish to move from stack {from_stack + 1} to stack {to_stack + 1}.")
            while True:
                number_of_cards = int(input())
                if number_of_cards in range(1, 15):
                    break
                print("There are only 14 cards possible in a stack. Please enter only 1 to 14.")
            
            if test.transfer(from_stack, to_stack, number_of_cards):
                print("Move successful")
                print(input("Press Enter to Continue."))
                # draw.head.next.value.flip_card()
            else:
                print("Invalid move")

        clear_screen()    



# Solitaire Testing
def main():
    run_game()
    exit()
    test = Solitare()
    # test.make_tableau()
    test.show_tableau()
    # print(test.card_deck.size)
    # test.make_foundation_piles()
    test.show_foundation_piles()
    # test.make_draw_pile()
    test.show_stock_pile()
    # print(test.card_deck.size)
    test_card = test.get_tableau()[0].pop()
    print(test_card)
    print(test_card.value)
    print(test_card.visible)
    print(test_card.suit)
    print(test_card.is_black)
    exit()
    
# def main():
#     # ConnectFourCLI.run()
#     run_game()
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

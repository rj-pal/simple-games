from cli import TicTacToeCLI, ConnectFourCLI, SolitaireCLI
from utils.game_options import GameOptions
from utils.clitools import print_menu_screen, menu_select
from utils.strings import SIMPLE_GAMES_START


import sys
import select

def clear_stdin_buffer():
    """Clears any pending input typed by the user before the prompt."""
    while select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.read(1)  # Read one character at a time until buffer is empty

 
def main():
    # SolitaireCLI.run()
    # exit()
    print_menu_screen() 
    clear_stdin_buffer()
    valid_game_options  = GameOptions.values()
    choice = menu_select(valid_game_options)
    
    if choice == GameOptions.TIC_TAC_TOE.value:
        TicTacToeCLI.run()
    elif choice == GameOptions.CONNECT_FOUR.value:
        ConnectFourCLI.run()
    elif choice == GameOptions.SOLITAIRE.value:
        SolitaireCLI.run()
    else:
        raise ValueError("Invalid choice. See you next time.")
    exit()

# import gc
# import sys

# def run_game():
#     clear_screen()
#     test = Solitare(klondike_value=3)
#     # print(test.size)
#     # exit()
    
#     for i in range(30):
#         print(f"Round {i + 1}\n")
#         for i in test.foundation_piles.values():
#             print(i.top_card())
#         for j in test.foundation_piles.keys():
#             print(j)
#         tab = test.get_tableau_for_print()
#         fp = test.get_foundation_piles()
#         draw = test.check_stock_pile()
        
#         print_card_table(tab, fp, draw)


#         # WASTE PILE
#         # print(test.card_deck.deck) 
#         # print_waste_pile(pile=test.get_waste_pile(), display_number=3)
#         print_waste_pile(pile=test.show_waste_pile())
#         # print(test.show_stock_pile())
        
#         print("\nPress 1: To build to the tableau from the waste pile.\nPress 2: To move one or more cards on the tableau.\n" \
#                     "Press 3: To build to the foundation piles from the waste pile or tableau.\nPress 4: To move a card from the foundation pile.\n" \
#                     "Press 5: To draw from the stock pile to the waste pile.\nPress 6: To reset the stock pile.\n")
#         move = move_validator()
#         if move == 1:
#             try:
#                 stack_number = stack_validator()
                    
#                 if test.build(stack_number):
#                     print("\nMove successful\n")
                    
#                 else:
#                     print("\nInvalid move")
#             except GameError as e:
#                 print(f"\n{e}\n")
#             input("Press ENTER or RETURN to Continue.")
#         elif move == 2:
#             try:          
#                 print("\nFirst enter the stack you wish to move from: ")
#                 from_stack = stack_validator()

#                 print("\nNext, enter the stack you wish to move to: ")
#                 to_stack = stack_validator()
                
#                 print(f"\nNow, how many cards you wish to move from stack {from_stack + 1} to stack {to_stack + 1}: ")
#                 number_of_cards = number_of_cards_validator()
                        
#                 if test.transfer(from_stack, to_stack, number_of_cards):
#                     print("\nMove successful\n")
#                 else:
#                     print("\nInvalid move")
#                     print(input("Press Enter or Return to Continue."))
#             except GameError as e:
#                 print(f"\n{e}\n")
#             input("Press ENTER or RETURN to Continue.")
        
#         elif move == 3:
#             try:
#                 while True:
#                     location = int(input("\nPress 1: To move a card from waste pile.\nPress 2: To move from the tableau.\n\nEnter your response: "))
#                     if location not in {1,2}:
#                         print("\nInvalid entry. Try again.\n")
#                     else:
#                         break
#                 if location == 1:

#                     if test.move_to_foundation("waste_pile"):
#                         print("\nMove successful\n")      
#                     else:
#                         print("\nInvalid move.")
                            
#                 elif location == 2:
#                     column = stack_validator()
#                     if test.move_to_foundation("tableau", column):
#                         print("\nMove successful\n")
#                     else:
#                         print("Invalid move")
#             except GameError as e:
#                 print(f"\n{e}\n") 
#             input("Press ENTER or RETURN to Continue.")  
#         elif move == 4:
#             # test.move_from_foundation(suit="H", stack_number=-9)
#             try:
#                 print("\nSelect the foundation pile you wish to take from to return to the tableau.\n")
#                 suit = suit_validator()
#                 print("\nNow, enter the stack you wish to move to: ")
#                 stack_number = stack_validator()
#                 if test.move_from_foundation(suit=suit, stack_number=stack_number):
#                     print("\nMove successful\n") 
#                 else:
#                     print("\nInvalid move.")
#             except GameError as e:
#                 print(f"\n{e}\n")
#             input("Press ENTER or RETURN to Continue.")              
#         elif move == 5:
#             try:
#                 if test.draw():
#                     print("\nMove successful\n")             
#             except GameError as e:
#                 print(f"\n{e}\n")
#             input("Press ENTER or RETURN to Continue.")
#         elif move == 6:

#             if test.reset_pile():
#                 print("\nMove successful\n")
            
#             input("Press ENTER or RETURN to Continue.")
            
#         if test.check_win():
#             print("You Win!")

#         print(sys.getrefcount(test))  # Curious about Garbage Collection 
#         referrers = gc.get_referrers(test)
#         print(f"Found {len(referrers)} referrers")
#         for r in referrers:
#             print(type(r), r)

#         print("Who refers to test.draw_pile?")
#         referrers = gc.get_referrers(test.draw_pile)

#         for r in referrers:
#             print(f"Type: {type(r)}")
#             if isinstance(r, dict):
#                 # Most referrers are internal dictionaries like __dict__ or locals
#                 for k, v in r.items():
#                     if v is main.object_a:
#                         print(f" - Key: {k}")


# def main():
    # run_game()
    # exit()
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

if __name__ == '__main__':
    main()

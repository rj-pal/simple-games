"""
SolitaireCLI.py 
Author: Robert Pal
Updated: 2025-08-21

This module contains all control flow logic for running the Solitaire Command Line Application.

This game is still in development.
"""

from games.solitaire import Solitare
import utils.clitools.console as GameCLI
from utils.clitools.printing import print_card_table, print_start_game
from utils.clitools.prompting import select_klondike_draw_number
# from utils.clitools.clitools import print_card_table
from utils.errors import *

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
            if move in {1, 2, 3, 4, 5, 6}:
                return move
            else:
                print(
                    "Invalid move option. Please enter a number between 1 and 6. Try again.\n"
                )
        except ValueError:
            print(
                "Invalid input. Enter only a number between 1 and 6. Try again\n"
            )
        except (EOFError, KeyboardInterrupt):
            print("\nInput terminated. Exiting program.")
            exit(1)


def suit_validator():
    suit_dictionary = {1: "S", 2: "H", 3: "D", 4: "C"}
    while True:
        try:
            suit = int(
                input(
                    "Press 1: for Spade, 2 for Heart, 3 for Diamond, 4 for Club: "
                ))
            if suit in {1, 2, 3, 4, 5}:
                return suit_dictionary[suit]
            else:
                print(
                    "Invalid suit option. Please enter a number between 1 and 4 to get the correct foundation pile. Try again.\n"
                )
        except ValueError:
            print(
                "Invalid input. Enter only a number between 1 and 4. Try again\n"
            )
        except (EOFError, KeyboardInterrupt):
            print("\nInput terminated. Exiting program.")
            exit(1)


def number_of_cards_validator():
    while True:
        try:
            number_of_cards = int(
                input("Enter how many cards you wish to transfer: "))
            if number_of_cards in range(1, 15):
                return number_of_cards
            print(
                "There are only 14 cards possible in a stack. Please enter only 1 to 14. Try again."
            )
        except ValueError:
            print(
                "Invalid input. Enter only a number between 1 and 14. Try again\n"
            )
        except (EOFError, KeyboardInterrupt):
            print("\nInput terminated. Exiting program.")
            exit(1)


def play_game(test):

    for i in range(30):
        print(f"Round {i + 1}\n")

        tab = test.get_tableau_for_print()
        fp = test.get_foundation_piles()
        draw = test.check_stock_pile()
        waste = test.show_waste_pile()
        # print(type(tab))
        # print(type(fp))
        # print(type(draw))
        # print(type(waste))

        print_card_table(tab, fp, draw, waste)
        # test.show_stock_pile()

        print("\nPress 1: To build to the tableau from the draw pile.\nPress 2: To move one or more cards on the tableau.\n" \
                    "Press 3: To build to the foundation piles from the draw pile or tableau.\nPress 4: To move a card from the foundation pile.\n" \
                    "Press 5: To draw from the draw pile.\nPress 6: To reset the draw pile.\n")
        move = move_validator()
        if move == 1:
            try:
                stack_number = stack_validator()

                if test.build(stack_number):
                    print("\nMove successful\n")

                else:
                    print("\nInvalid move")
            except GameError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")
        elif move == 2:
            try:
                print("\nFirst enter the stack you wish to move from: ")
                from_stack = stack_validator()

                print("\nNext, enter the stack you wish to move to: ")
                to_stack = stack_validator()

                print(
                    f"\nNow, how many cards you wish to move from stack {from_stack + 1} to stack {to_stack + 1}: "
                )
                number_of_cards = number_of_cards_validator()

                if test.transfer(from_stack, to_stack, number_of_cards):
                    print("\nMove successful\n")
                else:
                    print("\nInvalid move")
                    print(input("Press Enter or Return to Continue."))
            except GameError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")

        elif move == 3:
            try:
                while True:
                    location = int(
                        input(
                            "\nPress 1: To move a card from waste pile.\nPress 2: To move from the tableau.\n\nEnter your response: "
                        ))
                    if location not in {1, 2}:
                        print("\nInvalid entry. Try again.\n")
                    else:
                        break
                if location == 1:

                    if test.move_to_foundation("waste_pile"):
                        print("\nMove successful\n")
                    else:
                        print("\nInvalid move.")

                elif location == 2:
                    column = stack_validator()
                    if test.move_to_foundation("tableau", column):
                        print("\nMove successful\n")
                    else:
                        print("Invalid move")
            except GameError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")
        elif move == 4:
            # test.move_from_foundation(suit="H", stack_number=-9)
            try:
                print(
                    "\nSelect the foundation pile you wish to take from to return to the tableau.\n"
                )
                suit = suit_validator()
                print("\nNow, enter the stack you wish to move to: ")
                stack_number = stack_validator()
                if test.move_from_foundation(suit=suit,
                                             stack_number=stack_number):
                    print("\nMove successful\n")
                else:
                    print("\nInvalid move.")
            except GameError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")
        elif move == 5:
            try:
                if test.draw():
                    print("\nMove successful\n")
            except GameError as e:
                print(f"\n{e}\n")
            input("Press ENTER or RETURN to Continue.")
        elif move == 6:

            if test.reset_pile():
                print("\nMove successful\n")

            input("Press ENTER or RETURN to Continue.")

        if test.check_win():
            print("You Win!")

        GameCLI.clear_screen()


def set_up_game():

    klondike_value = select_klondike_draw_number()
    game = Solitare(klondike_value=klondike_value)

    return game


def run():
    GameCLI.set_console_window_size(120, 50)  # console dimensions: width, height
    print_start_game('Solitaire')
    game = set_up_game()
    play_game(game)

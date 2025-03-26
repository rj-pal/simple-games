from cli import TicTacToeCLI, ConnectFourCLI
from games.game import Solitare, ConnectFour
from utils.game_options import GameOptions
from utils.clitools import clear_screen, delay_effect, print_menu_screen, menu_select
from utils.strings import SIMPLE_GAMES_START
from core.board import LineChecker
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
   
    

    for row in zip(*padded_tableau):
        # print("  ".join(card.ljust(15) if card else " " * 15 for card in row))
        print("  ".join(card.center(15) if card else " " * 15 for card in row))
        
        # print(" ".join(card.rjust(max_card_length) for card in row))


def print_foundation_piles(piles):
    top_cards = [card_stack.peek() if card_stack.is_empty() else card_stack.peek().face for card_stack in piles]
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
    for _ in range(15):
        tab = test.get_tableau()
        fp = test.get_foundation_piles()
        draw = test.get_stock_pile()[0]
        print_card_table(tab, fp, draw)
        print()
        move = int(input("\nPress 1 to build\nPress 2 to move an Ace to a foundation pile\nPress 3 to draw\nPress 4 to move stock to tableau\nEnter your response: "))
        if move == 1:
            while True:
                position = int(input("Enter the card stack number: "))
                if position in range(9):
                    break
                print("Invalid entry. Try again.\n")

           
            card = draw.pop()
            # print(type(card))
            if test.build(position, card):
                print("Move successful")
                
            else:
                print("Invalid move")
                draw.push(card)
                # test.card_deck.add_card(card)
                    
            draw.head.next.value.flip_card()
            input("ENTER to Continue")
        elif move == 2:
            while True:
                location = int(input("Press 1 to move from stock pile or press 2 to move from the board: "))
                if location not in {1,2}:
                    print("Invalid entry. Try again.\n")
                else:
                    break
            if location == 1:
                if draw.peek().value != 1:
                    print("Cannot move a card that is not an Ace")
                    break
               
                card = draw.pop()
                if test.move_to_foundation(card):
                    print("Move successful")
                    draw.head.next.value.flip_card()
                # test.show_foundation_piles()
                    input("ENTER to Continue")
                else:
                    print("Invalid move")
                    test.draw.push(card)
                          
            elif location == 2:
                column = int(input("Enter the column of the card where there is an Ace: "))
                ### NEEDS VALIDATION
                if test.get_tableau()[column].peek().value != 1:
                    print("Cannot move a card that is not an Ace")
                    break
                card = test.get_tableau()[column].pop()
                if test.move_to_foundation(card):
                    print("Move successful")
                    test.get_tableau()[column].head.next.value.flip_card()
                # test.show_foundation_piles()
                    input("ENTER to Continue")
                else:
                    print("Invalid move")
                    test.get_tableau()[column].push(card)
                
                # draw.head.next.value.flip_card()

            
            
        elif move == 3:
            test.card_deck.add_card(draw.pop())
            draw.head.next.value.flip_card()
            input("ENTER to Continue")

        elif move == 4:
            from_stack = int(input("Move card from stack number: "))
            to_stack = int(input("Move card from stack number: "))
            if test.transfer(from_stack, to_stack):
                print("Move successful")
                # draw.head.next.value.flip_card()
            else:
                print("Invalid move")



        clear_screen()    




# def main():

    # test = ConnectFour()
    # print(test.columns)
    # test.create_ai_player(True)

    # # print(test.players[0])
    # player = test.players[1]

    # print(player.move())
    # exit()


    # run_game()
    # exit()

    # test = Solitare()
    # # test.make_tableau()
    # test.show_tableau()
    # # print(test.card_deck.size)
    # # test.make_foundation_piles()
    # test.show_foundation_piles()
    # # test.make_draw_pile()
    # test.show_draw_disard_piles()
    # # print(test.card_deck.size)
    # exit()


    # print_menu_screen()
    # choice = menu_select({'1', '2', '3'})
    # if choice == '1':
    #     TicTacToeCLI.run()
    # elif choice == '2':
    #     ConnectFourCLI.run()
    # elif choice == '3':
    #     run_game()
    # else:
    #     raise ValueError("Invalid choice. See you next time.")
    
def main():
    test = ConnectFour()

    test.make_move(0,"r")
    test.make_move(1,"y")
    test.make_move(2,"y")
    test.make_move(3,"y")
    test.make_move(4,"r")
    test.make_move(5,"r")
    test.make_move(6,"y")
    # test.make_move(0,"r")
    # test.make_move(1,"r")
    test.make_move(2,"r")
    test.make_move(3,"r")
    test.make_move(4,"r")
    # test.make_move(5,"r")
    # test.make_move(6,"r")
    print(test.board)
    # print(test.board.get_diagonals(7, 'right'))
    print(test.check_winner())
    line = LineChecker(test.board)
    last_row = test.board.get_rows()[-2]
    print(last_row)
    print(line.two_blanks(last_row, "r", 2))
    # print(test._win.check_rows(4))
    
    exit()


    ConnectFourCLI.run()
    exit()

    print_menu_screen()
    valid_game_options  = GameOptions.values()
    choice = menu_select(valid_game_options)
    
    if choice == GameOptions.TIC_TAC_TOE.value:
        TicTacToeCLI.run()
    elif choice == GameOptions.CONNECT_FOUR.value:
        ConnectFourCLI.run()
    elif choice == GameOptions.SOLITAIRE.value:
        run_game()
    else:
        raise ValueError("Invalid choice. See you next time.")


if __name__ == '__main__':
    main()

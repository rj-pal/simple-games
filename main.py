from cli import TicTacToeCLI, ConnectFourCLI
from games.Game import Deck, Solitare

def main():

    # deck = Deck()
    # print(deck.deck)
    test = Solitare()
    test.make_tableau()
    test.show_tableau()
    print(test.card_deck.size)
    exit()


    print(test.game_board)
    print(test.card_deck)
    test.card_deck.shuffle_deck()
    print(test.card_deck.get_deck())
    print(test.card_deck.deal_cards())
    print(test.card_deck.get_size())
    exit()

    print("Select a game:")
    print("1. Tic Tac Toe")
    print("2. Connect 4")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        TicTacToeCLI.run()
    elif choice == '2':
        ConnectFourCLI.run()
    else:
        print("Invalid choice. See you next time.")

if __name__ == '__main__':
    main()

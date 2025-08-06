"""
solitaire.py 
Author: Robert Pal
Updated: 2025-08-06

This module contains code for solitaire.
"""

from core.deck import Card, CardDeck, CardStack
from utils.errors import EmptyPileError, InvalidMoveError, InvalidStackError

class Solitare:

    def __init__(self, size: int=7, klondike_value: int=3):
        self._size = size
        self._klondike_value = klondike_value
        self.card_deck = CardDeck() # Used for dealing initial cards and as the waste pile
        self.tableau = self.make_tableau()
        self.foundation_piles = self.make_foundation_piles()
        self.draw_pile = self.make_draw_pile()
        self.waste_pile = self.make_waste_pile()

    @property
    def size(self):
        """Size is the number of columns on tableau for buidling game play."""
        return self._size

    @size.setter
    def size(self, value):
        if value not in {6, 7, 8, 9, 10}:
            raise ValueError("The size must be from 6 to 10 to determine he number of columns in play on the tableau.")
        self._size = value

    @property
    def klondike_value(self):
        """Klondike value to determine if the draw is 1 or 3."""
        return self._klondike_value

    @klondike_value.setter
    def klondike_value(self, value):
        if value not in {1, 3}:
            raise ValueError("Klondike value must be either 1 or 3 to determine the number of cards per draw.")
        self._klondike_value = value

    ### IS IT NECESSARY?
    @klondike_value.deleter
    def klondike_value(self):
        raise AttributeError("Cannot delete the klondike_value attribute")

    def reset_pile(self):
        if not self.draw_pile.is_empty():
            raise InvalidMoveError("Cannot reset the stock pile that is not empty.")
        number_of_waste_cards = self.waste_pile.size
        print(self.waste_pile)
        while not self.waste_pile.is_empty():
            waste_card = self.waste_pile.remove_from(flip=True)
            self.card_deck.add_card(waste_card)
        for card in self.card_deck.deck:
            print(card)
        temp_stack = self.card_deck.get_empty_card_stack()
        for i in range(number_of_waste_cards):
            bottom_card = self.card_deck.get_first_card()
            temp_stack.add_to(bottom_card)
        self.draw_pile = temp_stack
        return True

    def check_move(self, from_card: Card, to_card: Card):
        """Validates building to a tabelau stack in descending order and alternatie suit colour cards."""
        # check king move to empty stack
        if to_card is None:
            return from_card.value == 13
        # check all other possible moves
        return (to_card.is_black != from_card.is_black) and (to_card.value == from_card.value + 1)

    def check_foundation_move(self, card: Card):
        """Validates buidling to a foundation pile in ascending order and same suit card."""
        # suit validation checked before calling this function
        foundation_pile = self.foundation_piles[card.suit]
        if foundation_pile.is_empty():
            return card.value == 1
        return card.value == foundation_pile.top_card().value + 1

    def move_card(self, from_card_stack: CardStack, to_card_stack: CardStack, flip_card: bool=False):
        """Moves a single card from one card stack to another. Valid Card Stacks: tabelau, foundation pile, draw pile, or waste pile."""
        card = from_card_stack.remove_from(flip_card)
        to_card_stack.add_to(card)
        return True

    def check_win(self):
        return all(pile.size == 13 for pile in self.foundation_piles.values())

    def draw(self):
        """Draw a card from the stock pile and flip it over for move."""
        cards_drawn_for_play = 0
        for _ in range(self._klondike_value):
            try:
                self.move_card(from_card_stack=self.draw_pile, to_card_stack=self.waste_pile, flip_card=True)
                # card_for_play = self.draw_pile.remove_from(flip=True)         
                # self.waste_pile.add_to(card_for_play)
                cards_drawn_for_play += 1
            except EmptyPileError:
                break
        if cards_drawn_for_play == 0:
            raise EmptyPileError("The draw pile is empty. There are no cards to draw from.")

        return True

    def move_to_foundation(self, from_pile: str, stack_number: int=-1):
        """Move a card from the waste pile or tableau to the foundation pile of the selected card's suit. Defaults to move from waste pile."""
        # Get the pile the player is trying to move from
        if from_pile == "tableau":
            if not 0 <= stack_number < self._size:
                raise InvalidStackError(f"Invalid tableau stack number: {stack_number}")
            from_card_stack = self.tableau[stack_number]
        elif from_pile == "waste_pile":
            from_card_stack = self.waste_pile
        else:
            raise ValueError("Invalid 'from_pile' argument. Must be either 'tableau' or 'waste_pile'.")

        # Check that the card is not from an empty pile before checking the move to the foundation
        card = from_card_stack.top_card()
        if card is None:
            raise EmptyPileError("You are attempting to move a card from an empty card pile.")
        # Validate move to the foundation pile
        if not self.check_foundation_move(card):
            raise InvalidMoveError("The card you want to move cannot be put onto the foundation pile.")
        # Move the card
        self.move_card(from_card_stack=from_card_stack, to_card_stack=self.foundation_piles[card.suit])
        if from_pile == "tableau" and not from_card_stack.is_empty():
            if not from_card_stack.top_card().visible:
                self.flip_card_tableau(stack_number)
        return True

    def move_from_foundation(self, suit: str, stack_number: int):
        if suit not in self.foundation_piles.keys():
            raise ValueError(f"Invalid suit: {suit}") # Or a custom InvalidSuitError
        if not 0 <= stack_number < self._size:
            raise InvalidStackError(f"Invalid tableau stack number: {stack_number}")

        from_card = self.foundation_piles[suit].top_card()
        if from_card is None:
            raise EmptyPileError(f"Cannot move from empty {suit} foundation pile.")
        if from_card.value == 13:
            raise InvalidMoveError("Cannot move a King back to the tableau.")

        to_card = self.tableau[stack_number].top_card()
        if not self.check_move(from_card, to_card):
            raise InvalidMoveError(f"Cannot move {from_card} from foundation to tableau stack {stack_number}.")

        return self.move_card(from_card_stack=self.foundation_piles[suit], to_card_stack=self.tableau[stack_number])

    def get_tableau_card(self, stack_number):
        """Returns the top card of the requested tableau stack or None if the stack is empty."""
        if self.tableau[stack_number].is_empty():
            return None
        else:
           return self.tableau[stack_number].top_card()

    def build(self, stack_number):
        # No building from an empty waste
        card_to_move = self.waste_pile.top_card()
        if card_to_move is None:
            raise EmptyPileError("Cannot build from empty waste pile.")
        if not 0 <= stack_number < self._size:
            raise InvalidStackError(f"Invalid tableau stack number: {stack_number}")
        # Validate move first
        if not self.check_move(from_card=card_to_move, to_card=self.tableau[stack_number].top_card()):
            raise InvalidMoveError(f"Cannot build {card_to_move.name} on tableau stack {stack_number}.")
        return self.move_card(from_card_stack=self.waste_pile, to_card_stack=self.tableau[stack_number])

    def transfer(self, from_stack, to_stack, number_of_cards=1):
        if not 0 <= from_stack < self.size:
            raise InvalidStackError(f"Invalid tableau stack number for origin: {from_stack}")
        if not 0 <= to_stack < self.size:
            raise InvalidStackError(f"Invalid tableau stack number for destination: {to_stack}")
        if number_of_cards <= 0:
            raise InvalidMoveError(f"Invalid number of cards (cannot be negative): {number_of_cards}.")

        from_card_stack = self.tableau[from_stack]
        if from_card_stack.is_empty():
            raise EmptyPileError("Cannot move from empty tableau stack.")

        if from_card_stack.size < number_of_cards:
            raise InvalidMoveError(f"Cannot transfer {number_of_cards} cards. Stack {from_stack + 1} only has {from_card_stack.size} cards.")

        # Double check all cards in the transfer stack are visible or face up
        for i in range(number_of_cards - 1):
            card_for_transfer = from_card_stack.look_at(i)
            if not card_for_transfer.visible:
                raise InvalidMoveError(f"The card at position {i + 1} is face down. All cards to be transfered must be face up.")

        # Check if the final card is face up and keep its value for transfer validation
        from_card = from_card_stack.look_at(number_of_cards - 1) # for 0-indexed 
        if not from_card.visible:
            raise InvalidMoveError(f"The card you selected for transfer to another stack is face down.")

        # Validate move before moving cards between stacks             
        if not self.check_move(from_card=from_card, to_card=self.tableau[to_stack].top_card()):
            raise InvalidMoveError(f"The card or cards you wish to move from stack {from_stack} cannot be placed on stack {to_stack}.")

        # Create a temp card stack to move the cards from one tableau to another tableau card stack
        temp_stack = CardStack()
        for _ in range(number_of_cards):
            self.move_card(from_card_stack=from_card_stack, to_card_stack=temp_stack)
        while not temp_stack.is_empty():
            self.move_card(from_card_stack=temp_stack, to_card_stack=self.tableau[to_stack])

        # Flip the card in the tableau if necessary after moving all the cards. 
        if not from_card_stack.is_empty() and not from_card_stack.top_card().visible:
            self.flip_card_tableau(from_stack)

        return True

    def make_tableau(self):
        tableau = []
        self.card_deck.shuffle_deck()
        for i in range(self.size):
            card_stack = self.card_deck.deal_cards(number_of_cards=i + 1)
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

    def make_waste_pile(self):
        return self.card_deck.get_empty_card_stack()


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

    # def check_tableau(self, number):
    #     if number < 0 < self._size:
    #         raise IndexError()
    #     if self.tableau[number].is_empty():
    #         raise EmptyPileError

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
        if self.check_stock_pile():
            print(self.draw_pile.head.value.value)
        else:
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
        self.draw_pile.top_card().flip_card()
        return True

    def flip_card_tableau(self, stack_number):
        if not 0 <= stack_number < self._size:
            raise InvalidStackError(f"Invalid tableau stack number: {stack_number}")
        if self.tableau[stack_number].is_empty():
            return False
        self.tableau[stack_number].top_card().flip_card()
        return True
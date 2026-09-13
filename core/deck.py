"""
deck.py 
Author: Robert Pal
Updated: 2026-09-11

This module contains foundational code for `CardDeck`, a virtual deck of cards that mimics
the behavior of a physical deck of cards.

The primary user-facing class, `CardDeck`, acts as a master deck of cards using standard
or custom card objects (`StandardCard`, `CustomCard`). It utilizes two secondary data
structure classes: `CardQueue` and `CardStack`. These underlying structures represent
piles, hands, or decks, and manage all cards used during gameplay.

`CardDeck` interfaces using its `deck` attribute (a `CardQueue`) to support shuffling
and dealing cards from either end. Dealing hands or forming piles returns `CardStack`
objects, providing top-to-bottom card access via a linked list.
"""

from random import shuffle
from core.cards import StandardCard, CustomCard
from core.card_structures import CardQueue, CardStack

SUITS = ("S", "H", "D", "C")
VALUES = tuple(range(1, 14))

class CardDeck:
    """
    Represents a virtual deck of playing cards.

    Acts as a dealer's deck backed by a `CardQueue` structure. Supports creating
    standard 52-card decks or custom non-standard decks, shuffling, drawing, dealing
    hands, and moving cards into stacks or queues.

    Attributes:
        deck (CardQueue): The core data structure holding the active queue of card objects.
    """

    DECKTYPES = {"standard", "non_standard"}

    def __init__(self, deck_type="standard", suits=SUITS, values=VALUES):
        """
        Initialize a new instance of CardDeck.

        Args:
            deck_type (str, optional): Type of deck to create ('standard' or 'non_standard').
                Defaults to 'standard'.
            suits (iterable, optional): Sequence of suits for deck generation.
                Defaults to module-level `SUITS` for standard 52-card deck.
            values (iterable, optional): Sequence of values for deck generation.
                Defaults to module-level `VALUES` for standard 52-card deck.
        """
        self.deck_type = deck_type
        self._suits = suits
        self._values = values
        self.deck = self.create_deck()

    @property
    def deck_type(self):
        """str: The type of deck ('standard' or 'non_standard')."""
        return self._deck_type

    @deck_type.setter
    def deck_type(self, valid_deck_type):
        """
        Validate and set the deck type.

        Args:
            valid_deck_type (str): The deck type string to assign.

        Raises:
            ValueError: If `valid_deck_type` is not a string or not in `DECKTYPES`.
        """
        if isinstance(valid_deck_type, str):
            if valid_deck_type in self.DECKTYPES:
                self._deck_type = valid_deck_type
            else:
                raise ValueError("Only Deck Type standard or non_standard allowed")
        else:
            raise ValueError("Deck Type must be a string (standard or non_standard)")

    def create_deck(self):
        """
        Populate and return a new deck using the specified suits and values with default to 
        standard 52-card deck. Selects `StandardCard` for standard decks or `CustomCard` 
        for non-standard deck.

        Returns:
            CardQueue: The populated queue of cards.
        """
        deck = self.get_empty_card_queue()
        card_cls = StandardCard if self._deck_type == "standard" else CustomCard

        for suit in self._suits:
            for value in self._values:
                deck.add_to(card_cls(suit, value))

        return deck
    
    @property
    def size(self):
        """int: The current number of cards remaining in the deck."""
        return self.deck.size

    def is_empty(self):
        """
        Check whether the deck has no remaining cards.

        Returns:
            bool: True if the deck is empty, False otherwise.
        """
        return self.deck.is_empty()

    def show_deck(self):
        """Print the current string representation of the underlying card queue."""
        print(self.deck)

    def to_list(self):
        """
        Drain all cards from the deck queue into a standard Python list. Used for internal reordering.

        Returns:
            list: A list containing all card objects in front-to-back order starting at index 0 for front.
        """
        card_list = []
        while not self.deck.is_empty():
            card_list.append(self.deck.remove_from_front()) # remove each card into a list 
        return card_list

    def recreate_deck(self, deck_as_list):
        """
        Rebuild the internal deck queue from a list of card objects. Used for internal reordering.

        Args:
            deck_as_list (list): List of card objects to add into the deck.
        """
        deck = self.get_empty_card_queue()
        for card_data in deck_as_list:
            deck.add_to(card_data)
        self.deck = deck
    
    def shuffle_deck(self):
        """Randomly reorder all cards currently remaining in the deck."""
        temp_deck = self.to_list()
        shuffle(temp_deck)
        self.recreate_deck(temp_deck)

    def get_deck(self):
        """
        Retrieve the internal CardQueue object representing the deck.

        Returns:
            CardQueue: The internal deck structure.
        """
        return self.deck
    
    def get_empty_card_stack(self):
        """
        Factory method to create a new empty CardStack.

        Returns:
            CardStack: An empty card stack instance.
        """
        return CardStack()
    
    def get_empty_card_queue(self):
        """
        Factory method to create a new empty CardQueue.

        Returns:
            CardQueue: An empty card queue instance.
        """
        return CardQueue()
    
    def add_card(self, card):
        """
        Add a single card to the deck queue.

        Args:
            card: The card object to add.
        """
        self.deck.add_to(card)

    def remove_from(self, flip):
        """
        Remove the top node from the deck, optionally flipping the underlying card.

        Args:
            flip (bool): If True, triggers the card's `flip_card()` method.

        Returns:
            Node: The card node removed from the top of the queue.
        """
        card_node = self.deck.remove_from_top()
        if flip:
            card_node.value.flip_card()
        return card_node

    def deal_card(self, facedown=True):
        """
        Remove and return a single card from the front of the deck.

        Args:
            facedown (bool, optional): If True, sets the card's visibility to False.
                Defaults to True.

        Returns:
            Card or None: The dealt card object, or None if the deck is empty.
        """
        if self.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from_front()
        card.value.visible = not facedown # Set 'visibile' attribute to False to make the card facedown
        return card
    
    def deal_cards(self, number_of_cards=52, facedown=True):
        """
        Deal multiple cards from the deck into a CardStack.

        Simulates dealing a hand where the first card dealt ends up at the bottom
        and the last card dealt ends up at the top.

        Args:
            number_of_cards (int, optional): The maximum number of cards to deal.
                Defaults to 52.
            facedown (bool, optional): If True, sets card visibility to False.
                Defaults to True.

        Returns:
            CardStack: A stack containing the dealt cards.
        """
        card_stack = CardStack()
        for i in range(number_of_cards):
            if card := self.deal_card(facedown):
                card_stack.add_to(card)
            else:
                print("Dealing is finished.")
                break   
        return card_stack
    
    def deal(self, number_of_hands, number_of_cards=52, facedown=True, shuffle=False):
        """
        Deal a specified number of hands containing a given number of cards.

        Args:
            number_of_hands (int): The total number of hands to deal.
            number_of_cards (int, optional): Number of cards per hand. Defaults to 52.
            facedown (bool, optional): If True, cards in hands are dealt face down.
                Defaults to True.
            shuffle (bool, optional): If True, shuffles the deck prior to dealing.
                Defaults to False.

        Returns:
            list[CardStack]: A list of CardStack instances, each representing a hand.
        """
        if shuffle:
            self.shuffle_deck()
        hands = [self.deal_cards(number_of_cards, facedown) for _ in range(number_of_hands)]
        return hands

    def pile(self, facedown=True, card_pile_type="card_queue"):
        """
        Drain all remaining cards from the deck into a single pile structure.

        Args:
            facedown (bool, optional): If True, card visibility is set to False.
                Defaults to True.
            card_pile_type (str, optional): The target data structure, either
                'card_queue' or 'card_stack'. Defaults to "card_queue".

        Returns:
            CardQueue or CardStack: A pile structure populated with all remaining cards.

        Raises:
            TypeError: If `card_pile_type` is neither 'card_queue' nor 'card_stack'.
        """
        # The purpose of this function is to remove any remaining cards in the deck and pile them into one card pile
        if card_pile_type == "card_queue":
            card_pile = CardQueue()
        elif card_pile_type == "card_stack":
            card_pile = CardStack()
        else:
            raise TypeError
        
        while self.deck.size != 0:
            card = self.deck.remove_from_front()
            card.value.visible = not facedown
            card_pile.add_to(card)      
        return card_pile

    def get_last_card(self):
        """
        Remove and return a card from the front of the deck queue.

        Returns:
            Card or None: The removed card object, or None if the deck is empty.
        """
        if self.deck.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from_front()
        return card
    
    def get_first_card(self):
        """
        Remove and return card data using the deck's card data removal interface.

        Returns:
            Card or None: The retrieved card data, or None if the deck is empty.
        """
        if self.deck.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from(return_type="card_data")
        return card

if __name__=="__main__":
    # CARD QUEUE TESTING
    q = CardQueue()
    print(q)
    c = q.get_card_in_play()
    print(repr(c))
    print(c)
    print(c.value)

    s = CardStack()
    print(s)
    c = s.get_card_in_play()
    print(c)
    exit()
    # q.add_to(Card("S", 4))
    # q.add_to(Card("H", 0))
    # q.add_to(Card("H", 12))
    # q.add_to(Card("S", 11))
    # q.add_to(Card("D", 8))
    # # q.add_to("Three")
    # print(q)
    # exit()
    # print(q.size)
    # r = q.remove_from()
    # print(r)
    # q.remove_from()
    # # print("TAIl")
    # # print(q.tail)
    # d = q.remove_from_top()
    # # print(d.look_card())
    # print(d)
    # # print(q)
    # # # q.remove_from_top()
    # print(q)
    # exit()

    # CARD DECK TESTING
    deck = CardDeck()
    print(deck.deal_card())
    print(deck.deal_cards(3, False))
    hands = deck.deal(3, 4, True)
    for hand in hands:
        print(hand)
    exit()
    # deck.pile()
    # print(deck)
    # deck.show_deck()
    # # print(deck.to_list())
    # deck.shuffle_deck()
    # deck.show_deck()
    # exit()
    players = deck.deal(2, 6)
    print(deck.__str__())
    for p in players:
        tc = p.get_card_in_play()
        tc.flip_card()
        tc.visible = False
        print(tc)
        print(p)
    s1 = players[0]
    print(s1.suit)
    t1 =s1.get_card_in_play()
    t1.flip_card()
    print(t1)
    
    print(s1.to_list())
    print(s1)
    s1.suit = "H"
    print(s1.suit)
    for _ in range(s1.size):
        s1.remove_from()
    print(s1)
    # print(s1.suit)
    
    exit()
    
    # card = Card("S", 12)
    # print(card)
    # print(card.visible)
    # card.value = 8
    # card.visible = True
    # print(card)

    # exit()


    pile = CardStack()
    print(pile.head.value)
    print(pile.get_card_in_play())
    # pile.get_card_in_play().visible = True
    print(pile.get_card_in_play())

    exit()
        
        # pile.add_to(card)
        # print(pile.head.next.value)
        # # print(pile.get_card_in_play().next.next)
        # # print(pile.head)

        # hands = CardDeck().deal(number_of_players=5, number_of_cards=15, shuffle=True)
        # print(hands)

        # for i, hand in enumerate(hands, start=1):
        #     print(f"Player {i}'s hand: {hand.__str__()}")
        # exit()




    #     deck = CardDeck()
    #     queue = deck.pile()
    #     print(queue)
    #     for i in range(50):
    #         queue.remove_from()
    #     print(queue)
    #     exit()


        
    #     stack = deck.deal_cards(13, True)
    #     stack1 = deck.deal_cards(13, True)
    #     stack2 = deck.deal_cards(20, True)
    #     print(stack2.get_card_in_play())
    #     print(f"Stack 2: {stack2}, size {stack2.size}")
    #     stack3 = deck.deal_cards(13, True)
    #     stack4 = deck.deal_cards(13)
    #     # print(f"Stack: {stack}")
    #     # print(f"Stack: {stack1}")
    #     # print(f"Stack: {stack2}, size {stack2.size}")
    #     print(f"Stack 3: {stack3}, size {stack3.size}")
    #     print(f"Stack 4: {stack4}")

    #     # for _ in range(1, 6):
    #     #     top_value = stack.remove_from()
    #     #     print(f"Pop: {top_value}") # variable name changed
    #     # print(f"Stack: {stack}")
    #     # print(stack.get_card_in_play())

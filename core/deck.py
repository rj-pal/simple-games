"""
deck.py 
Author: Robert Pal
Updated: 2026-08-30

This module contains foundational code for a card deck that mimicks the behaviour of a physical deck of cards.

The primary user-facing classes are CardDeck, a custom class that acts as a master deck of cards, and Card, a custom calss for a playing card.

The two secondary classes are CardQueue and CardStack, two classes that act as piles or decks of cards. These are used in the card deck to manage
cards that are used in play. 

CardDeck interfaces using a deck attribute, which is itself a CardQueue, to allow for shuffling and dealing card from either the top or bottom of 
the deck. When dealing hands of cards, or creating a pile of cards, the card deck will return CardStack objects, which act on the principle of access
to the cards through the top card, moving down to the bottom card. 

These two custom Card Objects are Linked Lists, which use a wrapper CardNode class for implementation.

The original intent of this data structure was to demonstrate implementations of a stacks and queues using a linked list and node design pattern.
"""

from random import shuffle
from utils.emojis import SUITS, FACES
from core.cards import StandardCard
from core.card_structures import *

Card = StandardCard


class CardDeck:
    STANDARDSUITS = ("S", "H", "D", "C")
    def __init__(self, deck_type="standard"):
        """
        Card Deck data structure acts like a dealer's deck. It's core object is a Card Queue that can deal cards into hands, and remove cards from
        either it's front or back side. from the front
        """
        self.deck_type = deck_type
        self.deck = self.create_deck()

    @property
    def deck_type(self):
        return self._deck_type

    @deck_type.setter
    def deck_type(self, new_deck_type):
        if isinstance(new_deck_type, str):
            if new_deck_type in {"standard", "non_standard"}:
                self._deck_type = new_deck_type
            else:
                raise ValueError("Only Deck Type standard or non_standard allowed")
        else:
            raise ValueError("Deck Type must be a string (standard or non_standard)")

    def create_deck(self):
        """Creates standard 52-card deck or returns empty deck for custom card decks (non-standard)"""
        deck = self.get_empty_card_queue()
        if self._deck_type == "standard":
            for suit in self.STANDARDSUITS:
                for value in range(1, 14):
                    deck.add_to(Card(suit, value))
        return deck     

    @property
    def size(self):
        return self.deck.size

    def is_empty(self):
        return self.deck.is_empty()

    def show_deck(self):
        print(self.deck)

    def to_list(self):
        """Stores the data of each card currently in the card queue"""
        card_list = []
        while not self.deck.is_empty():
            card_list.append(self.deck.remove_from_front()) # remove each card into a list 
        return card_list

    def recreate_deck(self, deck_as_list):
        deck = self.get_empty_card_queue()
        for card_data in deck_as_list:
            deck.add_to(card_data)
        self.deck = deck
    
    def shuffle_deck(self):
        temp_deck = self.to_list()
        shuffle(temp_deck)
        self.recreate_deck(temp_deck)

    def get_deck(self):
        return self.deck
    
    def get_empty_card_stack(self):
        return CardStack()
    
    def get_empty_card_queue(self):
        return CardQueue()
    
    def add_card(self, card):
        self.deck.add_to(card)

    def deal_card(self, facedown=True):
        """Removes a single card from the deck or deals a card"""
        if self.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from_front()
        card.value.visible = not facedown # Set 'visibile' attribute to False to make the card facedown
        return card
    
    def deal_cards(self, number_of_cards=52, facedown=True):
        """Removes muliptle cards from the deck and adds to a stack, or deals a hand of cards. Imitates dealing a hand of cards with the 
        first card dealt on the bottom and the last card on the top"""
        card_stack = CardStack()
        for i in range(number_of_cards):
            if card := self.deal_card(facedown):
                card_stack.add_to(card)
            else:
                print("Dealing is finished.")
                break   
        return card_stack
    
    def deal(self, number_of_hands, number_of_cards=52, facedown=True, shuffle=False):
        """Creates an array of hands by dealing the desired number of cards in a hand"""
        if shuffle:
            self.shuffle_deck()
        hands = [self.deal_cards(number_of_cards, facedown) for _ in range(number_of_hands)]
        return hands

    
    def pile(self, facedown=True):
        # The purpose of this function is to remove any remaining cards in the deck and pile them into one card pile
        # card_stack = CardStack()
        card_stack = CardQueue()
        while self.deck.size != 0:
            card = self.deck.remove_from_front()
            card.value.visible = not facedown
            card_stack.add_to(card)      
        return card_stack

    def remove_from(self, flip):
        card_node = self.deck.remove_from_top()
        if flip:
            card_node.value.flip_card()
        return card_node

    def get_last_card(self):
        if self.deck.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from_front()
        return card
    
    def get_first_card(self):
        if self.deck.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.remove_from(return_type="card_data")
        return card
    
    # def __str__(self):
    #     return str(f"This is a card deck with {self.size} card(s)")

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

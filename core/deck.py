"""
deck.py 
Author: Robert Pal
Updated: 2026-08-04

This module contains foundational code for a card deck that mimicks the behaviour of a physical deck of cards.

The original intent of this data structure was to implement and demonstrate implementations of a stack using a linked list and node.
"""

from random import shuffle
from collections import deque
# from utils.errors import EmptyPileError

# Python program to demonstrate
# stack implementation using a linked list.
# node class

class CardNode:
    
    def __init__(self, value):
        """Base wrapper node class for implementation of various deck of cards. Basic linked list data structure."""
        self.value = value
        self.next = None
        self.previous = None

# Currently in use for GUI in Solitaire software
SUITS = {
       "S": {"name": "Spades", "emoji": "♠️", "alt": "♠"},
       "H": {"name": "Hearts", "emoji": "❤️", "alt": "♥"},
       "D": {"name": "Diamonds", "emoji": "♦️", "alt": "♦"},
       "C": {"name": "Clubs", "emoji": "♣️", "alt": "♣"},
       "B": {"name": "Blank", "emoji": "🎴", "alt": "🂠"},
   }

FACES = {
        0: "Blank", 1: " A", 2: " 2", 3: " 3", 4: " 4", 5: " 5", 6: " 6", 
        7: " 7", 8: " 8", 9: " 9", 10: "10", 11: " J", 12: " Q", 13: " K"
    }

# Possible use in future GUI for Solitaire or other card game software
CARDS = {
            'A♠': '🂡', '2♠': '🂢', '3♠': '🂣', '4♠': '🂤', '5♠': '🂥', '6♠': '🂦', '7♠': '🂧',
            '8♠': '🂨', '9♠': '🂩', 'T♠': '🂪', 'J♠': '🂫', 'Q♠': '🂭', 'K♠': '🂮',
            'A♥': '🂱', '2♥': '🂲', '3♥': '🂳', '4♥': '🂴', '5♥': '🂵', '6♥': '🂶', '7♥': '🂷',
            '8♥': '🂸', '9♥': '🂹', 'T♥': '🂺', 'J♥': '🂻', 'Q♥': '🂽', 'K♥': '🂾',
            'A♦': '🃁', '2♦': '🃂', '3♦': '🃃', '4♦': '🃄', '5♦': '🃅', '6♦': '🃆', '7♦': '🃇',
            '8♦': '🃈', '9♦': '🃉', 'T♦': '🃊', 'J♦': '🃋', 'Q♦': '🃍', 'K♦': '🃎',
            'A♣': '🃑', '2♣': '🃒', '3♣': '🃓', '4♣': '🃔', '5♣': '🃕', '6♣': '🃖', '7♣': '🃗',
            '8♣': '🃘', '9♣': '🃙', 'T♣': '🃚', 'J♣': '🃛', 'Q♣': '🃝', 'K♣': '🃞'
        }

class Card:
    def __init__(self, suit: str, value: int):
        """Card data structure that is used in a Card Node."""
        self._suit = suit
        self._value = value 
        self._visible = False
        self.face = self.create_face()
        self.name = self.create_name()
        
    def create_face(self, faces: dict=FACES, suits: dict=SUITS, suit_type: str="emoji"):
        """Creates a physical card face based on the type of emoji"""   
        if self.value == 0:
            return suits[self.suit]["alt"]
        else:
            return f"{faces[self.value]} of {suits[self.suit][suit_type]}"
    
    def create_name(self):
        """Creates basic string name for each card."""
        suit_dict = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}
        name_dict = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
                        8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}
        
        return f"{name_dict[self.value]} of {suit_dict[self.suit]}" if self.value != 0 else "This is a place card."
    
    @property
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit
    
    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, new_visibility: bool):
        if isinstance(new_visibility, bool):
            self._visible = new_visibility
        else:
            raise ValueError("Visible must be a boolean value.")

    @property
    def is_black(self):
        return self.suit in {"S", "C"}
    
    def is_visible(self):
        return self.visible
    
    def look_card(self):
        return self.face
    
    def flip_card(self):
        self._visible = not self._visible

    def __repr__(self):
        return f"Suit: {self.suit}, Value: {self.value}, Visible: {self.visible}, Face: {self.face}"
    
    def __str__(self):
        if self.visible:
            return self.face
        return "Hidden"

class CardQueue:

    def __init__(self):
        """Card Queue data structure with Blank Card Head acting as dummy head. Implements a linked list with the principle of first in, first out."""
        self.head = CardNode(Card("B", 0)) # dummy head node is flipped blank card indicating a deck of cards exists
        self.head.value.flip_card()
        self.tail = self.head
        self._size = 0
    
    @property
    def size(self):
        """Returns the number of cards in the stack (read-only)."""
        return self._size 

    def is_empty(self):
        """Returns if the queue is empty or not."""
        return self._size == 0
    
    def __str__(self):
        """Prints a simple string representation of the CardQueue"""
        if self.is_empty():
            return self.head.value.face
        
        current_card = self.head.next
        card_queue = ""
        while current_card:
            card_queue += repr(current_card.value) + " ->\n"
            current_card = current_card.next
        return card_queue

    def add_to(self, value):
        """Pushes a new card node to the head of the queue."""
        if not isinstance(value, Card):
            raise TypeError("Only objects of Type Card() are allowed in Card Queue")
        card_node = CardNode(value)
        self.tail.next = card_node
        card_node.previous = self.tail
        self.tail = card_node
        self._size += 1

    def remove_from(self):
        """Removes the first card node from the queue. Returns the removed card."""
        if self.is_empty():
            raise Exception("Popping from an empty queue")
        remove_card = self.head.next
        self.head.next = remove_card.next
        remove_card.previous = None
        self._size -= 1
        return remove_card.value

    def remove_from_top(self):
        if self.is_empty():
            raise Exception("Popping from an empty queue")
        remove_card = self.tail
        
        remove_card.previous = None
        self.tail = remove_card.previous
        self.tail.next = None
       
        return remove_card.value

    
    def top_card(self):
        """Returns the head of the card queue"""
        if self.is_empty():
            return self.head.value
        return self.head.next.value


class CardStack:
    VALID_SUITS = {"S": "♠️", "H": "❤️", "D": "♦️", "C": "♣️"} #
    SUITS = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}

    # Use a Dummy Head Card Node for indicating if the stack of cards is empty or not
    # Suit property is optional
    def __init__(self):
        """
        Card Stack data structure with Blank Card head acting as dummy card. Implements a linked list with the principle of first in, last out.
        
        A Card Stack suit defaults to None. A Card Stack without a set suit value will be displayed as a filler card, like on a card
        table. However, if a suit is set for a Card Stack, that suit will be displayed as a filler card.
        
        """
        self.head = CardNode(Card("B", 0))
        self.head.value.flip_card()
        self._size = 0
        self._suit = None

    @property
    def size(self):
        """Returns the number of cards in the stack (read-only)."""
        return self._size 

    @property
    def suit(self):
        """Returns the suit of the stack if suit is needed."""
        return self._suit

    @suit.setter
    def suit(self, value):
        """Sets the suit only if it is one of the four valid values."""
        if value not in self.VALID_SUITS.keys():
            raise ValueError(f"Invalid suit '{value}'. Must be one of {self.VALID_SUITS.keys()} or None.")
        self._suit = value
        # self.head.value = self.VALID_SUITS[self._suit]
        self.head.value.face = self.VALID_SUITS[self._suit]

    # String representation of the stack of cards
    def __str__(self):
        if self.is_empty():
            return self.head.value.face
        
        current_card = self.head.next
        card_stack = ""
        while current_card:
            card_stack += repr(current_card.value) + " ->\n"
            # card_stack += str(current_card.value) + " ->\n"
            current_card = current_card.next
        return card_stack
    
    def to_list(self):
        if self.is_empty():
            return [" "]   
        current_card = self.head.next
        card_list = []
        while current_card:
            if current_card.value.visible:
                card_list.append(current_card.value.face)
            else:
                # card_list.append(" ")
                card_list.append("🎴")
            current_card = current_card.next
        return card_list


    # Check if the stack is empty
    def is_empty(self):
        return self._size == 0
    
    def get_stack_suit(self):
        if self._suit is not None:
            return self.head.value.face
        else:
            return None

    # Get the top card of the card stack
    def top_card(self):
        """Returns the top card of the card stack"""
        if self.is_empty():
            # raise Exception("This pile of cards is empty.")
            return None #self.head.value # Value of head is string
        
        return self.head.next.value
    
    def look_at(self, stack_index):
        """Traverses card stack to retrieve card at the requested stack_index position from the top."""
        if stack_index < 0 or stack_index >= self._size: 
            raise IndexError(f"Index {stack_index} out of bounds for stack of size {self._size}.")
        
        current_card_node = self.head.next
       
        for _ in range(stack_index): 
            if not current_card_node: 
                raise IndexError("Index {stack_index} out of bounds with None pointer.")
            current_card_node = current_card_node.next
        
        if current_card_node:
            return current_card_node.value
        else: 
            raise IndexError("Could not retrieve card due to internal error.")
    
    # def __iter__(self):
    #     current_card_node = self.head.next
    #     while current_card_node:
    #         yield current_card_node.value
    #         current_card_node = current_card_node.next


    # Push a value into the stack.
    def add_to(self, card: 'Card'):
        card_node = CardNode(card)
        card_node.next = self.head.next # Make the new node point to the current head
        self.head.next = card_node # Update the head to be the new node
        self._size += 1


    # Remove a value from the stack and return.
    def remove_from(self, flip: bool=False):
        if self.is_empty():
            raise EmptyPileError()
        remove_card = self.head.next
        self.head.next = remove_card.next 
        self._size -= 1
        if flip:
            remove_card.value.flip_card()

        return remove_card.value
    
    # Remove a value from the bottom of the stack and return.
    # def remove_from_bottom(self, flip: bool=False):
    #     if self.is_empty():
    #         raise EmptyPileError()
    #     remove_card = self.head.next
    #     self.head.next = remove_card.next 
    #     self._size -= 1
    #     if flip:
    #         remove_card.value.flip_card()

    #     return remove_card.value


class CardDeck:
    def __init__(self):
        self.deck = self.create_deck()

    @property
    def size(self):
        return len(self.deck)
        
    def create_deck(self):
        suit_values = ("S", "H", "D", "C")
        return deque([Card(suit=suit, value=value) for suit in suit_values for value in range(1, 14)])
    
    def shuffle_deck(self):
        shuffle(self.deck)
    
    def get_deck(self):
        return self.deck
    
    def get_empty_card_stack(self):
        return CardStack()
    
    def get_empty_card_queue(self):
        return CardQueue()
    
    def add_card(self, card):
        self.deck.append(card)

    def deal_card(self, facedown=True):
        if self.size == 0:
            print("CardDeck is empty.")
            return None
        card = self.deck.pop()      
        card.visible = not facedown
        return card
    
    def deal_cards(self, number_of_cards=52, facedown=True):
        card_stack = CardStack()
        for i in range(number_of_cards):
            if card := self.deal_card(facedown):
                card_stack.add_to(card)
            else:
                print("Dealing is finished.")
                break   
        return card_stack
    
    def deal(self, number_of_players, number_of_cards=52, facedown=True, shuffle=False):
        if shuffle:
            self.shuffle_deck()
        players = [self.deal_cards(number_of_cards, facedown) for _ in range(number_of_players)]
        return players

    
    def pile(self, facedown=True):
        card_stack = CardStack()
        # print(self.deck)
        while self.size != 0:
            card = self.deck.popleft()
            card.visible = not facedown
            card_stack.add_to(card)      
        # print("Piling is finished")
        # print(card_stack)
        return card_stack
    
    def get_first_card(self):
        if self.size == 0:
            print("CardDeck is empty.")
            return None
        return self.deck.popleft()
    
    def __str__(self):
        return str(f"This is a card deck with {self.size} card(s)")

if __name__=="__main__":
    # CARD QUEUE TESTING
    q = CardQueue()
    print(q)
    q.add_to(Card("S", 4))
    q.add_to(Card("H", 0))
    q.add_to(Card("H", 12))
    q.add_to(Card("S", 11))
    q.add_to(Card("D", 8))
    # q.add_to("Three")
    print(q)
    # exit()
    print(q.size)
    r = q.remove_from()
    print(r)
    q.remove_from()
    # print("TAIl")
    # print(q.tail)
    d = q.remove_from_top()
    print(d.look_card())
    # print(q)
    # # q.remove_from_top()
    print(q)
    exit()

    # CARD DECK TESTING
    deck = CardDeck()
    print(deck)
    players = deck.deal(2, 6)
    print(deck.__str__())
    for p in players:
        tc = p.top_card()
        tc.flip_card()
        tc.visible = False
        print(tc)
    s1 = players[0]
    print(s1.suit)
    t1 =s1.top_card()
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
    print(pile.top_card())
    # pile.top_card().visible = True
    print(pile.top_card())

    exit()
        
        # pile.add_to(card)
        # print(pile.head.next.value)
        # # print(pile.top_card().next.next)
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
    #     print(stack2.top_card())
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
    #     # print(stack.top_card())

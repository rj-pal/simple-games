"""
card_structures.py 
Author: Robert Pal
Updated: 2026-08-31

This module contains foundational code for a two card data structures and one wrapper class: CardQueue, CardStack, CardNode

These two custom Card Objects are Linked Lists, which use a wrapper CardNode class for implementation.

The original intent of this data structure was to demonstrate implementations of a stacks and queues using a linked list and node design pattern.
"""

from core.base_card_model import Card
from core.cards import StandardCard
from utils.emojis import SUITS, FACE_DOWN_EMOJI
from utils.errors import EmptyPileError

# Python script to demonstrate stack and queue implementation using linked lists and wrapper node class

class CardNode:
    
    def __init__(self, value):
        """
        Base wrapper node class for Card Objects (CardQueue and CardStack) in the CardDeck Object that use a Card Object. 
        
        Implements these objects using single or double linked list data structures.

        For 'value', only Card Objects are permitted to be included in a node
        """
        if not isinstance(value, Card):
            raise TypeError("Only objects of Card(BaseCard) are allowed in CardNode")
        self.value = value
        self.next = None
        self.previous = None

# Card Data Structures default to StandardCard, but Card Node can accept any Card object based on ABC Card

class CardQueue:

    def __init__(self, card_cls=StandardCard):
        """
        Card Queue data structure with Blank Card Head acting as dummy head. Implements a linked list with the principle of first in, first out.
        
        Card Queue also allows for popping from the end of the queue (the active card in play).
        """
        self.card_cls = card_cls
        dummy_head_card = self.card_cls("B", 0)
        dummy_head_card.flip_card()

        self.head = CardNode(dummy_head_card) # dummy head node is flipped blank card indicating a pile of cards exists, uses 'alt' display emoji
        self.tail = self.head
        self._size = 0
    
    @property
    def size(self):
        """Returns the number of cards in the stack (read-only)."""
        return self._size 

    def is_empty(self):
        """Returns if the queue is empty or not."""
        return self._size == 0
    
    def add_to(self, value):
        """Pushes a new card node to the head of the queue."""
        if isinstance(value, CardNode):
            card_node = value
        elif isinstance(value, self.card_cls):
            card_node = CardNode(value)
        else:
            raise TypeError(f"Only objects of type {self.card_cls.__name__} or CardNode are allowed.")

        self.tail.next = card_node
        card_node.previous = self.tail
        self.tail = card_node
        self._size += 1

    def remove_from_front(self, flip: bool=False):
        """Removes the first card node from the queue. Returns the removed card."""
        if self.is_empty():
            raise EmptyPileError
        
        remove_card = self.head.next

        self.head.next = remove_card.next
        if remove_card != self.tail:
            remove_card.next.previous = self.head
        else:
            self.tail = self.head
        self._size -= 1

        remove_card.next = None
        remove_card.previous = None

        if flip:
            remove_card.value.flip_card()

        return remove_card

    def remove_from(self, flip: bool=False):
        """Removes the last card node from the queue. Last card is card active card in play. Returns the removed card."""
        if self.is_empty():
            raise EmptyPileError

        remove_card = self.tail
        
        remove_card.previous.next = None
        self.tail = remove_card.previous
        self._size -= 1

        remove_card.next = None
        remove_card.previous = None

        if flip:
            remove_card.value.flip_card()

        return remove_card
    
    def get_card_in_play(self):
        """Returns the tail of the card queue. Last card is active card in play. Return dummy head if empty."""
        if self.is_empty():
            return self.head.value
        return self.tail.value

    def look_at(self, queue_index):
        """Traverses card queue to retrieve card at the requested queue_index position from the back."""
        if queue_index < 0 or queue_index >= self._size: 
            raise IndexError(f"Index {queue_index} out of bounds for queue of size {self._size}.")
        
        current_card_node = self.tail
        
        for _ in range(queue_index): 
            if not current_card_node: 
                raise IndexError("Index {queue_index} out of bounds with None pointer.")
            current_card_node = current_card_node.previous
        
        if current_card_node:
            return current_card_node.value
        else: 
            raise IndexError("Could not retrieve card due to internal error.")

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
    

class CardStack:

    def __init__(self, card_cls=StandardCard):
        """
        Card Stack data structure with Blank Card head acting as dummy card. Implements a linked list with the principle of first in, last out.
        
        A Card Stack suit defaults to None, and is an optional attribute. A Card Stack without a set suit value will be displayed as a filler card, 
        like on a card table, using the dummy head. However, if a suit is set for a Card Stack, that suit can be displayed as a filler card instad of 
        the dummy card place holder. This must be implemented at the next level up in the software stack. 
        """
        self.card_cls = card_cls

        dummy_head_card = self.card_cls("B", 0)
        dummy_head_card.flip_card()

        self.head = CardNode(dummy_head_card)
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
        if value not in SUITS:
            raise ValueError(f"Invalid suit '{value}'. Must be one of {SUITS.keys()} or None.")
        self._suit = value
        self.head.value.face = SUITS[self._suit]["emoji"]

    # Check if the stack is empty
    def is_empty(self):
        return self._size == 0
    
    def get_stack_suit(self):
        if self._suit is not None:
            return self.head.value.face
        else:
            return None

    # Get the top card of the card stack
    def get_card_in_play(self):
        """Returns the top card of the card stack"""
        if self.is_empty():
            # return None
            return self.head.value
            # raise EmptyPileError
            # return None #self.head.value # Value of head is string
        
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

    # Push a value into the stack.
    def add_to(self, card):
        if isinstance(card, CardNode):
            card_node = card
        elif isinstance(card, self.card_cls):
            card_node = CardNode(card)
        else:
            raise TypeError(
                f"Only objects of type {self.card_cls.__name__} or CardNode are allowed."
            )
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

        remove_card.next = None

        return remove_card
    
    def to_list(self):
        """Returns the current state of Card Stack as a list while maintaining the state of the cards stack."""
        if self.is_empty():
            return [" "]   
        current_card = self.head.next
        card_list = []
        while current_card:
            if current_card.value.visible:
                card_list.append(current_card.value.face)
            else:
                card_list.append(FACE_DOWN_EMOJI)
            current_card = current_card.next

        return card_list

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


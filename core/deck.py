from random import shuffle

# Python program to demonstrate
# stack implementation using a linked list.
# node class

class CardNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class CardQueue:

    def __init__(self):
        self.head = CardNode("Empty Stack of Cards")
        self._size = 0
    
    @property
    def size(self):
        """Returns the number of cards in the stack (read-only)."""
        return self._size 

    def is_empty(self):
        return self._size == 0
    
    # String representation of the stack of cards
    def __str__(self):
        if self.is_empty():
            return self.head.value
        
        current_card = self.head.next
        card_queue = ""
        while current_card:
            card_queue += repr(current_card.value) + " ->\n"
            current_card = current_card.next
        return card_queue

    # Push a value into the stack.
    def add_to(self, value):
        card_node = CardNode(value)
        temp_card_node = self.head
        while temp_card_node.next:
            temp_card_node = temp_card_node.next
            
        temp_card_node.next = card_node
    
        self._size += 1

    # Remove a value from the stack and return.
    def remove_from(self):
        if self.is_empty():
            raise Exception("Popping from an empty queue")
        remove_card = self.head.next
        self.head.next = remove_card.next
        self._size -= 1
        return remove_card.value
    
    def top_card(self):
        if self.is_empty():
            return self.head.value
        return self.head.next.value


class CardStack:
    VALID_SUITS = {"S": "♠️", "H": "❤️", "D": "♦️", "C": "♣️"}#{"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}

    # Use a Dummy Head Card Node for indicating if the stack of cards is empty or not
    # Suit property is optional
    def __init__(self):
        self.head = CardNode("Empty Stack of Cards")
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
        self.head.value = self.VALID_SUITS[self._suit]

    # String representation of the stack of cards
    def __str__(self):
        if self.is_empty():
            return self.head.value
        
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

    # Get the top card of the card stack
    def top_card(self):
        """Returns the top card of the card stack"""
        if self.is_empty():
            return self.head.value
        
        return self.head.next.value


    # Push a value into the stack.
    def add_to(self, value):
        card_node = CardNode(value)
        card_node.next = self.head.next # Make the new node point to the current head
        self.head.next = card_node # Update the head to be the new node
        self._size += 1


    # Remove a value from the stack and return.
    def remove_from(self):
        if self.is_empty():
            raise Exception("Popping from an empty stack")
        remove_card = self.head.next
        self.head.next = remove_card.next 
        self._size -= 1
        return remove_card.value

class CardDeck:
    def __init__(self):
        self.deck = self.create_deck()

    @property
    def size(self):
        return len(self.deck)
        
    def create_deck(self):
        suit_values = ("S", "H", "D", "C")
        return [Card(suit=suit, value=value) for suit in suit_values for value in range(1, 14)]
    
    def shuffle_deck(self):
        return shuffle(self.deck)
    
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

    
    def pile(self, number_of_cards=52, facedown=True):
        card_queue = CardStack()
        for i in range(number_of_cards):
            if card := self.deal_card(facedown):
                card_queue.add_to(card)
            else:
                print("Piling is finished.")
                break
        return card_queue

class Card:
    def __init__(self, suit: int, value: str):
        self._suit = suit
        self._value = value 
        self._visible = False
        self.face = self.create_face()
        
    def create_face(self):
        
        suit_dict = {"S": "♠️", "H": "❤️", "D": "♦️", "C": "♣️"}
        face_dict = {1: " A", 2: " 2", 3: " 3", 4: " 4", 5: " 5", 6: " 6", 7: " 7",
                        8: " 8", 9: " 9", 10: "10", 11: " J", 12: " Q", 13: " K"}

        # {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
        #                             8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}

        return f"{face_dict[self.value]} of {suit_dict[self.suit]}"
    
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
# Driver Code
if __name__ == "__main__":
    hands = CardDeck().deal(number_of_players=5, number_of_cards=15, shuffle=True)

    for i, hand in enumerate(hands, start=1):
        print(f"Player {i}'s hand: {hand}")
    exit()




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

from random import shuffle



# Python program to demonstrate
# stack implementation using a linked list.
# node class

class CardNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class CardStack:

    # Dummy Head Card Node for indicating if the stack of cards is empty or not
    def __init__(self):
        self.head = CardNode("Empty Stack of Cards")
        self.size = 0

    # String representation of the stack of cards
    def __str__(self):
        if self.is_empty():
            return self.head.value
        
        current_card = self.head.next
        card_stack = ""
        while current_card:
            card_stack += repr(current_card.value) + " ->\n"
            current_card = current_card.next
        return card_stack

    # Get the current size of the stack
    def get_size(self):
        return self.size

    # Check if the stack is empty
    def is_empty(self):
        return self.size == 0

    # Get the top item of the stack
    def peek(self):

        if self.is_empty():
            return self.head.value
        
        return self.head.next.value.look_card()


    # Push a value into the stack.
    def push(self, value):
        card_node = CardNode(value)
        card_node.next = self.head.next # Make the new node point to the current head
        self.head.next = card_node #!!! # Update the head to be the new node
        self.size += 1


    # Remove a value from the stack and return.
    def pop(self):
        if self.is_empty():
            raise Exception("Popping from an empty stack")
        remove_card = self.head.next
        self.head.next = remove_card.next #!!! changed
        self.size -= 1
        return remove_card.value.face

class Deck:

    def __init__(self):
        self.deck = self.create_deck()

    @property
    def size(self):
        return len(self.deck)

    class Card:
        def __init__(self, suit: int, value: str):
            self.suit = suit
            self.value = value 
            self.visible = False
            self.face = self.create_face()
            
        def create_face(self):
            
            suit_dict = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}
            face_dict = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
                                        8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}

            return f"{face_dict[self.value]} of {suit_dict[self.suit]}"
        
        def look_card(self):
            return self.face
        
        def flip_card(self):
            self.visible = not self.visible
 
        def __repr__(self):
            if self.visible:
                return self.face
                # return f"Face: {self.suit}, Value: {self.value}"
            return "Hidden"
        
    def create_deck(self):
        suit_values = ("S", "H", "D", "C")
        return [self.Card(suit=suit, value=value) for suit in suit_values for value in range(1, 14)]
    
    def shuffle_deck(self):
        return shuffle(self.deck)
    
    def get_deck(self):
        return self.deck
    
    def deal_card(self, facedown=False):
        if self.size == 0:
            print("Deck is empty.")
            return None
        card = self.deck.pop()
        card.visible = facedown
        return card
    
    def deal_cards(self, number_of_cards=52, facedown=False):
        card_stack = CardStack()
        # while (n := self.get_size()) > 0:
        for i in range(number_of_cards):
            if card := self.deal_card(facedown):
             card_stack.push(card)
        
        return card_stack

# Driver Code
if __name__ == "__main__":
    deck = Deck()
    # stack = CardStack()
    # print(stack)
    # exit()
    # for i in range(52):
    #     stack.push(deck.deal_card(True))
    # print(stack.peek())
    stack = deck.deal_cards(13, True)
    stack1 = deck.deal_cards(13, True)
    stack2 = deck.deal_cards(20, True)
    stack3 = deck.deal_cards(13, True)
    stack4 = deck.deal_cards(13)
    print(f"Stack: {stack}")
    print(f"Stack: {stack1}")
    print(f"Stack: {stack2}, size {stack2.get_size()}")
    print(f"Stack: {stack3}, size {stack3.get_size()}")
    print(f"Stack: {stack4}")

    # for _ in range(1, 6):
    #     top_value = stack.pop()
    #     print(f"Pop: {top_value}") # variable name changed
    # print(f"Stack: {stack}")
    # print(stack.peek())

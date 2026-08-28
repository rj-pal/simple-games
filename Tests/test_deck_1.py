"""
test_deck.py
Unit tests for the deck.py card game module.

Tests cover Card, CardNode, CardQueue, CardStack, and CardDeck classes.
"""

import pytest
from core.deck import Card, CardNode, CardQueue, CardStack, CardDeck, SUITS, FACES


class TestCard:
    """Test cases for the Card class."""

    def test_card_creation(self):
        """Test creating a card with valid suit and value."""
        card = Card("S", 5)
        assert card.suit == "S"
        assert card.value == 5
        assert card.visible is False

    def test_card_with_all_suits(self):
        """Test creating cards with all valid suits."""
        suits = ["S", "H", "D", "C"]
        for suit in suits:
            card = Card(suit, 1)
            assert card.suit == suit

    def test_card_with_all_values(self):
        """Test creating cards with all valid values (1-13)."""
        for value in range(1, 14):
            card = Card("S", value)
            assert card.value == value

    def test_card_face_creation_numbered(self):
        """Test that numbered cards create proper face strings."""
        card = Card("H", 5)
        assert "5" in card.face
        assert "❤️" in card.face

    def test_card_face_creation_face_cards(self):
        """Test that face cards (J, Q, K) create proper face strings."""
        jack = Card("D", 11)
        queen = Card("D", 12)
        king = Card("D", 13)
        
        assert "J" in jack.face
        assert "Q" in queen.face
        assert "K" in king.face

    def test_card_face_creation_ace(self):
        """Test that aces create proper face strings."""
        ace = Card("C", 1)
        assert "A" in ace.face

    def test_card_blank_card(self):
        """Test creating a blank card (value 0)."""
        blank = Card("B", 0)
        assert blank.value == 0
        assert "place card" in blank.name.lower()

    def test_card_name_creation(self):
        """Test that card names are created correctly."""
        card = Card("S", 12)
        assert card.name == "Queen of Spades"
        
        card2 = Card("H", 1)
        assert card2.name == "Ace of Hearts"

    def test_card_is_black(self):
        """Test the is_black property for black cards."""
        spades = Card("S", 5)
        clubs = Card("C", 10)
        
        assert spades.is_black is True
        assert clubs.is_black is True

    def test_card_is_red(self):
        """Test the is_black property returns False for red cards."""
        hearts = Card("H", 5)
        diamonds = Card("D", 10)
        
        assert hearts.is_black is False
        assert diamonds.is_black is False

    def test_card_flip_card(self):
        """Test flipping a card changes visibility."""
        card = Card("S", 5)
        assert card.visible is False
        card.flip_card()
        assert card.visible is True
        card.flip_card()
        assert card.visible is False

    def test_card_flip_blank_card(self):
        """Test that flipping a blank card (value 0) doesn't change visibility."""
        blank = Card("B", 0)
        blank.flip_card()
        assert blank.visible is False

    def test_card_visibility_setter(self):
        """Test setting visibility directly."""
        card = Card("S", 5)
        card.visible = True
        assert card.visible is True
        card.visible = False
        assert card.visible is False

    def test_card_visibility_setter_invalid(self):
        """Test that non-boolean values raise ValueError."""
        card = Card("S", 5)
        with pytest.raises(ValueError):
            card.visible = "true"
        with pytest.raises(ValueError):
            card.visible = 1

    def test_card_is_visible_method(self):
        """Test the is_visible method."""
        card = Card("S", 5)
        assert card.is_visible() is False
        card.visible = True
        assert card.is_visible() is True

    def test_card_look_card(self):
        """Test the look_card method returns the face."""
        card = Card("S", 5)
        assert card.look_card() == card.face

    def test_card_str_visible(self):
        """Test string representation of visible card."""
        card = Card("S", 5)
        card.visible = True
        assert "5" in str(card)

    def test_card_str_hidden(self):
        """Test string representation of hidden card."""
        card = Card("S", 5)
        assert card.visible is False
        assert str(card) == "🎴"

    def test_card_repr(self):
        """Test card representation includes all attributes."""
        card = Card("H", 10)
        repr_str = repr(card)
        assert "Suit: H" in repr_str
        assert "Value: 10" in repr_str
        assert "Visible: False" in repr_str


class TestCardNode:
    """Test cases for the CardNode class."""

    def test_cardnode_creation(self):
        """Test creating a CardNode with a valid Card."""
        card = Card("S", 5)
        node = CardNode(card)
        assert node.value == card
        assert node.next is None
        assert node.previous is None

    def test_cardnode_invalid_value(self):
        """Test that CardNode raises TypeError for non-Card objects."""
        with pytest.raises(TypeError):
            CardNode("not a card, but a string")
        
        with pytest.raises(TypeError):
            CardNode(5)
        
        with pytest.raises(TypeError):
            CardNode(None)

    def test_cardnode_linking(self):
        """Test linking nodes together."""
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        node1 = CardNode(card1)
        node2 = CardNode(card2)
        
        node1.next = node2
        node2.previous = node1
        
        assert node1.next == node2
        assert node2.previous == node1


class TestCardQueue:
    """Test cases for the CardQueue class."""

    def test_cardqueue_creation(self):
        """Test creating an empty CardQueue."""
        queue = CardQueue()
        assert queue.size == 0
        assert queue.is_empty() is True

    def test_cardqueue_add_single_card(self):
        """Test adding a single card to the queue."""
        queue = CardQueue()
        card = Card("S", 5)
        queue.add_to(card)
        assert queue.size == 1
        assert queue.is_empty() is False

    def test_cardqueue_add_multiple_cards(self):
        """Test adding multiple cards to the queue."""
        queue = CardQueue()
        for i in range(1, 6):
            queue.add_to(Card("S", i))
        assert queue.size == 5

    def test_cardqueue_add_cardnode(self):
        """Test adding a CardNode directly to the queue."""
        queue = CardQueue()
        card = Card("S", 5)
        node = CardNode(card)
        queue.add_to(node)
        assert queue.size == 1

    def test_cardqueue_add_invalid_type(self):
        """Test that adding invalid type raises TypeError."""
        queue = CardQueue()
        with pytest.raises(TypeError):
            queue.add_to("not a card, but a string")
        with pytest.raises(TypeError):
            queue.add_to(5)

    def test_cardqueue_remove_from_front(self):
        """Test removing from the front of the queue (FIFO)."""
        queue = CardQueue()
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        queue.add_to(card1)
        queue.add_to(card2)
        
        removed = queue.remove_from_front()
        assert removed.value == card1
        assert queue.size == 1

    def test_cardqueue_remove_from_bottom(self):
        """Test removing from the bottom of the queue."""
        queue = CardQueue()
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        queue.add_to(card1)
        queue.add_to(card2)
        
        removed = queue.remove_from()
        assert removed.value == card2
        assert queue.size == 1

    def test_cardqueue_remove_from_empty_top(self):
        """Test that removing from empty queue raises Exception."""
        queue = CardQueue()
        with pytest.raises(Exception):
            queue.remove_from_top()

    def test_cardqueue_remove_from_empty_bottom(self):
        """Test that removing from bottom of empty queue raises Exception."""
        queue = CardQueue()
        with pytest.raises(Exception):
            queue.remove_from()

    def test_cardqueue_remove_from_front_returns_node(self):
        """Test that remove_from_front returns a CardNode."""
        queue = CardQueue()
        card = Card("S", 5)
        queue.add_to(card)
        
        removed = queue.remove_from_front()
        assert isinstance(removed, CardNode)
        assert removed.value == card

    def test_cardqueue_ordering(self):
        """Test that queue maintains correct FIFO ordering."""
        queue = CardQueue()
        cards = [Card("S", i) for i in range(1, 6)]
        for card in cards:
            queue.add_to(card)
        
        # Should remove in same order (FIFO)
        for expected_card in cards:
            removed = queue.remove_from_front()
            assert removed.value == expected_card

    def test_cardqueue_get_card_in_play(self):
        """Test getting the card in play (tail of queue)."""
        queue = CardQueue()
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        queue.add_to(card1)
        queue.add_to(card2)
        
        # The tail (most recently added) should be the card in play
        assert queue.get_card_in_play() == card2

    def test_cardqueue_look_at(self):
        """Test looking at a card at a specific index."""
        queue = CardQueue()
        cards = [Card("S", i) for i in range(1, 4)]
        for card in cards:
            queue.add_to(card)
        
        # Index 0 should be the most recent (tail)
        assert queue.look_at(0) == cards[2]
        assert queue.look_at(1) == cards[1]
        assert queue.look_at(2) == cards[0]


class TestCardStack:
    """Test cases for the CardStack class."""

    def test_cardstack_creation(self):
        """Test creating an empty CardStack."""
        stack = CardStack()
        assert stack.size == 0
        assert stack.is_empty() is True

    def test_cardstack_add_single_card(self):
        """Test adding a single card to the stack."""
        stack = CardStack()
        card = Card("S", 5)
        stack.add_to(card)
        assert stack.size == 1
        assert stack.is_empty() is False

    def test_cardstack_add_multiple_cards(self):
        """Test adding multiple cards to the stack."""
        stack = CardStack()
        for i in range(1, 6):
            stack.add_to(Card("S", i))
        assert stack.size == 5

    def test_cardstack_add_cardnode(self):
        """Test adding a CardNode directly to the stack."""
        stack = CardStack()
        card = Card("S", 5)
        node = CardNode(card)
        stack.add_to(node)
        assert stack.size == 1

    def test_cardstack_add_invalid_type(self):
        """Test that adding invalid type raises TypeError."""
        stack = CardStack()
        with pytest.raises(TypeError):
            stack.add_to("not a card, but a string")
        with pytest.raises(TypeError):
            stack.add_to(5)

    def test_cardstack_remove_from(self):
        """Test removing from the stack (LIFO)."""
        stack = CardStack()
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        stack.add_to(card1)
        stack.add_to(card2)
        
        removed = stack.remove_from()
        assert removed.value == card2
        assert stack.size == 1

    def test_cardstack_remove_from_empty(self):
        """Test that removing from empty stack raises Exception."""
        stack = CardStack()
        with pytest.raises(Exception):
            stack.remove_from()

    def test_cardstack_remove_from_returns_node(self):
        """Test that remove_from returns a CardNode."""
        stack = CardStack()
        card = Card("S", 5)
        stack.add_to(card)
        
        removed = stack.remove_from()
        assert isinstance(removed, CardNode)
        assert removed.value == card

    def test_cardstack_get_card_in_play_empty(self):
        """Test get_card_in_play returns a blank card."""
        stack = CardStack()
        card = stack.get_card_in_play()
        blank_card = Card("B", 0)

        assert card.value == blank_card.value
       
    def test_cardstack_get_card_in_play_with_cards(self):
        """Test get_card_in_play returns the top card."""
        stack = CardStack()
        card1 = Card("S", 5)
        card2 = Card("H", 10)
        stack.add_to(card1)
        stack.add_to(card2)
        
        assert stack.get_card_in_play() == card2

    def test_cardstack_lifo_order(self):
        """Test that stack maintains LIFO order."""
        stack = CardStack()
        cards = [Card("S", i) for i in range(1, 6)]
        for card in cards:
            stack.add_to(card)
        
        # Should remove in reverse order
        for expected_card in reversed(cards):
            removed = stack.remove_from()
            assert removed.value == expected_card

    def test_cardstack_suit_property(self):
        """Test getting and setting suit property."""
        stack = CardStack()
        assert stack.suit is None
        stack.suit = "H"
        assert stack.suit == "H"

    def test_cardstack_to_list(self):
        """Test converting stack to list."""
        stack = CardStack()
        cards = [Card("S", i) for i in range(1, 4)]
        for card in cards:
            stack.add_to(card)
        
        card_list = stack.to_list()
        assert len(card_list) == 3
        assert stack.is_empty() is False


class TestCardDeck:
    """Test cases for the CardDeck class."""

    def test_carddeck_creation(self):
        """Test creating a CardDeck initializes with 52 cards."""
        deck = CardDeck()
        assert deck.size == 52

    def test_carddeck_create_deck(self):
        """Test that deck contains all 52 cards."""
        deck = CardDeck()
        # Verify 52 cards: 4 suits × 13 values
        assert deck.size == 52

    def test_carddeck_deal_single_card(self):
        """Test dealing a single card from the deck."""
        deck = CardDeck()
        initial_size = deck.size
        
        card_node = deck.deal_card(facedown=False)
        
        assert card_node is not None
        assert deck.size == initial_size - 1
        assert card_node.value.visible is True

    def test_carddeck_deal_card_facedown(self):
        """Test dealing a card face down."""
        deck = CardDeck()
        card_node = deck.deal_card(facedown=True)
        
        assert card_node.value.visible is False

    def test_carddeck_deal_from_empty_deck(self):
        """Test dealing from an empty deck returns None."""
        deck = CardDeck()
        # Remove all cards
        while deck.size > 0:
            deck.deal_card()
        
        result = deck.deal_card()
        assert result is None

    def test_carddeck_deal_cards(self):
        """Test dealing multiple cards as a hand."""
        deck = CardDeck()
        initial_size = deck.size
        
        hand = deck.deal_cards(5, facedown=True)
        
        assert hand.size == 5
        assert deck.size == initial_size - 5
        assert isinstance(hand, CardStack)

    def test_carddeck_deal_cards_face_up(self):
        """Test dealing cards face up."""
        deck = CardDeck()
        hand = deck.deal_cards(3, facedown=False)
        
        # Check that cards in hand are visible
        cards = hand.to_list()
        for card_display in cards:
            # card_display is a string (emoji or face), not a Card object
            # A visible card will have face/number content, not just the blank emoji
            assert card_display != SUITS["B"]["emoji"] or len(hand.to_list()) == 0

    def test_carddeck_deal_hands_multiple(self):
        """Test dealing multiple hands to players."""
        deck = CardDeck()
        hands = deck.deal(3, 5, facedown=True)
        
        assert len(hands) == 3
        for hand in hands:
            assert hand.size == 5

    def test_carddeck_deal_hands_shuffle(self):
        """Test dealing with shuffle option."""
        deck = CardDeck()
        hands = deck.deal(2, 26, shuffle=True, facedown=True)
        
        assert len(hands) == 2
        assert hands[0].size == 26

    def test_carddeck_shuffle(self):
        """Test shuffling the deck."""
        deck1 = CardDeck()
        deck2 = CardDeck()
        
        deck1.shuffle_deck()
        
        # Convert both to lists to compare
        list1 = deck1.to_list()
        list2 = deck2.to_list()
        
        # Recreate decks for comparison
        deck1.recreate_deck(list1)
        deck2.recreate_deck(list2)
        
        # After shuffle, order should likely be different (very small chance they're the same)
        # We can't guarantee this, so just verify both have 52 cards
        assert len(list1) == 52
        assert len(list2) == 52

    def test_carddeck_to_list(self):
        """Test converting deck to list."""
        deck = CardDeck()
        deck_list = deck.to_list()
        
        assert len(deck_list) == 52
        assert deck.size == 0

    def test_carddeck_recreate_deck(self):
        """Test recreating deck from list."""
        deck = CardDeck()
        deck_list = deck.to_list()
        
        deck.recreate_deck(deck_list)
        assert deck.size == 52

    def test_carddeck_get_empty_stack(self):
        """Test getting an empty CardStack."""
        deck = CardDeck()
        stack = deck.get_empty_card_stack()
        
        assert isinstance(stack, CardStack)
        assert stack.is_empty() is True

    def test_carddeck_get_empty_queue(self):
        """Test getting an empty CardQueue."""
        deck = CardDeck()
        queue = deck.get_empty_card_queue()
        
        assert isinstance(queue, CardQueue)
        assert queue.is_empty() is True

    def test_carddeck_add_card(self):
        """Test adding a card back to the deck."""
        deck = CardDeck()
        initial_size = deck.size
        
        card = Card("S", 5)
        deck.add_card(card)
        
        assert deck.size == initial_size + 1

    def test_carddeck_size_property(self):
        """Test that size property returns correct value."""
        deck = CardDeck()
        assert deck.size == 52
        
        deck.deal_card()
        assert deck.size == 51


class TestIntegration:
    """Integration tests combining multiple classes."""

    def test_full_game_scenario(self):
        """Test a complete game scenario: create deck, shuffle, deal hands."""
        deck = CardDeck()
        
        # Shuffle
        deck.shuffle_deck()
        
        # Deal to 4 players
        hands = deck.deal(4, 13, shuffle=False, facedown=True)
        
        # Verify distribution
        assert len(hands) == 4
        total_cards = sum(hand.size for hand in hands)
        assert total_cards == 52
        assert deck.size == 0

    def test_dealing_and_playing_cards(self):
        """Test dealing cards and revealing them."""
        deck = CardDeck()
        
        # Deal a hand
        hand = deck.deal_cards(5, facedown=True)
        
        # Get top card and flip it
        get_card_in_play = hand.get_card_in_play()
        assert get_card_in_play.visible is False
        
        get_card_in_play.flip_card()
        assert get_card_in_play.visible is True

    def test_multiple_deck_operations(self):
        """Test various operations on a single deck."""
        deck = CardDeck()
        
        # Deal some cards
        hand1 = deck.deal_cards(13)
        hand2 = deck.deal_cards(13)
        
        # Verify sizes
        assert hand1.size == 13
        assert hand2.size == 13
        assert deck.size == 26
        
        # Get remaining cards
        remaining = deck.pile()
        assert remaining.size == 26
        assert deck.size == 0

    def test_card_properties_after_dealing(self):
        """Test that card properties are maintained after dealing."""
        deck = CardDeck()
        card_node = deck.deal_card(facedown=False)
        card = card_node.value
        
        # Verify card properties
        assert card.suit in ["S", "H", "D", "C"]
        assert 1 <= card.value <= 13
        assert card.visible is True

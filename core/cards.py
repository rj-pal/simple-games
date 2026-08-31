"""
cards.py

Author: Robert Pal
Updated: 2026-08-30

Concreate Card Classes that contains specific implementations of a playing card that can be customized for game needs.
"""
from core.base_card_model import Card
from utils.emojis import CARDS, SUITS, BLANK_CARD_EMOJI, FACE_DOWN_EMOJI

class StandardCard(Card):
    """
    Concrete playing card implementation for a standard French-suited deck of cards.

    Inherits core card mechanics and interface requirements from abstract Card base class.
    """

    # Required attributes required by abstract Card base class for key data in Card (attirbutes)
    SUITS = SUITS
    CARDS = CARDS
    FACE_DOWN_CARD = FACE_DOWN_EMOJI
    BLANK_CARD = BLANK_CARD_EMOJI

    def __init__(self, suit: str, value: int):
        # Validate prior to triggering super().__init__()
        self._validate_suit(suit)
        self._validate_value(value)

        # Triggers BaseCard initialization, create_face(), and create_name()
        super().__init__(suit=suit, value=value)

    # --- Validation Helpers & Setters ---

    def _validate_suit(self, suit: str):
        """Standard suits: 'Spade', 'Diamond', 'Heart', 'Club', Blank' ('S', 'D', 'H', 'C', 'B'). Uses keys from SUITS dictionary."""
        if not isinstance(suit, str):
            raise ValueError("Suit must be a string")
        if suit not in self.SUITS:
            raise ValueError(
                f"Suit must be one of {list(self.SUITS.keys())} for standard cards"
            )

    def _validate_value(self, value: int):
        """Standard values: 0 to 13 (0 for 'Blank', 11 for 'Jack', 12 for 'Queen', 13 for 'King'). Uses keys for from CARDS dictionary."""
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        if value not in self.CARDS:
            raise ValueError(
                f"Value must be one of {list(self.CARDS.keys())} for standard cards"
            )

    @Card.suit.setter
    def suit(self, new_suit: str):
        self._validate_suit(new_suit)
        self._suit = new_suit

    @Card.value.setter
    def value(self, new_value: int):
        self._validate_value(new_value)
        self._value = new_value

    # --- Specific Standard Card Properties ---

    @property
    def is_black(self) -> bool:
        """Returns True if card suit is Spades or Clubs."""
        return self.suit in {"S", "C"}
    
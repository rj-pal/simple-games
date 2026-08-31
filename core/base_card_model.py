"""
base_card_model.py

Author: Robert Pal
Updated: 2026-08-30

Base Card Contains key data for a playing card that can be used in any kind of card game.
"""
from abc import ABC

class Card(ABC):
    """
    Abstract Base Class for all Card object implementations. Subclasses require configuration mappings to define card faces and card names for UI. 
    All implementations must define non-empty CARDS, SUITS, FACE_DOWN_CARD, and BLANK_CARD for visual representations and messaging, in order for cards to 
    have concrete data for all attributes.

    Card attributes:

    suit - string
    value - number (or number substitute for a face)
    visible - boolean (set initial to 'False' indicating face down card)
    face - custom-emoji based string
    name - basic card string for display messaging

    Card Methods

    flip_card - to change visible attribute (mimicks flipping over card on a table)
    look_card - to view the current face whether visible or not (mimicks peeking at the card face)
    """
    CARDS: dict = {}
    SUITS: dict = {}
    FACE_DOWN_CARD: str = ""
    BLANK_CARD: str = ""

    def __init__(self, suit: str, value: int):
        self._suit = suit
        self._value = value
        self._visible = False

        # Set face-down and blank representations directly from enforced class attributes
        self.face_down_card = self.FACE_DOWN_CARD
        self.blank_card = self.BLANK_CARD

        # Visual and messaging ttributes that can be customized through overriding abstract methods create_name and create_face

        self.face = self.create_face()
        self.name = self.create_name()

    def __init_subclass__(cls, **kwargs):
        """Enforces that concrete subclasses explicitly define all required attributes at class definition time."""
        super().__init_subclass__(**kwargs)
        
        required_attrs = {
            "CARDS": dict,
            "SUITS": dict,
            "FACE_DOWN_CARD": str,
            "BLANK_CARD": str,
        }
        
        for attr, attr_type in required_attrs.items():
            val = getattr(cls, attr, None)
            if not val or not isinstance(val, attr_type):
                raise TypeError(
                    f"Subclass '{cls.__name__}' must explicitly define a non-empty '{attr}' ({attr_type.__name__})."
                )

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, new_visibility: bool):
        if not isinstance(new_visibility, bool):
            raise ValueError("Visible must be a boolean value.")
        self._visible = new_visibility

    def flip_card(self):
        if self.value != 0:
            self._visible = not self._visible

    def look_card(self):
        return self.face

    # --- Abstract / Overrideable Methods ---

    def create_face(self, card_key: str = "short", suit_key: str = "emoji") -> str:
        """Generates visual string representation using configuration mappings when face-up. Default keys for emoji graphic representations."""
        if self.value == 0:
            return self.blank_card
        
        card_val = self.CARDS.get(self.value, {}).get(card_key, str(self.value))
        suit_val = self.SUITS.get(self.suit, {}).get(suit_key, str(self.suit))
        return f"{card_val} of {suit_val}"

    def create_name(self, card_key: str = "full", suit_key: str = "name") -> str:
        """Generates display text name using configuration mappings for UI messaging. Default keys for fully spelled card names in messages."""
        if self.value == 0:
            return "This is a place card."
            
        card_val = self.CARDS.get(self.value, {}).get(card_key, str(self.value))
        suit_val = self.SUITS.get(self.suit, {}).get(suit_key, str(self.suit))
        return f"{card_val} of {suit_val}"

    def __repr__(self):
        """Key attribute information"""
        return f"Suit: {self.suit}, Value: {self.value}, Visible: {self.visible}, Face: {self.face}"

    def __str__(self):
        """Displays the face of the card or face down side of the card."""
        return self.face if self.visible else self.face_down_card
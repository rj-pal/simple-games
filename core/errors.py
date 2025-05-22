class GameError(Exception):
    """Base exception for all game-related errors."""
    pass

class EmptyPileError(GameError):
    """Raised when trying to draw from an empty deck."""
    def __init__(self, message="The pile is empty."):
        super().__init__(message)

class EmptyDrawPileError(EmptyPileError):
    """Raised when trying to draw from an empty deck."""
    def __init__(self, message="The draw pile is empty. There are no cards to draw from."):
        super().__init__(message)

class EmptyFoundationPileError(EmptyPileError):
    """Raised when trying to draw from an empty deck."""
    def __init__(self, message="The foundation pile is empty. There are no cards to draw from."):
        super().__init__(message)

class InvalidStackError(GameError):
    def __init__(self, message="Invalid tableau stack number."):
        super().__init__(message)

class InvalidMoveError(GameError):
    """Raised when a move cannot be played as attempted."""
    def __init__(self, message="This move cannot be played in this situation."):
        super().__init__(message)


class InvalidPlayError(GameError):
    """Raised when a card cannot be played as attempted."""
    def __init__(self, message="That card cannot be played in this situation."):
        super().__init__(message)

class PlayerHasNoCardsError(GameError):
    """Raised when a player tries to play a card but has none."""
    def __init__(self, message="You don't have any cards to play!"):
        super().__init__(message)
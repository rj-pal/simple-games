from enum import Enum

class GameOptions(Enum):
    TIC_TAC_TOE = "1"
    CONNECT_FOUR = "2"
    SOLITAIRE = "3"

    @classmethod
    def values(cls):
        return {choice.value for choice in cls}
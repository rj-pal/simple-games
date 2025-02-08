from collections import namedtuple, Counter
from typing import Tuple, List

class Player:
        def __init__(self, name: str = None, marker: str = None):
            self.name = name
            self.marker = marker
            self.win_count = 0
            self.lost_count = 0
            self.games_played = 0

        def game_played(self) -> None:
            """Updates the number of total games played by the player."""
            self.games_played += 1

        def won(self) -> None:
            """Updates the number of games won of the player."""
            self.win_count += 1

        def lost(self) -> None:
            """Updates the number of games lost of the player."""
            self.lost_count += 1

        def get_draw_count(self) -> int:
            """Returns the number of tied games of the player based on the other game statistics."""
            return self.games_played - (self.win_count + self.lost_count)

        def __repr__(self) -> str:
            """Returns a string of information on current attributes of the player for information purposes only. Stored
            as a named tuple. """
            PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "draw", "played"])

            player_info = PlayerRepr(
                self.name,
                self.marker,
                self.win_count,
                self.lost_count,
                self.get_draw_count(),
                self.games_played
            )
            return str(player_info)
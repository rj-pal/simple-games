from collections import namedtuple
from typing import Tuple, List
from copy import deepcopy

class Player:
    def __init__(self, name: str = None, marker: str = None):
        self._name = name
        self._marker = marker
        self._win_count = 0
        self._lost_count = 0
        self._games_played = 0
        self.name = name
        self.marker = marker

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, value):
        self._marker = value

    @property
    def win_count(self):
        return self._win_count

    @win_count.setter
    def win_count(self, value):
        if value < 0:
            raise ValueError("Win count cannot be negative.")
        self._win_count = value

    @property
    def lost_count(self):
        return self._lost_count

    @lost_count.setter
    def lost_count(self, value):
        if value < 0:
            raise ValueError("Lost count cannot be negative.")
        self._lost_count = value

    @property
    def games_played(self):
        return self._games_played

    @games_played.setter
    def games_played(self, value):
        if value < 0:
            raise ValueError("Games played cannot be negative.")
        self._games_played = value

    @property
    def draw_count(self) -> int:
        """Returns the number of tied games of the player based on the other game statistics."""
        return self.games_played - (self.win_count + self.lost_count)

    def get_player_name(self) -> str:
        return deepcopy(self.name)
    
    def get_player_marker(self) -> str:
        return deepcopy(self.marker)
    
    def game_played(self) -> None:
        """Updates the number of total games played by the player."""
        self.games_played += 1

    def won(self) -> None:
        """Updates the number of games won by the player."""
        self.win_count += 1

    def lost(self) -> None:
        """Updates the number of games lost by the player."""
        self.lost_count += 1

    def __repr__(self) -> str:
        """Returns a string of information on current attributes of the player for information purposes only."""
        PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "draw", "played"])
        player_info = PlayerRepr(
            self.name,
            self.marker,
            self.win_count,
            self.lost_count,
            self.draw_count,
            self.games_played
        )
        return str(player_info)

    
    def __str__(self) -> str:
        """Returns a string of key information on the player statistics used for printing in the Game Class."""
        player_string = f"\n{self.marker}: {self.name}\nWin: {self.win_count}, Loss: {self.lost_count}, " \
                        f"Draw: {self.draw_count}\n"
        return player_string

a =Player()
print(a.name)
print(a.marker)
# class Player:
#         def __init__(self, name: str = None, marker: str = None):
#             self.name = name
#             self.marker = marker
#             self.win_count = 0
#             self.lost_count = 0
#             self.games_played = 0

#         def game_played(self) -> None:
#             """Updates the number of total games played by the player."""
#             self.games_played += 1

#         def won(self) -> None:
#             """Updates the number of games won of the player."""
#             self.win_count += 1

#         def lost(self) -> None:
#             """Updates the number of games lost of the player."""
#             self.lost_count += 1

#         def get_draw_count(self) -> int:
#             """Returns the number of tied games of the player based on the other game statistics."""
#             return self.games_played - (self.win_count + self.lost_count)

#         def __repr__(self) -> str:
#             """Returns a string of information on current attributes of the player for information purposes only. Stored
#             as a named tuple. """
#             PlayerRepr = namedtuple("Player", ["name", "marker", "win", "lost", "draw", "played"])

#             player_info = PlayerRepr(
#                 self.name,
#                 self.marker,
#                 self.win_count,
#                 self.lost_count,
#                 self.get_draw_count(),
#                 self.games_played
#             )
#             return str(player_info)
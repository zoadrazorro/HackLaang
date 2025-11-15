"""
Track implementation - represents a temporal logical timeline.
"""

from enum import Enum
from typing import Callable


class LogicType(Enum):
    """
    Enumeration of the types of logic supported by HaackLang.
    """
    CLASSICAL = "classical"
    FUZZY = "fuzzy"
    PARACONSISTENT = "paraconsistent"


class Track:
    """
    Represents a logical track with its own period, phase, and logic.

    A track is a temporal timeline that fires at regular intervals, defined by
    its period and phase. Each track is also associated with a specific logic
    system.

    Attributes:
        name (str): The name of the track.
        period (int): The period of the track.
        phase (int): The phase of the track.
        logic (LogicType): The logic system used by the track.
        current_beat (int): The internal beat counter for the track.
    """
    
    def __init__(self, name: str, period: int, phase: int = 0, logic: LogicType = LogicType.CLASSICAL):
        """
        Initializes a Track.

        Args:
            name (str): The name of the track.
            period (int): The period of the track.
            phase (int): The phase of the track.
            logic (LogicType): The logic system for the track.
        """
        self.name = name
        self.period = period
        self.phase = phase
        self.logic = logic
        self.current_beat = 0
    
    def is_active(self, global_beat: int) -> bool:
        """
        Checks if the track fires on a given global beat.

        Args:
            global_beat (int): The global beat to check against.

        Returns:
            bool: True if the track is active on the given beat, False otherwise.
        """
        return (global_beat - self.phase) % self.period == 0
    
    def advance(self):
        """Advances the track's internal beat counter by one."""
        self.current_beat += 1
    
    def __repr__(self):
        """
        Returns a string representation of the Track.

        Returns:
            str: The string representation of the Track.
        """
        return f"Track({self.name}, period={self.period}, phase={self.phase}, logic={self.logic.value})"

"""
Track implementation - represents a temporal logical timeline.
"""

from enum import Enum
from typing import Callable


class LogicType(Enum):
    """Types of logic."""
    CLASSICAL = "classical"
    FUZZY = "fuzzy"
    PARACONSISTENT = "paraconsistent"


class Track:
    """Represents a logical track with its own period and logic."""
    
    def __init__(self, name: str, period: int, phase: int = 0, logic: LogicType = LogicType.CLASSICAL):
        self.name = name
        self.period = period
        self.phase = phase
        self.logic = logic
        self.current_beat = 0
    
    def is_active(self, global_beat: int) -> bool:
        """Check if this track fires on the given global beat."""
        return (global_beat - self.phase) % self.period == 0
    
    def advance(self):
        """Advance the track's internal beat counter."""
        self.current_beat += 1
    
    def __repr__(self):
        return f"Track({self.name}, period={self.period}, phase={self.phase}, logic={self.logic.value})"

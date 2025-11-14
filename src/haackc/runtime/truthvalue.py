"""
TruthValue (BoolRhythm) implementation - multi-track truth values.
"""

from typing import Dict, Optional, Union
from .track import Track, LogicType


class TruthValue:
    """
    Represents a multi-track truth value (BoolRhythm).
    Each track has its own truth value that can evolve independently.
    """
    
    def __init__(self, tracks: Dict[str, Track], initial_value: Union[float, Dict[str, float]] = 0.0):
        """
        Initialize a TruthValue.
        
        Args:
            tracks: Dictionary mapping track names to Track objects
            initial_value: Either a single value for all tracks, or a dict of values per track
        """
        self.tracks = tracks
        self.values: Dict[str, float] = {}
        
        if isinstance(initial_value, dict):
            for track_name in tracks:
                self.values[track_name] = initial_value.get(track_name, 0.0)
        else:
            for track_name in tracks:
                self.values[track_name] = float(initial_value)
    
    def get(self, track_name: str) -> float:
        """Get the truth value for a specific track."""
        return self.values.get(track_name, 0.0)
    
    def set(self, track_name: str, value: float):
        """Set the truth value for a specific track."""
        if track_name in self.values:
            # Clamp to [0, 1] for fuzzy/paraconsistent, {0, 1} for classical
            track = self.tracks.get(track_name)
            if track and track.logic == LogicType.CLASSICAL:
                self.values[track_name] = 1.0 if value >= 0.5 else 0.0
            else:
                self.values[track_name] = max(0.0, min(1.0, float(value)))
    
    def set_all(self, value: float):
        """Set the same value for all tracks."""
        for track_name in self.values:
            self.set(track_name, value)
    
    def to_dict(self) -> Dict[str, float]:
        """Get all track values as a dictionary."""
        return self.values.copy()
    
    def to_classical(self) -> bool:
        """
        Convert to a classical boolean by taking the main track
        or the average if no main track exists.
        """
        if 'main' in self.values:
            return self.values['main'] >= 0.5
        # Otherwise take average
        if self.values:
            avg = sum(self.values.values()) / len(self.values)
            return avg >= 0.5
        return False
    
    def __repr__(self):
        vals = ', '.join(f"{k}: {v:.2f}" for k, v in self.values.items())
        return f"TruthValue({{{vals}}})"
    
    def __float__(self):
        """Convert to float by using main track or average."""
        if 'main' in self.values:
            return self.values['main']
        if self.values:
            return sum(self.values.values()) / len(self.values)
        return 0.0
    
    def __bool__(self):
        """Convert to bool."""
        return self.to_classical()


def apply_logic_operator(op: str, logic: LogicType, *operands: float) -> float:
    """
    Apply a logical operator according to the specified logic type.
    
    Args:
        op: Operator name ('and', 'or', 'not')
        logic: Logic type to use
        operands: Operand values (1 for unary, 2 for binary)
    
    Returns:
        Result value in range [0, 1]
    """
    if logic == LogicType.CLASSICAL:
        # Classical boolean logic
        if op == 'and':
            return 1.0 if (operands[0] >= 0.5 and operands[1] >= 0.5) else 0.0
        elif op == 'or':
            return 1.0 if (operands[0] >= 0.5 or operands[1] >= 0.5) else 0.0
        elif op == 'not':
            return 1.0 if operands[0] < 0.5 else 0.0
    
    elif logic == LogicType.FUZZY:
        # Fuzzy logic (Gödel t-norm/s-norm)
        if op == 'and':
            return min(operands[0], operands[1])
        elif op == 'or':
            return max(operands[0], operands[1])
        elif op == 'not':
            return 1.0 - operands[0]
    
    elif logic == LogicType.PARACONSISTENT:
        # Paraconsistent logic (for now, use fuzzy as base)
        # In a full implementation, this would track contradictions
        if op == 'and':
            return min(operands[0], operands[1])
        elif op == 'or':
            return max(operands[0], operands[1])
        elif op == 'not':
            # In paraconsistent logic, not introduces ambiguity
            return 1.0 - operands[0]
    
    return 0.0

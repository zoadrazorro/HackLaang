"""
TruthValue (BoolRhythm) implementation - multi-track truth values.
"""

from typing import Dict, Optional, Union
from .track import Track, LogicType


class TruthValue:
    """
    Represents a multi-track truth value, also known as a BoolRhythm.

    Each track within a TruthValue has its own truth value that can evolve
    independently. This allows for representing complex, polyrhythmic logical states.

    Attributes:
        tracks (Dict[str, Track]): A dictionary of the tracks that this
            TruthValue is aware of.
        values (Dict[str, float]): A dictionary mapping track names to their
            current truth values.
    """
    
    def __init__(self, tracks: Dict[str, Track], initial_value: Union[float, Dict[str, float]] = 0.0):
        """
        Initializes a TruthValue.

        Args:
            tracks (Dict[str, Track]): A dictionary mapping track names to
                Track objects.
            initial_value (Union[float, Dict[str, float]]): Either a single
                value to be applied to all tracks, or a dictionary of values
                for specific tracks.
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
        """
        Gets the truth value for a specific track.

        Args:
            track_name (str): The name of the track to get the value of.

        Returns:
            float: The truth value of the specified track, or 0.0 if the track
                does not exist.
        """
        return self.values.get(track_name, 0.0)
    
    def set(self, track_name: str, value: float):
        """
        Sets the truth value for a specific track.

        The value is clamped to the appropriate range for the track's logic
        system ([0, 1] for fuzzy/paraconsistent, {0, 1} for classical).

        Args:
            track_name (str): The name of the track to set the value of.
            value (float): The new truth value for the track.
        """
        if track_name in self.values:
            # Clamp to [0, 1] for fuzzy/paraconsistent, {0, 1} for classical
            track = self.tracks.get(track_name)
            if track and track.logic == LogicType.CLASSICAL:
                self.values[track_name] = 1.0 if value >= 0.5 else 0.0
            else:
                self.values[track_name] = max(0.0, min(1.0, float(value)))
    
    def set_all(self, value: float):
        """
        Sets the same value for all tracks.

        Args:
            value (float): The value to set for all tracks.
        """
        for track_name in self.values:
            self.set(track_name, value)
    
    def to_dict(self) -> Dict[str, float]:
        """
        Gets all track values as a dictionary.

        Returns:
            Dict[str, float]: A copy of the internal values dictionary.
        """
        return self.values.copy()
    
    def to_classical(self) -> bool:
        """
        Converts the TruthValue to a classical boolean.

        This is done by taking the value of the 'main' track, or the average
        of all tracks if no 'main' track exists.

        Returns:
            bool: The classical boolean representation of the TruthValue.
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
    Applies a logical operator according to the specified logic type.

    This function implements the semantics of 'and', 'or', and 'not' for
    classical, fuzzy, and paraconsistent logic systems.

    Args:
        op (str): The name of the operator ('and', 'or', 'not').
        logic (LogicType): The logic system to use for the operation.
        *operands (float): The operand values (1 for unary, 2 for binary).

    Returns:
        float: The result of the logical operation, in the range [0, 1].
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

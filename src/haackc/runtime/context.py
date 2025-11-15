"""
Context implementation - cognitive domains with specific logic rules.
"""

from typing import Dict, Optional, Any
from .track import LogicType


class Context:
    """
    Represents a cognitive context with specific logic and track bindings.

    A context is a domain of reasoning that can have its own logic system and
    be associated with a specific track. It also holds its own set of variables.

    Attributes:
        name (str): The name of the context.
        logic (Optional[LogicType]): The logic system used by the context.
        track (Optional[str]): The track associated with the context.
        variables (Dict[str, Any]): A dictionary of variables local to the context.
    """
    
    def __init__(self, name: str, logic: Optional[LogicType] = None, track: Optional[str] = None):
        """
        Initializes a Context.

        Args:
            name (str): The name of the context.
            logic (Optional[LogicType]): The logic system for the context.
            track (Optional[str]): The track associated with the context.
        """
        self.name = name
        self.logic = logic
        self.track = track
        self.variables: Dict[str, Any] = {}
    
    def __repr__(self):
        return f"Context({self.name}, logic={self.logic}, track={self.track})"

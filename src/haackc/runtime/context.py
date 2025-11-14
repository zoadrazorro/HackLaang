"""
Context implementation - cognitive domains with specific logic rules.
"""

from typing import Dict, Optional, Any
from .track import LogicType


class Context:
    """Represents a cognitive context with specific logic and track bindings."""
    
    def __init__(self, name: str, logic: Optional[LogicType] = None, track: Optional[str] = None):
        self.name = name
        self.logic = logic
        self.track = track
        self.variables: Dict[str, Any] = {}
    
    def __repr__(self):
        return f"Context({self.name}, logic={self.logic}, track={self.track})"

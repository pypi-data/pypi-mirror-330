"""
Constraints for sequence generation.

This module provides constraint definitions for controlling
sequence generation.
"""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Constraint:
    """Represents a constraint on sequence generation."""

    property_name: str
    condition: Callable[[Any], bool]
    description: str = ""

    def __call__(self, value: Any) -> bool:
        """Apply the constraint to a value."""
        return self.condition(value)

"""
Base classes and enums for the analysis module.

This module provides the fundamental types used throughout the analysis system:
- Complexity classes for time/space analysis
- Property access types for tracking how properties are used
- Base exceptions and utility types
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Set


class ComplexityClass(Enum):
    """Complexity classes for time and space analysis."""

    CONSTANT = 1  # O(1)
    LOGARITHMIC = 2  # O(log n)
    LINEAR = 3  # O(n)
    LINEARITHMIC = 4  # O(n log n)
    QUADRATIC = 5  # O(n²)
    CUBIC = 6  # O(n³)
    EXPONENTIAL = 7  # O(2ⁿ)
    FACTORIAL = 8  # O(n!)

    def __lt__(self, other):
        if not isinstance(other, ComplexityClass):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, ComplexityClass):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, ComplexityClass):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, ComplexityClass):
            return NotImplemented
        return self.value >= other.value

    def __str__(self) -> str:
        """Return the big-O notation for this complexity class."""
        return {
            ComplexityClass.CONSTANT: "O(1)",
            ComplexityClass.LOGARITHMIC: "O(log n)",
            ComplexityClass.LINEAR: "O(n)",
            ComplexityClass.LINEARITHMIC: "O(n log n)",
            ComplexityClass.QUADRATIC: "O(n²)",
            ComplexityClass.CUBIC: "O(n³)",
            ComplexityClass.EXPONENTIAL: "O(2ⁿ)",
            ComplexityClass.FACTORIAL: "O(n!)",
        }[self]


class PropertyAccessType(Enum):
    """Types of property access patterns."""

    READ = auto()  # Direct read access
    CONDITIONAL = auto()  # Used in conditional
    COMPARISON = auto()  # Used in comparison
    METHOD = auto()  # Method call
    NESTED = auto()  # Nested property access


class ValidatedAccessTypeSet(set):
    """A set that only accepts PropertyAccessType values."""

    def add(self, item):
        if not isinstance(item, PropertyAccessType):
            raise ValueError(
                f"Invalid access type: {item}. Must be a PropertyAccessType."
            )
        super().add(item)


@dataclass
class PropertyAccess:
    """Details about how a property is accessed."""

    name: str
    access_types: Set[PropertyAccessType] = field(
        default_factory=ValidatedAccessTypeSet
    )
    access_count: int = 0
    nested_properties: Set[str] = field(default_factory=set)


class ComplexityScore(Enum):
    """Complexity score levels."""

    TRIVIAL = 1
    SIMPLE = 2
    MODERATE = 3
    COMPLEX = 4
    VERY_COMPLEX = 5
    EXTREME = 6

    def __lt__(self, other):
        if not isinstance(other, ComplexityScore):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, ComplexityScore):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, ComplexityScore):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, ComplexityScore):
            return NotImplemented
        return self.value >= other.value


class AnalysisError(Exception):
    """Error raised during rule analysis."""

    pass

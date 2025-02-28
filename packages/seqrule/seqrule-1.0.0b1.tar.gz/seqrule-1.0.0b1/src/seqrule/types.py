"""
Type definitions for SeqRule.

This module contains common type definitions used throughout the library.
Centralizing these definitions improves consistency and makes type annotations
more maintainable.
"""

from enum import Enum
from typing import Any, Callable, Dict, TypeVar

# Core type variables for generic functions
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Property type definitions
PropertyKey = str
PropertyValue = Any
Properties = Dict[PropertyKey, PropertyValue]

# Function type definitions
PredicateFunction = Callable[[Any], bool]
TransformFunction = Callable[[Any], Any]


class RuleRelationship(Enum):
    """Relationship between two rules."""

    EQUIVALENT = "equivalent"
    STRICTER = "stricter"
    LOOSER = "looser"
    INCOMPARABLE = "incomparable"


class ComplexityOrder(Enum):
    """Ordering of algorithmic complexity classes."""

    CONSTANT = 1  # O(1)
    LOGARITHMIC = 2  # O(log n)
    LINEAR = 3  # O(n)
    LINEARITHMIC = 4  # O(n log n)
    QUADRATIC = 5  # O(n²)
    POLYNOMIAL = 6  # O(n^k) for k > 2
    EXPONENTIAL = 7  # O(2^n)
    FACTORIAL = 8  # O(n!)

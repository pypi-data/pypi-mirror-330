"""
Utilities for generating sequences.

This module provides functions for generating sequences from domains of objects,
with support for bounded generation, filtering, constraints, and prediction.
"""

# Create type aliases for improved readability
from typing import Any, Callable, Dict, List, TypeVar, Union

from ..core import AbstractObject, Sequence
from .constrained import ConstrainedGenerator
from .constraints import Constraint
from .core import generate_counter_examples, generate_sequences
from .lazy import LazyGenerator, generate_lazy
from .patterns import PropertyPattern

T = TypeVar("T")
Domain = List[Union[AbstractObject, Dict[str, Any]]]
FilterRule = Callable[[Sequence], bool]
ConstraintFunction = Callable[[Sequence], bool]

__all__ = [
    # Core classes
    "Constraint",
    "PropertyPattern",
    "ConstrainedGenerator",
    "LazyGenerator",
    # Generation functions
    "generate_sequences",
    "generate_counter_examples",
    "generate_lazy",
    # Type aliases
    "Domain",
    "FilterRule",
    "ConstraintFunction",
]

"""
Core abstractions for sequence rules.

This module provides the fundamental types and functions for working with
abstract objects and sequences.
"""

from typing import Any, Callable, Dict, List, Protocol, TypeVar

T = TypeVar("T")


class AbstractObject:
    """
    Represents an abstract object with arbitrary properties.
    """

    def __init__(self, **properties: Any):
        self.properties: Dict[str, Any] = properties

    def __getitem__(self, key: str) -> Any:
        value = self.properties.get(key)
        if isinstance(value, dict):
            # Return a proxy object that handles nested access
            return DictAccessProxy(value)
        return value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.properties})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AbstractObject):
            return NotImplemented
        return self.properties == other.properties

    def __hash__(self) -> int:
        def make_hashable(value):
            if isinstance(value, dict):
                return tuple((k, make_hashable(v)) for k, v in sorted(value.items()))
            elif isinstance(value, list):
                # Preserve list order in hash
                return tuple(make_hashable(v) for v in value)
            elif isinstance(value, set):
                # Convert set to sorted tuple for consistent hash
                return tuple(sorted(make_hashable(v) for v in value))
            return value

        # Convert properties to a tuple of (key, value) pairs and hash it
        return hash(
            tuple(sorted((k, make_hashable(v)) for k, v in self.properties.items()))
        )


class DictAccessProxy:
    """Proxy class for handling nested dictionary access."""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getitem__(self, key: str) -> Any:
        value = self._data.get(key)
        if value is None:
            return None
        if isinstance(value, dict):
            return DictAccessProxy(value)
        return value

    def get(self, key: Any, default: Any = None) -> Any:
        """Get a value from the dictionary with a default if not found."""
        value = self._data.get(key, default)
        if isinstance(value, dict):
            return DictAccessProxy(value)
        return value

    def __contains__(self, key: Any) -> bool:
        """Support 'in' operator for checking key existence."""
        return key in self._data


# A Sequence is simply a list of AbstractObjects.
Sequence = List[AbstractObject]


class FormalRuleProtocol(Protocol):
    """Protocol defining the interface for formal rules."""

    def __call__(self, seq: Sequence) -> bool:
        """
        Evaluates the rule against a sequence.

        Args:
            seq: The sequence to evaluate against

        Returns:
            bool: True if the sequence satisfies the rule, False otherwise
        """
        ...  # pragma: no cover


# A FormalRule is a predicate over sequences.
FormalRule = Callable[[Sequence], bool]


def check_sequence(seq: Sequence, rule: FormalRule) -> bool:
    """
    Returns True if the sequence satisfies the formal rule.

    Args:
        seq: The sequence to check
        rule: The formal rule to apply

    Returns:
        bool: True if the sequence satisfies the rule, False otherwise

    Raises:
        TypeError: If any element in the sequence is not an AbstractObject
    """
    if not all(isinstance(obj, AbstractObject) for obj in seq):
        raise TypeError("All elements in sequence must be instances of AbstractObject")
    return rule(seq)

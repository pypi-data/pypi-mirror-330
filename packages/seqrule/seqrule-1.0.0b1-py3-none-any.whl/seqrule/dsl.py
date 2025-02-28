"""
DSL layer for building sequence rules.

This module provides a high-level DSL for constructing sequence rules,
including combinators and common rule patterns.
"""

from typing import TypeVar, Union

from .core import FormalRule, FormalRuleProtocol, Sequence
from .types import PredicateFunction

T = TypeVar("T")


class DSLRule:
    """
    DSLRule wraps a formal rule with a human-readable description.

    This DSL layer allows domain experts to build high-level rules that are automatically
    translated into the underlying formal model.

    Attributes:
        func: The underlying formal rule function
        description: Human-readable description of the rule
        _original_func: The original unwrapped function for inspection

    Examples:
        >>> def ascending_values(seq):
        ...     return all(seq[i]["value"] < seq[i+1]["value"] for i in range(len(seq)-1))
        ...
        >>> rule = DSLRule(ascending_values, "values must be ascending")
        >>> rule(sequence)  # Returns True if values ascend, False otherwise
    """

    def __init__(
        self, func: Union[FormalRule, FormalRuleProtocol], description: str = ""
    ):
        """
        Initialize a DSL rule with a function and description.

        Args:
            func: The rule function that takes a sequence and returns a boolean
            description: Human-readable description of the rule's purpose
        """
        self.func = func
        self.description = description
        # Store the original function for inspection
        if hasattr(func, "__wrapped__"):
            self._original_func = func.__wrapped__
        else:
            self._original_func = func

    def __call__(self, seq: Sequence) -> bool:
        """
        Apply the rule to a sequence.

        Args:
            seq: The sequence to evaluate

        Returns:
            bool: True if the sequence satisfies the rule, False otherwise
        """
        return self.func(seq)

    def __and__(self, other: "DSLRule") -> "DSLRule":
        """
        Combine two rules with a logical AND operation.

        Args:
            other: Another DSL rule to combine with this one

        Returns:
            DSLRule: A new rule that requires both rules to be satisfied
        """
        return DSLRule(
            lambda seq: self(seq) and other(seq),
            f"({self.description} AND {other.description})",
        )

    def __or__(self, other: "DSLRule") -> "DSLRule":
        """
        Combine two rules with a logical OR operation.

        Args:
            other: Another DSL rule to combine with this one

        Returns:
            DSLRule: A new rule that requires either rule to be satisfied
        """
        return DSLRule(
            lambda seq: self(seq) or other(seq),
            f"({self.description} OR {other.description})",
        )

    def __invert__(self) -> "DSLRule":
        """
        Negate a rule with a logical NOT operation.

        Returns:
            DSLRule: A new rule that is satisfied when this rule is not
        """
        return DSLRule(lambda seq: not self(seq), f"(NOT {self.description})")

    def __repr__(self) -> str:
        """
        String representation of the rule.

        Returns:
            str: A string showing the rule description
        """
        return f"DSLRule({self.description})"

    def __get_original_func__(self):
        """
        Return the original function for inspection.

        Returns:
            Callable: The original unwrapped function
        """
        return self._original_func


def if_then_rule(
    condition: PredicateFunction, consequence: PredicateFunction
) -> DSLRule:
    """
    Constructs a DSLRule that applies to every adjacent pair in a sequence.

    If an object satisfies 'condition', then its immediate successor must satisfy 'consequence'.

    Args:
        condition: Predicate that must be satisfied by the first object
        consequence: Predicate that must be satisfied by the second object

    Returns:
        DSLRule: A rule enforcing the if-then relationship

    Examples:
        >>> # If an object is red, then the next object must have value > 5
        >>> rule = if_then_rule(
        ...     lambda obj: obj["color"] == "red",
        ...     lambda obj: obj["value"] > 5
        ... )
    """
    desc = "if [condition] then [consequence]"

    def rule(seq: Sequence) -> bool:
        for i in range(len(seq) - 1):
            if condition(seq[i]) and not consequence(seq[i + 1]):
                return False
        return True

    return DSLRule(rule, desc)


def check_range(
    seq: Sequence, start: int, length: int, condition: PredicateFunction
) -> bool:
    """
    Checks if a slice of the sequence satisfies a condition.

    Args:
        seq: The sequence to check
        start: Starting index
        length: Length of the slice
        condition: Predicate that must be satisfied by each object

    Returns:
        bool: True if the slice satisfies the condition
    """
    if len(seq) < start + length:
        return False
    return all(condition(seq[i]) for i in range(start, start + length))


def range_rule(start: int, length: int, condition: PredicateFunction) -> DSLRule:
    """
    Constructs a DSLRule requiring elements in an index range satisfy a condition.

    Args:
        start: Starting index
        length: Length of the range
        condition: Predicate that must be satisfied by each object

    Returns:
        DSLRule: A rule enforcing the condition over the range

    Examples:
        >>> # Require the first three elements to have even values
        >>> rule = range_rule(0, 3, lambda obj: obj["value"] % 2 == 0)
    """
    desc = f"elements[{start}:{start+length}] satisfy condition"
    return DSLRule(lambda seq: check_range(seq, start, length, condition), desc)


def and_atomic(*conditions: PredicateFunction) -> PredicateFunction:
    """
    Combines multiple atomic predicates into one using logical AND.

    Args:
        *conditions: Variable number of predicates to combine

    Returns:
        Callable: A new predicate that is the conjunction of all inputs

    Examples:
        >>> # Object must be red AND have value > 5
        >>> predicate = and_atomic(
        ...     lambda obj: obj["color"] == "red",
        ...     lambda obj: obj["value"] > 5
        ... )
    """
    return lambda obj: all(cond(obj) for cond in conditions)

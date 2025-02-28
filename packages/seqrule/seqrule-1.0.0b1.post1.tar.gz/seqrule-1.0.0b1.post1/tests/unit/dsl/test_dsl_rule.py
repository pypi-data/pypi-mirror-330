"""
Tests for the DSLRule class.

These tests verify that the DSLRule class correctly wraps rule functions
and provides the expected behavior.
"""

import functools

import pytest

from seqrule import AbstractObject, DSLRule
from seqrule.dsl import and_atomic, check_range, if_then_rule, range_rule


@pytest.fixture
def basic_sequence():
    """Provide a basic sequence of objects for testing."""
    return [
        AbstractObject(value=1, color="red"),
        AbstractObject(value=2, color="blue"),
        AbstractObject(value=3, color="green"),
    ]


@pytest.fixture
def empty_sequence():
    """Provide an empty sequence for testing."""
    return []


class TestDSLRule:
    """Test suite for the DSLRule class."""

    def test_initialization(self):
        """Test initialization with a rule function."""

        def is_positive(seq):
            return all(obj["value"] > 0 for obj in seq)

        rule = DSLRule(is_positive, "All values are positive")

        assert rule.func == is_positive
        assert rule.description == "All values are positive"

    def test_initialization_with_wrapped_function(self):
        """Test initialization with a wrapped function."""

        def original_func(seq):
            return True

        # Create a wrapped function using a decorator
        @functools.wraps(original_func)
        def wrapped_func(seq):
            return original_func(seq)

        rule = DSLRule(wrapped_func, "Test rule")

        # The original function should be accessed through __wrapped__
        assert rule._original_func is original_func

    def test_rule_application(self, basic_sequence):
        """Test applying a rule to a sequence."""

        def is_positive(seq):
            return all(obj["value"] > 0 for obj in seq)

        rule = DSLRule(is_positive)

        # All values in basic_sequence are positive
        assert rule(basic_sequence) is True

        # Create a sequence with a negative value
        negative_sequence = basic_sequence + [AbstractObject(value=-1)]
        assert rule(negative_sequence) is False

    def test_rule_with_empty_sequence(self, empty_sequence):
        """Test applying a rule to an empty sequence."""

        def is_empty(seq):
            return len(seq) == 0

        rule = DSLRule(is_empty, "Sequence is empty")

        assert rule(empty_sequence) is True
        assert rule([AbstractObject(value=1)]) is False

    def test_rule_with_parameters(self):
        """Test a rule function that takes additional parameters."""

        # For a rule with parameters, we need to use a closure or partial function
        def create_threshold_rule(threshold):
            def values_above_threshold(seq):
                return all(obj["value"] > threshold for obj in seq)

            return values_above_threshold

        # Create rules with different thresholds
        rule_threshold_0 = DSLRule(create_threshold_rule(0), "Values above 0")
        rule_threshold_4 = DSLRule(create_threshold_rule(4), "Values above 4")
        rule_threshold_7 = DSLRule(create_threshold_rule(7), "Values above 7")

        sequence = [
            AbstractObject(value=5),
            AbstractObject(value=10),
            AbstractObject(value=15),
        ]

        # All values are above 0
        assert rule_threshold_0(sequence) is True

        # All values are above 4
        assert rule_threshold_4(sequence) is True

        # Not all values are above 7
        assert rule_threshold_7(sequence) is False

    def test_lambda_rule(self):
        """Test using a lambda function as a rule."""
        rule = DSLRule(lambda seq: len(seq) > 0, "Non-empty sequence")

        assert rule([AbstractObject(value=1)]) is True
        assert rule([]) is False

    def test_rule_composition(self):
        """Test composing multiple rules."""

        def is_positive(seq):
            return all(obj["value"] > 0 for obj in seq)

        def is_sorted(seq):
            if len(seq) <= 1:
                return True
            return all(
                seq[i]["value"] < seq[i + 1]["value"] for i in range(len(seq) - 1)
            )

        # Combine rules using a new rule function
        def is_positive_and_sorted(seq):
            return is_positive(seq) and is_sorted(seq)

        rule = DSLRule(is_positive_and_sorted, "Positive and sorted")

        sorted_positive = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]

        unsorted_positive = [
            AbstractObject(value=3),
            AbstractObject(value=1),
            AbstractObject(value=2),
        ]

        assert rule(sorted_positive) is True
        assert rule(unsorted_positive) is False

    def test_rule_operators(self, basic_sequence):
        """Test rule operators (&, |, ~)."""
        # Create two simple rules
        is_positive = DSLRule(
            lambda seq: all(obj["value"] > 0 for obj in seq), "All positive"
        )
        has_three_items = DSLRule(lambda seq: len(seq) == 3, "Has three items")

        # Test AND operator
        and_rule = is_positive & has_three_items
        assert and_rule(basic_sequence) is True
        assert and_rule(basic_sequence + [AbstractObject(value=4)]) is False  # 4 items
        assert and_rule([AbstractObject(value=-1)]) is False  # Not positive

        # Test OR operator
        or_rule = is_positive | has_three_items
        assert or_rule(basic_sequence) is True  # Both conditions true
        assert or_rule([AbstractObject(value=1)]) is True  # Only positive true
        assert (
            or_rule(
                [
                    AbstractObject(value=-1),
                    AbstractObject(value=-2),
                    AbstractObject(value=-3),
                ]
            )
            is True
        )  # Only three items true
        assert (
            or_rule([AbstractObject(value=-1), AbstractObject(value=-2)]) is False
        )  # Both conditions false

        # Test NOT operator
        not_rule = ~is_positive
        assert not_rule(basic_sequence) is False  # All positive, so NOT is false
        assert (
            not_rule([AbstractObject(value=-1)]) is True
        )  # Not positive, so NOT is true

    def test_rule_repr(self):
        """Test the string representation of a rule."""
        rule = DSLRule(lambda seq: True, "Test rule")
        assert repr(rule) == "DSLRule(Test rule)"

    def test_get_original_func(self):
        """Test getting the original function from a rule."""

        def test_func(seq):
            return True

        rule = DSLRule(test_func, "Test rule")
        assert rule.__get_original_func__() is test_func


class TestIfThenRule:
    """Test suite for the if_then_rule function."""

    def test_if_then_rule(self):
        """Test the if_then_rule function."""

        # Create a rule: if an object is red, the next object must have value > 5
        def is_red(obj):
            return obj["color"] == "red"

        def value_gt_5(obj):
            return obj["value"] > 5

        rule = if_then_rule(is_red, value_gt_5)

        # Valid sequence: red followed by value > 5
        valid_sequence = [
            AbstractObject(color="red", value=1),
            AbstractObject(color="blue", value=6),
            AbstractObject(color="green", value=3),
        ]
        assert rule(valid_sequence) is True

        # Invalid sequence: red followed by value <= 5
        invalid_sequence = [
            AbstractObject(color="red", value=1),
            AbstractObject(color="blue", value=5),  # Not > 5
            AbstractObject(color="green", value=3),
        ]
        assert rule(invalid_sequence) is False

        # Valid sequence: no red objects
        no_red_sequence = [
            AbstractObject(color="blue", value=1),
            AbstractObject(color="green", value=2),
        ]
        assert rule(no_red_sequence) is True

        # Valid sequence: red at the end (no next object to check)
        red_at_end = [
            AbstractObject(color="blue", value=1),
            AbstractObject(color="red", value=2),
        ]
        assert rule(red_at_end) is True

        # Empty sequence should be valid
        assert rule([]) is True


class TestRangeRules:
    """Test suite for the range_rule and check_range functions."""

    def test_check_range(self):
        """Test the check_range function."""
        # Create a sequence of objects
        sequence = [{"value": 1}, {"value": 2}, {"value": 3}]

        # Check a valid range
        def is_even(obj):
            return obj["value"] % 2 == 0

        # Objects at index 1 and 2 are 2 and 3, but only 2 is even
        assert (
            check_range(sequence, 1, 1, is_even) is True
        )  # Only check index 1 (value=2)

        # Check an invalid range
        assert (
            check_range(sequence, 0, 2, is_even) is False
        )  # Objects at index 0 and 1 are 1 and 2

        # Check a range that's too long
        assert check_range(sequence, 3, 3, is_even) is False  # Not enough objects

    def test_range_rule(self):
        """Test the range_rule function."""
        # Create a sequence of objects
        sequence = [{"value": 1}, {"value": 2}, {"value": 3}]

        # Create a rule: objects at indices 1-2 must be even
        def is_even(obj):
            return obj["value"] % 2 == 0

        rule = range_rule(1, 1, is_even)  # Only check index 1 (value=2)

        # Valid sequence
        assert rule(sequence) is True

        # Invalid sequence
        invalid_sequence = [
            {"value": 1},
            {"value": 3},  # Not even
            {"value": 5},  # Not even
            {"value": 4},
            {"value": 5},
        ]
        assert rule(invalid_sequence) is False

        # Sequence too short
        short_sequence = [{"value": 2}]
        assert rule(short_sequence) is False


class TestAndAtomic:
    """Test suite for the and_atomic function."""

    def test_and_atomic(self):
        """Test the and_atomic function."""

        # Create predicates
        def is_red(obj):
            return obj["color"] == "red"

        def value_gt_5(obj):
            return obj["value"] > 5

        # Combine predicates
        is_red_and_gt_5 = and_atomic(is_red, value_gt_5)

        # Test with objects
        red_6 = AbstractObject(color="red", value=6)
        red_4 = AbstractObject(color="red", value=4)
        blue_6 = AbstractObject(color="blue", value=6)

        assert is_red_and_gt_5(red_6) is True
        assert is_red_and_gt_5(red_4) is False
        assert is_red_and_gt_5(blue_6) is False

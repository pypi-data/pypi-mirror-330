"""
Tests for sequence validation functions.

These tests verify that the check_sequence function correctly applies rules to sequences.
"""

import pytest

from seqrule import AbstractObject, DSLRule, check_sequence


@pytest.fixture
def empty_sequence():
    """Provide an empty sequence for testing."""
    return []


@pytest.fixture
def nested_properties_sequence():
    """Provide a sequence with nested properties for testing."""
    return [AbstractObject(value=1, metadata={"type": "important", "priority": 1})]


class TestSequenceValidation:
    """Test suite for sequence validation functions."""

    def test_check_sequence_with_function(self):
        """Test checking a sequence against a rule function."""

        # Create a simple rule function
        def is_positive(seq):
            return all(obj["value"] > 0 for obj in seq)

        # Create a test sequence
        sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]

        # Check the sequence
        assert check_sequence(sequence, is_positive) is True

        # Test with a failing sequence
        failing_sequence = sequence + [AbstractObject(value=-1)]
        assert check_sequence(failing_sequence, is_positive) is False

    def test_check_sequence_with_dsl_rule(self):
        """Test checking a sequence against a DSLRule."""

        # Create a DSL rule
        def has_even_values(seq):
            return any(obj["value"] % 2 == 0 for obj in seq)

        rule = DSLRule(has_even_values, "Contains even values")

        # Create test sequences
        sequence_with_even = [
            AbstractObject(value=1),
            AbstractObject(value=2),  # Even
            AbstractObject(value=3),
        ]

        sequence_without_even = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=5),
        ]

        # Check the sequences
        assert check_sequence(sequence_with_even, rule) is True
        assert check_sequence(sequence_without_even, rule) is False

    def test_check_sequence_with_empty_sequence(self, empty_sequence):
        """Test checking an empty sequence."""

        # Create a rule that checks if sequence is empty
        def is_empty(seq):
            return len(seq) == 0

        # Check the empty sequence
        assert check_sequence(empty_sequence, is_empty) is True

        # Check a non-empty sequence
        assert check_sequence([AbstractObject(value=1)], is_empty) is False

    def test_check_sequence_with_nested_properties(self, nested_properties_sequence):
        """Test checking a sequence with nested properties."""

        # Create a rule that checks for a specific nested property
        def has_important_type(seq):
            return any(obj["metadata"].get("type") == "important" for obj in seq)

        # Check the sequence
        assert check_sequence(nested_properties_sequence, has_important_type) is True

        # Create a sequence without important type
        sequence_without_important = [
            AbstractObject(value=1, metadata={"type": "normal", "priority": 1})
        ]

        assert check_sequence(sequence_without_important, has_important_type) is False

    def test_check_sequence_with_invalid_sequence(self):
        """Test checking a sequence that contains non-AbstractObject elements."""

        # Create a simple rule function
        def always_true(seq):
            return True

        # Create an invalid sequence with a non-AbstractObject element
        invalid_sequence = [
            AbstractObject(value=1),
            "not an AbstractObject",  # This is a string, not an AbstractObject
            AbstractObject(value=3),
        ]

        # Check that TypeError is raised
        with pytest.raises(TypeError) as excinfo:
            check_sequence(invalid_sequence, always_true)

        # Check the error message
        assert "All elements in sequence must be instances of AbstractObject" in str(
            excinfo.value
        )

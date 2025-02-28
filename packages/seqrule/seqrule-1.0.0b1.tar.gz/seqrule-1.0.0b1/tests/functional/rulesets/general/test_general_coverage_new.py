import unittest

from seqrule.core import AbstractObject
from seqrule.rulesets.general import (
    create_balanced_rule,
    create_dependency_rule,
    create_numerical_range_rule,
    create_pattern_rule,
    create_property_match_rule,
    create_property_trend_rule,
    create_ratio_rule,
    create_sum_rule,
    create_transition_rule,
    create_unique_property_rule,
)


class TestGeneralCoverage(unittest.TestCase):
    """Test cases to improve coverage for general.py."""

    def test_property_trend_rule(self):
        """Test property_trend_rule with various inputs."""
        # Create a rule that checks if values are increasing
        rule = create_property_trend_rule("value", "increasing")

        # Create a sequence with increasing values
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with non-increasing values
        seq = [
            AbstractObject(value=3),
            AbstractObject(value=2),
            AbstractObject(value=1),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with non-numeric values (should be skipped)
        seq = [
            AbstractObject(value="a"),
            AbstractObject(value="b"),
            AbstractObject(value="c"),
        ]

        # Check that the sequence passes (non-numeric values are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with exception in property access
        seq = [
            AbstractObject(value=1),
            AbstractObject(),  # Missing value property
            AbstractObject(value=3),
        ]

        # Check that the sequence passes (missing properties are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with None values (should be skipped)
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=None),
            AbstractObject(value=3),
        ]

        # Check that the sequence passes (None values are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with decreasing trend (to cover line 508)
        rule = create_property_trend_rule("value", "decreasing")
        seq = [
            AbstractObject(value=5),
            AbstractObject(value=3),
            AbstractObject(value=1),
        ]

        # Check that the sequence satisfies the decreasing rule
        result = rule(seq)
        self.assertTrue(result)

        # Test with non-decreasing values
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=5),
        ]

        # Check that the sequence does not satisfy the decreasing rule
        result = rule(seq)
        self.assertFalse(result)

    def test_pattern_rule(self):
        """Test pattern_rule with various inputs."""
        # Create a rule that checks if a sequence follows a pattern
        pattern = ["A", "B", "C"]
        rule = create_pattern_rule(
            pattern, "value"
        )  # Note: pattern comes first, then property_name

        # Create a sequence that follows the pattern
        seq = [
            AbstractObject(value="A"),
            AbstractObject(value="B"),
            AbstractObject(value="C"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence that doesn't follow the pattern
        seq = [
            AbstractObject(value="A"),
            AbstractObject(value="C"),  # Should be "B"
            AbstractObject(value="C"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_property_match_rule(self):
        """Test property_match_rule with various inputs."""
        # Create a rule that checks if a property matches a value
        rule = create_property_match_rule("color", "red")

        # Create a sequence with matching property
        seq = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with non-matching property
        seq = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),  # Not "red"
            AbstractObject(color="red"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_numerical_range_rule(self):
        """Test numerical_range_rule with various inputs."""
        # Create a rule that checks if values are within a range
        rule = create_numerical_range_rule("value", 1, 5)

        # Create a sequence with values in range
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=5),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with values outside range
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=6),  # Outside range
            AbstractObject(value=5),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_sum_rule(self):
        """Test sum_rule with various inputs."""
        # Create a rule that checks if the sum of values equals a target
        rule = create_sum_rule("value", 10)

        # Create a sequence with sum equal to target
        seq = [
            AbstractObject(value=2),
            AbstractObject(value=3),
            AbstractObject(value=5),  # Sum: 2 + 3 + 5 = 10
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with sum not equal to target
        seq = [
            AbstractObject(value=2),
            AbstractObject(value=3),
            AbstractObject(value=6),  # Sum: 2 + 3 + 6 = 11
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_unique_property_rule(self):
        """Test unique_property_rule with various inputs."""
        # Create a rule that checks if property values are unique
        rule = create_unique_property_rule("value", "global")

        # Create a sequence with unique values
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with non-unique values
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=1),  # Duplicate
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with adjacent scope
        rule = create_unique_property_rule("value", "adjacent")

        # Create a sequence with no adjacent duplicates
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=1),  # Not adjacent to first 1
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with adjacent duplicates
        seq = [
            AbstractObject(value=1),
            AbstractObject(value=1),  # Adjacent duplicate
            AbstractObject(value=2),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with KeyError in adjacent scope
        seq = [
            AbstractObject(value=1),
            AbstractObject(),  # Missing value property
            AbstractObject(value=2),
        ]

        # Check that the rule raises KeyError
        with self.assertRaises(KeyError):
            rule(seq)

    def test_property_cycle_rule(self):
        """Test property_cycle_rule with various inputs."""
        # Create a rule that checks if properties cycle
        # Using transition_rule instead since property_cycle_rule doesn't exist
        valid_transitions = {
            "red": {"red", "blue"},
            "blue": {"blue", "green"},
            "green": {"green", "red"},
        }
        rule = create_transition_rule("color", valid_transitions)

        # Create a sequence with valid transitions
        seq = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),  # red -> red is valid
            AbstractObject(color="blue"),  # red -> blue is valid
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with invalid transitions
        seq = [
            AbstractObject(color="red"),
            AbstractObject(color="green"),  # red -> green is invalid
            AbstractObject(color="blue"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_dependency_rule(self):
        """Test dependency_rule with various inputs."""
        # Create a rule that checks dependencies between property values
        dependencies = {
            "A": ["B", "C"],  # A depends on B and C
            "D": ["E"],  # D depends on E
        }
        rule = create_dependency_rule("type", dependencies)

        # Create a sequence with satisfied dependencies
        seq = [
            AbstractObject(type="A"),
            AbstractObject(type="B"),
            AbstractObject(type="C"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with unsatisfied dependencies
        seq = [AbstractObject(type="A"), AbstractObject(type="B")]  # Missing C

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with None value (should be skipped)
        seq = [
            AbstractObject(type=None),
            AbstractObject(type="B"),
            AbstractObject(type="C"),
        ]

        # Check that the sequence passes (None values are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with KeyError
        seq = [
            AbstractObject(),  # Missing type property
            AbstractObject(type="B"),
            AbstractObject(type="C"),
        ]

        # Check that the rule raises KeyError
        with self.assertRaises(KeyError):
            rule(seq)

    def test_balanced_rule(self):
        """Test balanced_rule with various inputs."""
        # Create a rule that checks group balance
        groups = {
            "vowels": {"A", "E", "I", "O", "U"},
            "consonants": {"B", "C", "D", "F", "G"},
        }
        rule = create_balanced_rule("letter", groups, 0.1)

        # Create a sequence with balanced groups
        seq = [
            AbstractObject(letter="A"),
            AbstractObject(letter="E"),
            AbstractObject(letter="B"),
            AbstractObject(letter="C"),
            AbstractObject(letter="D"),  # 2 vowels (40%), 3 consonants (60%)
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with unbalanced groups
        seq = [
            AbstractObject(letter="A"),
            AbstractObject(letter="E"),
            AbstractObject(letter="I"),
            AbstractObject(letter="O"),
            AbstractObject(letter="B"),  # 4 vowels (80%), 1 consonant (20%)
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with None value (should be skipped)
        seq = [
            AbstractObject(letter="A"),
            AbstractObject(letter=None),
            AbstractObject(letter="B"),
            AbstractObject(letter="C"),
            AbstractObject(letter="D"),
        ]

        # Check that the sequence passes (None values are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with KeyError (should be skipped)
        seq = [
            AbstractObject(letter="A"),
            AbstractObject(),  # Missing letter property
            AbstractObject(letter="B"),
            AbstractObject(letter="C"),
            AbstractObject(letter="D"),
        ]

        # Check that the sequence passes (missing properties are skipped)
        result = rule(seq)
        self.assertTrue(result)

        # Test with empty counts (all values skipped)
        seq = [
            AbstractObject(letter="X"),  # Not in any group
            AbstractObject(letter="Y"),  # Not in any group
            AbstractObject(letter="Z"),  # Not in any group
        ]

        # Check that the sequence passes (no valid counts)
        result = rule(seq)
        self.assertTrue(result)

    def test_ratio_rule(self):
        """Test ratio_rule with various inputs."""

        # Create a rule that checks the ratio of two properties
        # Define a filter function
        def is_even(obj):
            return obj.properties.get("value", 0) % 2 == 0

        rule = create_ratio_rule("value", 0.3, 0.7, is_even)

        # Create a sequence with correct ratio of even numbers
        seq = [
            AbstractObject(value=2),  # Even
            AbstractObject(value=4),  # Even
            AbstractObject(value=5),  # Odd
            AbstractObject(value=7),  # Odd
            AbstractObject(value=9),  # Odd
        ]

        # Check that the sequence satisfies the rule (2/5 = 0.4, which is between 0.3 and 0.7)
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with incorrect ratio
        seq = [
            AbstractObject(value=2),  # Even
            AbstractObject(value=4),  # Even
            AbstractObject(value=6),  # Even
            AbstractObject(value=8),  # Even
            AbstractObject(value=9),  # Odd
        ]

        # Check that the sequence does not satisfy the rule (4/5 = 0.8, which is > 0.7)
        result = rule(seq)
        self.assertFalse(result)

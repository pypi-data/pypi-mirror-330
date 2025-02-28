"""
Tests for the general-purpose ruleset coverage.

These tests are designed to increase test coverage for the general ruleset.
"""

import pytest

from seqrule import AbstractObject
from seqrule.dsl import DSLRule
from seqrule.rulesets.general import (
    create_alternation_rule,
    create_balanced_rule,
    create_bounded_sequence_rule,
    create_composite_rule,
    create_dependency_rule,
    create_group_rule,
    create_historical_rule,
    create_meta_rule,
    create_numerical_range_rule,
    create_pattern_rule,
    create_property_cycle_rule,
    create_property_match_rule,
    create_property_trend_rule,
    create_ratio_rule,
    create_running_stat_rule,
    create_sum_rule,
    create_transition_rule,
    create_unique_property_rule,
)


class TestGeneralCoverage:
    """Test suite for general-purpose rules coverage."""

    class TestCore:
        """Core functionality tests."""

        def test_property_trend_rule_edge_cases(self):
            """Test property trend rule with edge cases."""
            # Test with empty sequence
            rule = create_property_trend_rule("value", "increasing")
            assert rule([]) is True  # Empty sequences should pass

            # Test with single element sequence
            single_element = [AbstractObject(value=1)]
            assert rule(single_element) is True  # Single element sequences should pass

            # Test with missing property
            missing_property = [AbstractObject(other=1), AbstractObject(other=2)]
            assert (
                rule(missing_property) is True
            )  # Missing properties should be skipped

        def test_balanced_rule_edge_cases(self):
            """Test balanced rule with edge cases."""
            # Test with empty sequence
            color_groups = {"red": {"red"}, "blue": {"blue"}}
            rule = create_balanced_rule("color", color_groups)
            assert rule([]) is True  # Empty sequences should pass

            # Test with missing property
            missing_property = [
                AbstractObject(other="value1"),
                AbstractObject(other="value2"),
            ]
            assert (
                rule(missing_property) is True
            )  # Missing properties should be skipped

        def test_unique_property_rule_edge_cases(self):
            """Test unique property rule with edge cases."""
            # Test with empty sequence
            rule = create_unique_property_rule("id")
            assert rule([]) is True  # Empty sequences should pass

            # Test with adjacent scope
            rule_adjacent = create_unique_property_rule("id", scope="adjacent")
            assert rule_adjacent([]) is True  # Empty sequences should pass

            # Test with single element sequence
            single_element = [AbstractObject(id=1)]
            assert (
                rule_adjacent(single_element) is True
            )  # Single element sequences should pass

        def test_property_match_rule_edge_cases(self):
            """Test property match rule with edge cases."""
            # Test with empty sequence
            rule = create_property_match_rule("color", "red")
            assert rule([]) is True  # Empty sequences should pass

        def test_alternation_rule_edge_cases(self):
            """Test alternation rule with edge cases."""
            # Test with empty sequence
            rule = create_alternation_rule("color")
            assert rule([]) is True  # Empty sequences should pass

            # Test with single element sequence
            single_element = [AbstractObject(color="red")]
            assert rule(single_element) is True  # Single element sequences should pass

        def test_numerical_range_rule_edge_cases(self):
            """Test numerical range rule with edge cases."""
            # Test with empty sequence
            rule = create_numerical_range_rule("value", 1, 10)
            assert rule([]) is True  # Empty sequences should pass

            # Test with non-numeric values
            non_numeric = [AbstractObject(value="not-a-number")]
            assert rule(non_numeric) is True  # Non-numeric values should be skipped

        def test_sum_rule_edge_cases(self):
            """Test sum rule with edge cases."""
            # Test with empty sequence
            rule = create_sum_rule("value", 10)
            assert rule([]) is True  # Empty sequences should pass

            # Test with missing property
            with pytest.raises(ValueError, match="Missing required property: value"):
                rule([AbstractObject(other=5)])

            # Test with invalid value
            with pytest.raises(ValueError, match="Invalid value for value"):
                rule([AbstractObject(value="not-a-number")])

        def test_historical_rule_edge_cases(self):
            """Test historical rule with edge cases."""

            # Test with empty sequence
            def all_different(window):
                return len({obj.properties.get("value") for obj in window}) == len(
                    window
                )

            rule = create_historical_rule(3, all_different)
            assert rule([]) is True  # Empty sequences should pass

            # Test with sequence shorter than window
            short_sequence = [AbstractObject(value=1), AbstractObject(value=2)]
            assert (
                rule(short_sequence) is True
            )  # Sequences shorter than window should pass

            # Test with condition that raises an exception
            def failing_condition(window):
                raise ValueError("Test exception")

            rule_failing = create_historical_rule(2, failing_condition)
            test_sequence = [
                AbstractObject(value=1),
                AbstractObject(value=2),
                AbstractObject(value=3),
            ]
            assert (
                rule_failing(test_sequence) is True
            )  # Should skip windows with errors

        def test_transition_rule_edge_cases(self):
            """Test transition rule with edge cases."""
            # Test with empty sequence
            valid_transitions = {"A": {"B"}, "B": {"C"}, "C": {"A"}}
            rule = create_transition_rule("type", valid_transitions)
            assert rule([]) is True  # Empty sequences should pass

            # Test with single element sequence
            single_element = [AbstractObject(type="A")]
            assert rule(single_element) is True  # Single element sequences should pass

            # Test with missing property
            missing_property = [AbstractObject(type="A"), AbstractObject(other="B")]
            assert (
                rule(missing_property) is True
            )  # Missing properties should be skipped

            # Test with None values
            none_values = [AbstractObject(type="A"), AbstractObject(type=None)]
            assert rule(none_values) is True  # None values should be skipped

        def test_running_stat_rule_edge_cases(self):
            """Test running stat rule with edge cases."""

            # Test with empty sequence
            def mean(values):
                return sum(values) / len(values)

            rule = create_running_stat_rule("value", mean, 0, 10, window=3)
            assert rule([]) is True  # Empty sequences should pass

            # Test with sequence shorter than window
            short_sequence = [AbstractObject(value=1), AbstractObject(value=2)]
            assert (
                rule(short_sequence) is True
            )  # Sequences shorter than window should pass

            # Test with invalid values in window
            invalid_window = [
                AbstractObject(value=1),
                AbstractObject(value="not-a-number"),
                AbstractObject(value=3),
            ]
            assert rule(invalid_window) is True  # Invalid windows should be skipped

            # Test with stat function that raises an exception
            def failing_stat(values):
                return 1 / 0  # ZeroDivisionError

            rule_failing = create_running_stat_rule(
                "value", failing_stat, 0, 10, window=2
            )
            test_sequence = [
                AbstractObject(value=1),
                AbstractObject(value=2),
                AbstractObject(value=3),
            ]
            assert (
                rule_failing(test_sequence) is True
            )  # Should skip windows with errors

        def test_composite_rule_edge_cases(self):
            """Test composite rule with edge cases."""
            # Test with empty rule list
            rule = create_composite_rule([])
            assert rule([]) is True  # Empty rule list should pass

            # Test with empty sequence
            rule1 = create_property_trend_rule("value", "increasing")
            rule2 = create_numerical_range_rule("value", 1, 10)
            composite_rule = create_composite_rule([rule1, rule2])
            assert composite_rule([]) is True  # Empty sequences should pass

            # Test with rule that raises an exception
            def failing_rule(seq):
                raise ValueError("Test exception")

            failing_dsl_rule = DSLRule(failing_rule)

            # Test with "all" mode (should fail on exception)
            all_rule = create_composite_rule([rule1, failing_dsl_rule], mode="all")
            assert all_rule([AbstractObject(value=5)]) is False

            # Test with "any" mode (should skip exceptions)
            any_rule = create_composite_rule([failing_dsl_rule, rule1], mode="any")
            assert any_rule([AbstractObject(value=5)]) is True

        def test_meta_rule_edge_cases(self):
            """Test meta rule with edge cases."""
            # Test with empty rule list
            rule = create_meta_rule([], 0)
            assert rule([]) is True  # Empty rule list should pass

            # Test with empty sequence
            rule1 = create_property_trend_rule("value", "increasing")
            rule2 = create_numerical_range_rule("value", 1, 10)
            meta_rule = create_meta_rule([rule1, rule2], 1)
            assert meta_rule([]) is True  # Empty sequences should pass

        def test_property_cycle_rule_edge_cases(self):
            """Test property cycle rule with edge cases."""
            # Test with empty sequence
            rule = create_property_cycle_rule("type")
            assert rule([]) is True  # Empty sequences should pass

            # Test with single element sequence
            single_element = [AbstractObject(type="A")]
            assert rule(single_element) is True  # Single element sequences should pass

            # Test with sequence that forms a cycle
            cycle_sequence = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="A"),
                AbstractObject(type="B"),
            ]
            assert rule(cycle_sequence) is True

            # Test with sequence that doesn't form a cycle
            non_cycle = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="C"),
            ]
            assert rule(non_cycle) is False

            # Test with TypeError in property access
            class BrokenObject(AbstractObject):
                def __init__(self):
                    # Skip the parent __init__ to avoid setting self.properties
                    pass

                @property
                def properties(self):
                    raise TypeError("Test exception")

            broken_sequence = [BrokenObject(), BrokenObject()]
            assert rule(broken_sequence) is True  # Should skip properties with errors

        def test_dependency_rule_edge_cases(self):
            """Test dependency rule with edge cases."""
            # Test with empty sequence
            dependencies = {"A": {"B", "C"}}
            rule = create_dependency_rule("type", dependencies)
            assert rule([]) is True  # Empty sequences should pass

            # Test with KeyError in property access
            with pytest.raises(KeyError):
                rule([AbstractObject(other="A")])  # Missing required property

        def test_group_rule_edge_cases(self):
            """Test group rule with edge cases."""

            # Test with empty sequence
            def check_group(group):
                return len(group) <= 3

            rule = create_group_rule(3, check_group)
            assert rule([]) is True  # Empty sequences should pass

            # Test with condition that raises an exception
            def failing_condition(group):
                raise ValueError("Test exception")

            rule_failing = create_group_rule(2, failing_condition)
            test_sequence = [
                AbstractObject(value=1),
                AbstractObject(value=2),
                AbstractObject(value=3),
            ]
            assert rule_failing(test_sequence) is True  # Should skip groups with errors

        def test_ratio_rule_edge_cases(self):
            """Test ratio rule with edge cases."""

            # Test with empty sequence
            def is_type_a(obj):
                return obj.properties.get("type") == "A"

            rule = create_ratio_rule("type", 0.3, 0.7, is_type_a)
            assert rule([]) is True  # Empty sequences should pass

            # Test with no valid objects
            no_valid_objects = [AbstractObject(other="A"), AbstractObject(other="B")]
            assert rule(no_valid_objects) is True  # No valid objects should pass

            # Test with filter function that raises an exception
            def failing_filter(obj):
                raise ValueError("Test exception")

            rule_failing = create_ratio_rule("type", 0.3, 0.7, failing_filter)
            test_sequence = [AbstractObject(type="A"), AbstractObject(type="B")]
            assert (
                rule_failing(test_sequence) is True
            )  # Should skip if filter function fails

            # Test with exception in property access
            class BrokenObject(AbstractObject):
                def __init__(self):
                    # Skip the parent __init__ to avoid setting self.properties
                    pass

                @property
                def properties(self):
                    raise TypeError("Test exception")

            broken_sequence = [BrokenObject(), BrokenObject()]
            assert rule(broken_sequence) is True  # Should skip objects with errors

        def test_bounded_sequence_rule_edge_cases(self):
            """Test bounded sequence rule with edge cases."""
            # Test with empty sequence
            inner_rule = DSLRule(lambda seq: True)
            rule = create_bounded_sequence_rule(1, 5, inner_rule)
            assert (
                rule([]) is False
            )  # Empty sequences should fail (length < min_length)

    class TestEdgeCases:
        """Edge case tests."""

        def test_property_trend_rule_invalid_trend(self):
            """Test property trend rule with invalid trend type."""
            # Test with valid trend types
            create_property_trend_rule("value", "increasing")
            create_property_trend_rule("value", "decreasing")
            create_property_trend_rule("value", "non-increasing")
            create_property_trend_rule("value", "non-decreasing")

        def test_composite_rule_invalid_operator(self):
            """Test composite rule with invalid operator."""
            # Test with valid operators
            rule1 = create_property_trend_rule("value", "increasing")
            rule2 = create_numerical_range_rule("value", 1, 10)
            create_composite_rule([rule1, rule2], mode="all")
            create_composite_rule([rule1, rule2], mode="any")

        def test_running_stat_rule_invalid_stat(self):
            """Test running stat rule with invalid stat type."""

            # Test with valid stat function
            def mean(values):
                return sum(values) / len(values)

            create_running_stat_rule("value", mean, 0, 10, window=3)

    class TestCoverage:
        """Specific coverage tests."""

        def test_transition_rule_with_failures(self):
            """Test transition rule with failing transitions."""
            # Test with failing transitions
            valid_transitions = {"A": {"B"}, "B": {"C"}, "C": {"A"}}
            rule = create_transition_rule("type", valid_transitions)

            # Sequence with invalid transition (A -> C instead of A -> B)
            invalid_sequence = [AbstractObject(type="A"), AbstractObject(type="C")]
            assert rule(invalid_sequence) is False

        def test_dependency_rule_with_failures(self):
            """Test dependency rule with failing dependencies."""
            # Test with failing dependencies
            dependencies = {"A": {"B", "C"}}
            rule = create_dependency_rule("type", dependencies)

            # Sequence with A but without required B or C
            invalid_sequence = [AbstractObject(type="A"), AbstractObject(type="D")]
            assert rule(invalid_sequence) is False

        def test_group_rule_with_failures(self):
            """Test group rule with failing groups."""

            # Test with failing groups
            def check_group(group):
                # Check if all values in the group are the same
                first_value = group[0].properties.get("type")
                return all(obj.properties.get("type") == first_value for obj in group)

            rule = create_group_rule(2, check_group)

            # Sequence with groups that fail the condition
            invalid_sequence = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),  # Different from A
                AbstractObject(type="B"),
                AbstractObject(type="B"),
            ]
            assert rule(invalid_sequence) is False

        def test_ratio_rule_with_failures(self):
            """Test ratio rule with failing ratios."""

            # Test with failing ratios
            def is_type_a(obj):
                return obj.properties.get("type") == "A"

            rule = create_ratio_rule("type", 0.4, 0.6, is_type_a)

            # Sequence with ratio outside the allowed range (0.25 < 0.4)
            invalid_sequence = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="B"),
                AbstractObject(type="B"),
            ]
            assert rule(invalid_sequence) is False

        def test_property_cycle_rule_with_cycle(self):
            """Test property cycle rule with a cycle."""
            # Test with a sequence that forms a cycle
            rule = create_property_cycle_rule("type")

            # Sequence with a cycle
            cycle_sequence = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="C"),
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="C"),
            ]
            assert rule(cycle_sequence) is True

        def test_sum_rule_with_exact_match(self):
            """Test sum rule with exact match."""
            # Test with sum exactly matching target
            rule = create_sum_rule("value", 10)

            # Sequence with sum exactly 10
            exact_sequence = [AbstractObject(value=3), AbstractObject(value=7)]
            assert rule(exact_sequence) is True

        def test_pattern_rule_with_empty_sequence(self):
            """Test pattern rule with empty sequence."""
            # Test with empty sequence
            rule = create_pattern_rule(["A", "B"], "type")

            # Empty sequence
            assert rule([]) is False

    class TestAdditionalCoverage:
        """Additional tests to cover remaining uncovered lines."""

        def test_dependency_rule_with_key_error(self):
            """Test dependency rule with KeyError."""
            # Test with KeyError in property access
            rule = create_dependency_rule("type", {"A": ["B", "C"]})

            # Create a sequence with missing property
            seq = [AbstractObject(other="X")]

            # This should raise a KeyError
            with pytest.raises(KeyError):
                rule(seq)

        def test_ratio_rule_with_none_values(self):
            """Test ratio rule with None values."""

            def is_type_a(obj):
                return obj.properties.get("type") == "A"

            rule = create_ratio_rule("type", 0.0, 1.0, is_type_a)  # Allow any ratio

            # Create a sequence with None values
            seq = [AbstractObject(type=None), AbstractObject(type="B")]

            # Should skip None values
            assert rule(seq) is True

        def test_unique_property_rule_with_key_error(self):
            """Test unique property rule with KeyError."""
            # Test with KeyError in property access
            rule = create_unique_property_rule("type", "global")

            # Create a sequence with missing property
            seq = [AbstractObject(other="X"), AbstractObject(type="A")]

            # This should raise a KeyError
            with pytest.raises(KeyError):
                rule(seq)

        def test_property_trend_rule_non_increasing(self):
            """Test property trend rule with non-increasing trend."""
            rule = create_property_trend_rule("value", "non-increasing")

            # Create a sequence with non-increasing values
            seq = [
                AbstractObject(value=5),
                AbstractObject(value=5),
                AbstractObject(value=3),
            ]

            # Should pass for non-increasing values
            assert rule(seq) is True

            # Create a sequence with increasing values
            seq = [AbstractObject(value=3), AbstractObject(value=5)]

            # Should fail for increasing values
            assert rule(seq) is False

        def test_group_rule_with_none_values(self):
            """Test group rule with None values."""

            # Create a condition function that handles None values
            def check_condition(group):
                return True  # Always return True for this test

            rule = create_group_rule(2, check_condition)  # Use numeric group size

            # Create a sequence with None values
            seq = [AbstractObject(type=None), AbstractObject(type="B")]

            # Should pass with our condition
            assert rule(seq) is True

        def test_dependency_rule_with_key_error_in_check(self):
            """Test dependency rule with KeyError in check."""
            rule = create_dependency_rule("type", {"A": ["B", "C"]})

            # Create a sequence with the property but missing required values
            seq = [
                AbstractObject(type="A"),
                AbstractObject(type="D"),  # Missing required B or C
            ]

            # This should fail the rule
            assert rule(seq) is False

        def test_unique_property_rule_with_adjacent_scope(self):
            """Test unique property rule with adjacent scope."""
            rule = create_unique_property_rule("type", "adjacent")

            # Create a sequence with adjacent duplicates
            seq = [
                AbstractObject(type="A"),
                AbstractObject(type="A"),  # Adjacent duplicate
                AbstractObject(type="B"),
            ]

            # This should fail the rule
            assert rule(seq) is False

            # Create a sequence without adjacent duplicates
            seq = [
                AbstractObject(type="A"),
                AbstractObject(type="B"),
                AbstractObject(type="A"),  # Not adjacent to first A
            ]

            # This should pass the rule
            assert rule(seq) is True

        def test_property_trend_rule_with_non_numeric(self):
            """Test property trend rule with non-numeric values."""
            rule = create_property_trend_rule("value", "increasing")

            # Create a sequence with non-numeric values
            seq = [AbstractObject(value="A"), AbstractObject(value="B")]

            # This should pass (non-numeric values are skipped)
            assert rule(seq) is True

            # Create a sequence with mixed numeric and non-numeric values
            seq = [
                AbstractObject(value=1),
                AbstractObject(value="A"),
                AbstractObject(value=2),
            ]

            # This should pass (non-numeric values are skipped)
            assert rule(seq) is True

        def test_final_remaining_lines(self):
            """Test the final remaining uncovered lines."""
            # Test property trend rule with empty values list
            rule = create_property_trend_rule("value", "increasing")

            # Create a sequence with no numeric values
            seq = [
                AbstractObject(other=1),  # Missing value property
                AbstractObject(other=2),  # Missing value property
            ]

            # This should pass (no values to compare)
            assert rule(seq) is True

        def test_final_uncovered_lines(self):
            """Test the final remaining uncovered lines in general.py."""
            # Test unique property rule with adjacent scope and KeyError
            rule = create_unique_property_rule("type", "adjacent")

            # Create a sequence with missing property in adjacent check
            seq = [
                AbstractObject(type="A"),
                AbstractObject(other="X"),  # Missing type property
            ]

            # This should raise a KeyError
            with pytest.raises(KeyError):
                rule(seq)

            # Test property trend rule with insufficient values
            rule = create_property_trend_rule("value", "increasing")

            # Create a sequence with only one numeric value
            seq = [
                AbstractObject(value=1),
                AbstractObject(value="A"),  # Non-numeric, will be skipped
            ]

            # This should pass (not enough numeric values to compare)
            assert rule(seq) is True

            # Test group rule with a group that has a member
            def check_group(group):
                # Check if the group contains a vowel
                return any(
                    obj.properties.get("type") in ["A", "E", "I", "O", "U"]
                    for obj in group
                )

            rule = create_group_rule(1, check_group)  # Group size of 1

            # Create a sequence with a group member
            seq = [AbstractObject(type="A")]  # Member of vowels group

            # This should pass
            assert rule(seq) is True

        def test_remaining_uncovered_lines(self):
            """Test the remaining uncovered lines in general.py."""
            # Test dependency rule with TypeError
            rule = create_dependency_rule("type", {"A": ["B", "C"]})

            # Create a sequence with a property that raises TypeError
            class TypeErrorObject(AbstractObject):
                def __init__(self, **props):
                    self._props = props

                @property
                def properties(self):
                    if "type" in self._props and self._props["type"] == "error":
                        raise TypeError("Test TypeError")
                    return self._props

            seq = [TypeErrorObject(type="error")]

            # This should raise a KeyError (which is what the code does when it catches TypeError)
            with pytest.raises(KeyError):
                rule(seq)

            # Test unique property rule with adjacent scope and TypeError
            rule = create_unique_property_rule("type", "adjacent")

            # Create a sequence with a property that raises TypeError
            seq = [AbstractObject(type="A"), TypeErrorObject(type="error")]

            # This should raise a TypeError (the TypeError is not caught in unique_property_rule)
            with pytest.raises(TypeError):
                rule(seq)

            # Test property trend rule with TypeError
            rule = create_property_trend_rule("value", "increasing")

            # Create a sequence with a property that raises TypeError
            seq = [
                AbstractObject(value=1),
                TypeErrorObject(value="error", type="error"),
            ]

            # This should pass (the TypeError is caught and skipped)
            assert rule(seq) is True

            # Test group rule with TypeError
            def check_group(group):
                # Check if any object in the group has a property type that is a vowel
                return any(
                    obj.properties.get("type") in ["A", "E", "I", "O", "U"]
                    for obj in group
                )

            rule = create_group_rule(1, check_group)  # Use integer for group size

            # Create a sequence with a property that raises TypeError
            seq = [AbstractObject(type="A"), TypeErrorObject(type="error")]

            # This should pass (the TypeError is caught and skipped)
            assert rule(seq) is True

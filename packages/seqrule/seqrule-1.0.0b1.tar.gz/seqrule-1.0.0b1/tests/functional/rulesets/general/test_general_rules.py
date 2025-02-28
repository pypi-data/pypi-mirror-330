"""
Tests for the general-purpose ruleset.

These tests verify that the general-purpose rule factories create rules
that correctly validate sequences against common patterns.
"""

from seqrule import AbstractObject
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


class TestGeneralRules:
    """Test suite for general-purpose rules."""

    def test_property_trend_rule_ascending(self):
        """Test that property trend rule correctly validates ascending trends."""
        # Create a rule that checks if 'value' is in ascending order
        rule = create_property_trend_rule("value", "increasing")

        # Test with ascending sequence
        ascending_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]
        assert rule(ascending_sequence) is True

        # Test with non-ascending sequence
        non_ascending_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=2),
        ]
        assert rule(non_ascending_sequence) is False

        # Test with equal values (not strictly ascending)
        equal_values_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=1),
            AbstractObject(value=2),
        ]
        assert rule(equal_values_sequence) is False

    def test_property_trend_rule_descending(self):
        """Test that property trend rule correctly validates descending trends."""
        # Create a rule that checks if 'value' is in descending order
        rule = create_property_trend_rule("value", "decreasing")

        # Test with descending sequence
        descending_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=2),
            AbstractObject(value=1),
        ]
        assert rule(descending_sequence) is True

        # Test with non-descending sequence
        non_descending_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=1),
            AbstractObject(value=2),
        ]
        assert rule(non_descending_sequence) is False

    def test_property_trend_rule_non_decreasing(self):
        """Test that property trend rule correctly validates non-decreasing trends."""
        # Create a rule that checks if 'value' is non-decreasing (>=)
        rule = create_property_trend_rule("value", "non-decreasing")

        # Test with ascending sequence
        ascending_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]
        assert rule(ascending_sequence) is True

        # Test with equal values (should be valid for non-decreasing)
        equal_values_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=1),
            AbstractObject(value=2),
        ]
        assert rule(equal_values_sequence) is True

        # Test with decreasing values - should fail for non-decreasing
        decreasing_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=2),
            AbstractObject(value=1),
        ]
        # The implementation checks if current <= next, which is false for 3 <= 2
        assert rule(decreasing_sequence) is False

    def test_pattern_rule(self):
        """Test that pattern rule correctly validates property patterns."""
        # Create a rule that checks if 'color' follows the pattern ["red", "blue", "green"]
        pattern = ["red", "blue", "green"]
        rule = create_pattern_rule(pattern, "color")

        # Test with matching pattern
        matching_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
        ]
        assert rule(matching_sequence) is True

        # Test with non-matching pattern
        non_matching_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="green"),
            AbstractObject(color="blue"),
        ]
        assert rule(non_matching_sequence) is False

        # Test with repeating pattern
        repeating_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
        ]
        assert rule(repeating_sequence) is True

        # Test with truncated pattern
        truncated_sequence = [AbstractObject(color="red"), AbstractObject(color="blue")]
        assert rule(truncated_sequence) is True

    def test_balanced_rule(self):
        """Test that balanced rule correctly validates property value distributions."""
        # Create a rule that checks if 'color' values are balanced within 20% tolerance
        # Note: The balanced rule now requires a groups parameter, so we'll create a mapping of each color to itself
        color_groups = {"red": {"red"}, "blue": {"blue"}, "green": {"green"}}
        rule = create_balanced_rule("color", color_groups, tolerance=0.2)

        # Test with balanced sequence
        balanced_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
            AbstractObject(color="green"),
        ]
        # Equal distribution: 2 red, 2 blue, 2 green = perfectly balanced
        assert rule(balanced_sequence) is True

        # Test with slightly unbalanced sequence (within tolerance)
        slightly_unbalanced = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
            AbstractObject(color="green"),
        ]
        # Distribution: 3 red, 2 blue, 2 green - within 20% tolerance
        assert rule(slightly_unbalanced) is True

        # Test with very unbalanced sequence
        very_unbalanced = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
        ]
        # Distribution: 4 red, 1 blue, 1 green - outside 20% tolerance
        assert rule(very_unbalanced) is False

    def test_uniqueness_rule(self):
        """Test that uniqueness rule correctly validates unique property values."""
        # Create a rule that checks if 'id' values are unique
        rule = create_unique_property_rule("id")

        # Test with unique values
        unique_sequence = [
            AbstractObject(id=1),
            AbstractObject(id=2),
            AbstractObject(id=3),
        ]
        assert rule(unique_sequence) is True

        # Test with duplicate values
        duplicate_sequence = [
            AbstractObject(id=1),
            AbstractObject(id=2),
            AbstractObject(id=2),  # Duplicate
        ]
        assert rule(duplicate_sequence) is False

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence has no duplicates

    def test_length_rule(self):
        """Test that bounded sequence rule correctly validates sequence length."""

        # Create length rules with different constraints
        # Using a simple rule (always returns True) for the inner rule
        def simple_rule(seq):
            return True

        from seqrule.dsl import DSLRule

        inner_rule = DSLRule(simple_rule)

        # Create rules with different length constraints
        exactly_3 = create_bounded_sequence_rule(
            min_length=3, max_length=3, inner_rule=inner_rule
        )
        min_2 = create_bounded_sequence_rule(
            min_length=2, max_length=float("inf"), inner_rule=inner_rule
        )
        max_4 = create_bounded_sequence_rule(
            min_length=0, max_length=4, inner_rule=inner_rule
        )
        between_2_and_4 = create_bounded_sequence_rule(
            min_length=2, max_length=4, inner_rule=inner_rule
        )

        # Test sequence
        sequence = [AbstractObject(value=i) for i in range(3)]

        # Test exact length
        assert exactly_3(sequence) is True
        assert exactly_3([AbstractObject(value=1), AbstractObject(value=2)]) is False

        # Test minimum length
        assert min_2(sequence) is True
        assert min_2([AbstractObject(value=1)]) is False

        # Test maximum length
        assert max_4(sequence) is True
        assert max_4([AbstractObject(value=i) for i in range(5)]) is False

        # Test range
        assert between_2_and_4(sequence) is True
        assert between_2_and_4([AbstractObject(value=1)]) is False
        assert between_2_and_4([AbstractObject(value=i) for i in range(5)]) is False

    def test_property_match_rule(self):
        """Test that property match rule correctly validates property values."""
        # Create a rule that checks if all objects have color="red"
        rule = create_property_match_rule("color", "red")

        # Test with all matching values
        matching_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
        ]
        assert rule(matching_sequence) is True

        # Test with non-matching values
        non_matching_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="red"),
        ]
        assert rule(non_matching_sequence) is False

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence has no violations

    def test_alternation_rule(self):
        """Test that alternation rule correctly validates alternating property values."""
        # Create a rule that checks if 'color' values alternate
        rule = create_alternation_rule("color")

        # Test with alternating values
        alternating_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
        ]
        assert rule(alternating_sequence) is True

        # Test with non-alternating values
        non_alternating_sequence = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="blue"),  # Duplicate
            AbstractObject(color="red"),
        ]
        assert rule(non_alternating_sequence) is False

        # Test with single value
        assert rule([AbstractObject(color="red")]) is True

        # Test with empty sequence
        assert rule([]) is True

    def test_numerical_range_rule(self):
        """Test that numerical range rule correctly validates values within a range."""
        # Create a rule that checks if 'value' is between 10 and 20
        rule = create_numerical_range_rule("value", 10, 20)

        # Test with values in range
        in_range_sequence = [
            AbstractObject(value=10),
            AbstractObject(value=15),
            AbstractObject(value=20),
        ]
        assert rule(in_range_sequence) is True

        # Test with values outside range
        out_of_range_sequence = [
            AbstractObject(value=10),
            AbstractObject(value=25),  # Outside range
            AbstractObject(value=15),
        ]
        assert rule(out_of_range_sequence) is False

        # Test with boundary values
        boundary_sequence = [
            AbstractObject(value=10),  # Min boundary
            AbstractObject(value=20),  # Max boundary
        ]
        assert rule(boundary_sequence) is True

        # Test with empty sequence
        assert rule([]) is True

    def test_sum_rule(self):
        """Test that sum rule correctly validates property values summing to a target."""
        # Create a rule that checks if 'value' sums to 10
        rule = create_sum_rule("value", 10, tolerance=0.1)

        # Test with sum exactly matching target
        exact_sum_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=3),
            AbstractObject(value=4),
        ]
        assert rule(exact_sum_sequence) is True

        # Test with sum within tolerance
        within_tolerance_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=3),
            AbstractObject(value=4.05),  # Sum = 10.05, within tolerance
        ]
        assert rule(within_tolerance_sequence) is True

        # Test with sum outside tolerance
        outside_tolerance_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=3),
            AbstractObject(value=5),  # Sum = 11, outside tolerance
        ]
        assert rule(outside_tolerance_sequence) is False

        # Test with empty sequence
        assert rule([]) is True

    def test_historical_rule(self):
        """Test that historical rule correctly validates conditions over sliding windows."""

        # Create a rule that checks if values in each window of 3 are all different
        def all_different(window):
            values = [obj.properties.get("value") for obj in window]
            return len(values) == len(set(values))

        rule = create_historical_rule(3, all_different)

        # Test with all windows having different values
        valid_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
            AbstractObject(value=4),
            AbstractObject(value=5),
        ]
        assert rule(valid_sequence) is True

        # Test with a window having duplicate values
        invalid_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=2),  # Creates a window with duplicate
            AbstractObject(value=3),
        ]
        assert rule(invalid_sequence) is False

        # Test with sequence shorter than window
        short_sequence = [AbstractObject(value=1), AbstractObject(value=2)]
        assert rule(short_sequence) is True  # Too short to check

    def test_transition_rule(self):
        """Test that transition rule correctly validates valid transitions between values."""
        # Create a rule that checks if 'state' transitions follow valid paths
        valid_transitions = {
            "start": {"processing", "error"},
            "processing": {"complete", "error"},
            "error": {"retry", "fail"},
            "retry": {"processing", "fail"},
            "complete": {"archive"},
            "fail": set(),
            "archive": set(),
        }

        rule = create_transition_rule("state", valid_transitions)

        # Test with valid transitions
        valid_sequence = [
            AbstractObject(state="start"),
            AbstractObject(state="processing"),
            AbstractObject(state="complete"),
            AbstractObject(state="archive"),
        ]
        assert rule(valid_sequence) is True

        # Test with invalid transition
        invalid_sequence = [
            AbstractObject(state="start"),
            AbstractObject(state="processing"),
            AbstractObject(state="error"),
            AbstractObject(state="complete"),  # Invalid: error -> complete
        ]
        assert rule(invalid_sequence) is False

        # Test with single state
        assert rule([AbstractObject(state="start")]) is True

        # Test with empty sequence
        assert rule([]) is True

    def test_running_stat_rule(self):
        """Test that running stat rule correctly validates statistics over sliding windows."""

        # Create a rule that checks if the average of 'value' in each window of 3 is between 5 and 15
        def average(values):
            return sum(values) / len(values)

        rule = create_running_stat_rule("value", average, 5, 15, window=3)

        # Test with all windows having averages in range
        valid_sequence = [
            AbstractObject(value=5),
            AbstractObject(value=10),
            AbstractObject(value=15),  # Window avg = 10
            AbstractObject(value=10),  # Window avg = 11.67
        ]
        assert rule(valid_sequence) is True

        # Test with a window having average outside range
        invalid_sequence = [
            AbstractObject(value=5),
            AbstractObject(value=10),
            AbstractObject(value=20),  # Window avg = 11.67
            AbstractObject(value=20),  # Window avg = 16.67 (outside range)
        ]
        assert rule(invalid_sequence) is False

        # Test with sequence shorter than window
        short_sequence = [AbstractObject(value=5), AbstractObject(value=10)]
        assert rule(short_sequence) is True  # Too short to check

    def test_composite_rule(self):
        """Test that composite rule correctly combines multiple rules with AND/OR logic."""
        # Create individual rules
        red_rule = create_property_match_rule("color", "red")
        value_range_rule = create_numerical_range_rule("value", 1, 5)

        # Create composite rules
        all_rule = create_composite_rule([red_rule, value_range_rule], mode="all")
        any_rule = create_composite_rule([red_rule, value_range_rule], mode="any")

        # Test sequences
        both_valid = [
            AbstractObject(color="red", value=3),
            AbstractObject(color="red", value=4),
        ]

        only_red_valid = [
            AbstractObject(color="red", value=10),
            AbstractObject(color="red", value=20),
        ]

        only_range_valid = [
            AbstractObject(color="blue", value=3),
            AbstractObject(color="green", value=4),
        ]

        neither_valid = [
            AbstractObject(color="blue", value=10),
            AbstractObject(color="green", value=20),
        ]

        # Test AND mode
        assert all_rule(both_valid) is True
        assert all_rule(only_red_valid) is False
        assert all_rule(only_range_valid) is False
        assert all_rule(neither_valid) is False

        # Test OR mode
        assert any_rule(both_valid) is True
        assert any_rule(only_red_valid) is True
        assert any_rule(only_range_valid) is True
        assert any_rule(neither_valid) is False

    def test_meta_rule(self):
        """Test that meta rule correctly requires a certain number of rules to be satisfied."""

        # Create rules that check for specific values
        def has_value_1(seq):
            return any(obj.properties.get("value") == 1 for obj in seq)

        def has_value_2(seq):
            return any(obj.properties.get("value") == 2 for obj in seq)

        def has_value_3(seq):
            return any(obj.properties.get("value") == 3 for obj in seq)

        from seqrule.dsl import DSLRule

        rule1 = DSLRule(has_value_1, "has value 1")
        rule2 = DSLRule(has_value_2, "has value 2")
        rule3 = DSLRule(has_value_3, "has value 3")

        # Create meta rule requiring at least 2 of the rules to pass
        meta_rule = create_meta_rule([rule1, rule2, rule3], required_count=2)

        # Test with sequence satisfying exactly 2 rules
        two_rules_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=4),  # Not 3
        ]
        assert meta_rule(two_rules_sequence) is True

        # Test with sequence satisfying only 1 rule
        one_rule_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=4),
            AbstractObject(value=5),
        ]
        assert meta_rule(one_rule_sequence) is False

        # Test with sequence satisfying all 3 rules
        all_rules_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
        ]
        assert meta_rule(all_rules_sequence) is True

    def test_property_cycle_rule(self):
        """Test that property cycle rule correctly validates cyclic property values."""
        # Create a rule that checks if 'color' values form a cycle
        rule = create_property_cycle_rule("color")

        # Test with a simple cycle
        simple_cycle = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
        ]
        assert rule(simple_cycle) is True

        # Test with a broken cycle
        broken_cycle = [
            AbstractObject(color="red"),
            AbstractObject(color="blue"),
            AbstractObject(color="green"),
            AbstractObject(color="red"),
            AbstractObject(color="green"),  # Should be blue
            AbstractObject(color="green"),
        ]
        assert rule(broken_cycle) is False

        # Test with a single value (trivial cycle)
        single_value = [
            AbstractObject(color="red"),
            AbstractObject(color="red"),
            AbstractObject(color="red"),
        ]
        assert rule(single_value) is True

        # Test with empty sequence
        assert rule([]) is True

        # Test with multiple properties
        multi_prop_rule = create_property_cycle_rule("color", "shape")

        multi_prop_cycle = [
            AbstractObject(color="red", shape="circle"),
            AbstractObject(color="blue", shape="square"),
            AbstractObject(color="red", shape="circle"),
            AbstractObject(color="blue", shape="square"),
        ]
        assert multi_prop_rule(multi_prop_cycle) is True

        multi_prop_broken = [
            AbstractObject(color="red", shape="circle"),
            AbstractObject(color="blue", shape="square"),
            AbstractObject(color="red", shape="triangle"),  # Shape breaks cycle
            AbstractObject(color="blue", shape="square"),
        ]
        assert multi_prop_rule(multi_prop_broken) is False

    def test_dependency_rule(self):
        """Test that dependency rule correctly validates dependencies between property values."""
        # Create a rule that checks if 'stage' dependencies are satisfied
        dependencies = {
            "deploy": {"test", "build"},  # deploy requires test and build
            "release": {"deploy", "approve"},  # release requires deploy and approve
        }

        rule = create_dependency_rule("stage", dependencies)

        # Test with all dependencies satisfied
        valid_sequence = [
            AbstractObject(stage="build"),
            AbstractObject(stage="test"),
            AbstractObject(stage="approve"),
            AbstractObject(stage="deploy"),
            AbstractObject(stage="release"),
        ]
        assert rule(valid_sequence) is True

        # Test with missing dependency
        missing_test = [
            AbstractObject(stage="build"),
            # Missing test stage
            AbstractObject(stage="approve"),
            AbstractObject(stage="deploy"),  # Should fail because test is missing
            AbstractObject(stage="release"),
        ]
        assert rule(missing_test) is False

        # Test with missing transitive dependency
        missing_deploy = [
            AbstractObject(stage="build"),
            AbstractObject(stage="test"),
            AbstractObject(stage="approve"),
            # Missing deploy stage
            AbstractObject(stage="release"),  # Should fail because deploy is missing
        ]
        assert rule(missing_deploy) is False

        # Test with no dependent stages
        no_dependent_stages = [
            AbstractObject(stage="build"),
            AbstractObject(stage="test"),
            AbstractObject(stage="approve"),
        ]
        assert rule(no_dependent_stages) is True

        # Test with empty sequence
        assert rule([]) is True

    def test_group_rule(self):
        """Test that group rule correctly validates conditions over groups of consecutive objects."""

        # Create a rule that checks if each pair of consecutive values is in ascending order
        def ascending_pair(group):
            return group[0].properties.get("value") < group[1].properties.get("value")

        rule = create_group_rule(2, ascending_pair)

        # Test with all pairs ascending
        ascending_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=5),
            AbstractObject(value=8),
        ]
        assert rule(ascending_sequence) is True

        # Test with a non-ascending pair
        non_ascending_sequence = [
            AbstractObject(value=1),
            AbstractObject(value=3),
            AbstractObject(value=2),  # Creates a non-ascending pair (3,2)
            AbstractObject(value=5),
        ]
        assert rule(non_ascending_sequence) is False

        # Test with sequence shorter than group size
        short_sequence = [AbstractObject(value=1)]
        assert rule(short_sequence) is True  # Too short to check

        # Test with empty sequence
        assert rule([]) is True

        # Test with larger group size
        def ascending_triplet(group):
            return (
                group[0].properties.get("value")
                < group[1].properties.get("value")
                < group[2].properties.get("value")
            )

        triplet_rule = create_group_rule(3, ascending_triplet)

        # Test with all triplets ascending
        ascending_triplets = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
            AbstractObject(value=4),
            AbstractObject(value=5),
        ]
        assert triplet_rule(ascending_triplets) is True

        # Test with a non-ascending triplet
        non_ascending_triplets = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=3),
            AbstractObject(value=2),  # Creates a non-ascending triplet (2,3,2)
            AbstractObject(value=5),
        ]
        assert triplet_rule(non_ascending_triplets) is False

    def test_ratio_rule(self):
        """Test that ratio rule correctly validates the ratio of objects meeting a condition."""

        # Create a rule that checks if 40-60% of objects have value > 5
        def is_greater_than_five(obj):
            return obj.properties.get("value") > 5

        rule = create_ratio_rule("value", 0.4, 0.6, is_greater_than_five)

        # Test with ratio in range (50%)
        in_range_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=4),
            AbstractObject(value=6),
            AbstractObject(value=7),
        ]
        # 2 out of 4 values are > 5, ratio = 0.5
        assert rule(in_range_sequence) is True

        # Test with ratio too low (25%)
        too_low_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=4),
            AbstractObject(value=5),
            AbstractObject(value=7),
        ]
        # 1 out of 4 values are > 5, ratio = 0.25
        assert rule(too_low_sequence) is False

        # Test with ratio too high (75%)
        too_high_sequence = [
            AbstractObject(value=3),
            AbstractObject(value=6),
            AbstractObject(value=7),
            AbstractObject(value=8),
        ]
        # 3 out of 4 values are > 5, ratio = 0.75
        assert rule(too_high_sequence) is False

        # Test with empty sequence
        assert rule([]) is True

        # Test without filter function (uses first value as reference)
        no_filter_rule = create_ratio_rule("category", 0.4, 0.6)

        balanced_categories = [
            AbstractObject(category="A"),
            AbstractObject(category="A"),
            AbstractObject(category="B"),
            AbstractObject(category="B"),
        ]
        # 2 out of 4 match first value ("A"), ratio = 0.5
        assert no_filter_rule(balanced_categories) is True

        unbalanced_categories = [
            AbstractObject(category="A"),
            AbstractObject(category="B"),
            AbstractObject(category="B"),
            AbstractObject(category="B"),
        ]
        # 1 out of 4 match first value ("A"), ratio = 0.25
        assert no_filter_rule(unbalanced_categories) is False

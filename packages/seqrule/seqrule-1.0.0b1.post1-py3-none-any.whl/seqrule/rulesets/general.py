"""
General purpose sequence rules.

This module provides a collection of commonly useful rule patterns that can be
applied across different domains. These patterns are abstracted from common
use cases seen in specific domains like card games, DNA sequences, music,
and tea processing.

Common use cases:
- Pattern matching and cycles
- Property-based rules
- Numerical constraints
- Historical patterns
- Meta-rules and combinations
"""

from typing import Any, Callable, Dict, List, Optional, Set, TypeVar

from ..core import AbstractObject, Sequence
from ..dsl import DSLRule

T = TypeVar("T")


def create_property_match_rule(property_name: str, value: Any) -> DSLRule:
    """
    Creates a rule requiring objects to have a specific property value.

    Example:
        color_is_red = create_property_match_rule("color", "red")
    """

    def check_property(seq: Sequence) -> bool:
        return all(obj.properties.get(property_name) == value for obj in seq)

    return DSLRule(check_property, f"all objects have {property_name}={value}")


def create_property_cycle_rule(*properties: str) -> DSLRule:
    """
    Creates a rule requiring objects to cycle through property values.

    Example:
        color_cycle = create_property_cycle_rule("color")  # Values must cycle
    """

    def check_cycle(seq: Sequence) -> bool:
        if not seq:
            return True

        for prop in properties:
            try:
                values = [obj.properties.get(prop) for obj in seq]
                if len(values) <= 1:
                    continue

                # Find potential cycle by looking at first occurrence of each value
                seen_values = []
                cycle_found = False
                for value in values:
                    if value in seen_values:
                        # Found potential cycle, verify it matches
                        cycle = seen_values
                        cycle_length = len(cycle)

                        # Check if rest of sequence follows the cycle
                        for i, value in enumerate(values):
                            if value != cycle[i % cycle_length]:
                                return False
                        cycle_found = True
                        break
                    seen_values.append(value)

                # If we get here without finding a cycle, it's invalid
                if not cycle_found:
                    return False

            except TypeError:
                continue  # Skip properties with errors

        return True

    return DSLRule(check_cycle, f"properties {properties} form cycles")


def create_alternation_rule(property_name: str) -> DSLRule:
    """
    Creates a rule requiring alternating property values.

    Example:
        alternating_colors = create_alternation_rule("color")
    """

    def check_alternation(seq: Sequence) -> bool:
        if len(seq) <= 1:
            return True

        for i in range(len(seq) - 1):
            val1 = seq[i].properties.get(property_name)
            val2 = seq[i + 1].properties.get(property_name)
            if val1 is not None and val2 is not None and val1 == val2:
                return False
        return True

    return DSLRule(check_alternation, f"{property_name} values must alternate")


def create_numerical_range_rule(
    property_name: str, min_value: float, max_value: float
) -> DSLRule:
    """
    Creates a rule requiring numerical property values within a range.

    Example:
        valid_temperature = create_numerical_range_rule("temperature", 20, 30)
    """

    def check_range(seq: Sequence) -> bool:
        for obj in seq:
            try:
                value = obj.properties.get(property_name)
                if value is not None:
                    value = float(value)
                    if not (min_value <= value <= max_value):
                        return False
            except (ValueError, TypeError):
                continue  # Skip invalid values
        return True

    return DSLRule(
        check_range, f"{property_name} must be between {min_value} and {max_value}"
    )


def create_sum_rule(
    property_name: str, target: float, tolerance: float = 0.001
) -> DSLRule:
    """
    Creates a rule requiring property values to sum to a target value.

    Example:
        total_duration = create_sum_rule("duration", 60.0)  # Sum to 60
    """

    def check_sum(seq: Sequence) -> bool:
        if not seq:
            return True  # Empty sequence is valid

        values = []
        for obj in seq:
            if property_name not in obj.properties:
                raise ValueError(f"Missing required property: {property_name}")
            try:
                value = float(obj.properties[property_name])
                values.append(value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid value for {property_name}") from e

        total = sum(values)
        return abs(total - target) <= tolerance

    return DSLRule(check_sum, f"sum of {property_name} must be {target}")


def create_pattern_rule(pattern: List[Any], property_name: str) -> DSLRule:
    """
    Creates a rule requiring property values to match a specific pattern.

    Example:
        color_pattern = create_pattern_rule(["red", "black", "red"], "color")
    """

    def check_pattern(seq: Sequence) -> bool:
        if not seq:
            return False

        # If sequence is shorter than pattern, it's valid if it matches the start of the pattern
        if len(seq) < len(pattern):
            values = [obj.properties.get(property_name) for obj in seq]
            return all(values[i] == pattern[i] for i in range(len(values)))

        values = [obj.properties.get(property_name) for obj in seq]
        pattern_length = len(pattern)

        # Check if values match pattern cyclically
        return all(values[i] == pattern[i % pattern_length] for i in range(len(values)))

    return DSLRule(check_pattern, f"{property_name} must match pattern {pattern}")


def create_historical_rule(
    window: int, condition: Callable[[List[AbstractObject]], bool]
) -> DSLRule:
    """
    Creates a rule checking a condition over a sliding window.

    Example:
        def no_repeats(window): return len(set(obj["value"] for obj in window)) == len(window)
        unique_values = create_historical_rule(3, no_repeats)
    """

    def check_historical(seq: Sequence) -> bool:
        if len(seq) < window:
            return True

        for i in range(len(seq) - window + 1):
            try:
                window_seq = seq[i : i + window]
                if not condition(window_seq):
                    return False
            except Exception:  # Catch any error from condition
                continue  # Skip windows with errors
        return True

    return DSLRule(
        check_historical, f"condition must hold over {window}-object windows"
    )


def create_dependency_rule(
    property_name: str, dependencies: Dict[Any, Set[Any]]
) -> DSLRule:
    """
    Creates a rule enforcing dependencies between property values.

    Example:
        stage_deps = create_dependency_rule("stage", {"deploy": {"test", "build"}})
    """

    def check_dependencies(seq: Sequence) -> bool:
        for obj in seq:
            try:
                if property_name not in obj.properties:
                    raise KeyError(property_name)
                value = obj.properties[property_name]
                if value is None:
                    continue
                for dep_value, required_values in dependencies.items():
                    if value == dep_value:
                        for required_value in required_values:
                            if not any(
                                o.properties.get(property_name) == required_value
                                for o in seq
                            ):
                                return False
            except (KeyError, TypeError) as e:
                raise KeyError(property_name) from e
        return True

    return DSLRule(check_dependencies, f"dependencies between {property_name} values")


def create_meta_rule(rules: List[DSLRule], required_count: int) -> DSLRule:
    """
    Creates a rule requiring a certain number of other rules to be satisfied.

    Example:
        any_two = create_meta_rule([rule1, rule2, rule3], 2)  # Any 2 must pass
    """

    def check_meta(seq: Sequence) -> bool:
        if not rules:
            return True  # Empty rule list passes

        passed = sum(1 for rule in rules if rule(seq))
        return passed >= required_count

    return DSLRule(check_meta, f"at least {required_count} rules must be satisfied")


def create_group_rule(
    group_size: int, condition: Callable[[List[AbstractObject]], bool]
) -> DSLRule:
    """
    Creates a rule checking a condition over groups of consecutive objects.

    Example:
        def ascending(group):
            return all(group[i]["value"] < group[i+1]["value"]
                      for i in range(len(group)-1))
        ascending_pairs = create_group_rule(2, ascending)
    """

    def check_groups(seq: Sequence) -> bool:
        if len(seq) < group_size:
            return True

        for i in range(0, len(seq) - group_size + 1):
            try:
                group = seq[i : i + group_size]
                if not condition(group):
                    return False
            except Exception:  # Catch any error from condition
                continue  # Skip groups with errors
        return True

    return DSLRule(check_groups, f"condition must hold for each group of {group_size}")


# Common rule combinations
def create_bounded_sequence_rule(
    min_length: int, max_length: int, inner_rule: DSLRule
) -> DSLRule:
    """
    Creates a rule that combines length constraints with another rule.

    Example:
        valid_sequence = create_bounded_sequence_rule(2, 5, pattern_rule)
    """

    def check_bounded(seq: Sequence) -> bool:
        return min_length <= len(seq) <= max_length and inner_rule(seq)

    return DSLRule(
        check_bounded, f"length {min_length}-{max_length} and {inner_rule.description}"
    )


def create_composite_rule(rules: List[DSLRule], mode: str = "all") -> DSLRule:
    """
    Creates a rule that combines multiple rules with AND/OR logic.

    Example:
        all_rules = create_composite_rule([rule1, rule2], mode="all")
        any_rule = create_composite_rule([rule1, rule2], mode="any")
    """

    def check_composite(seq: Sequence) -> bool:
        results = []
        for rule in rules:
            try:
                result = rule(seq)
                results.append(result)
                if mode == "all" and not result:
                    return False  # Short-circuit AND mode
                if mode == "any" and result:
                    return True  # Short-circuit OR mode
            except Exception:  # Catch any error from rules
                if mode == "all":
                    return False  # Any error fails AND mode
                continue  # Skip errors in OR mode

        if not results:
            return True  # No valid results means pass

        return all(results) if mode == "all" else any(results)

    mode_desc = "all" if mode == "all" else "any"
    return DSLRule(check_composite, f"{mode_desc} of the rules must be satisfied")


def create_ratio_rule(
    property_name: str,
    min_ratio: float,
    max_ratio: float,
    filter_rule: Optional[Callable[[AbstractObject], bool]] = None,
) -> DSLRule:
    """
    Creates a rule requiring a ratio of objects meeting a condition to be within a range.

    Example:
        # At least 40% but no more than 60% GC content
        gc_content = create_ratio_rule("base", 0.4, 0.6, lambda obj: obj["base"] in ["G", "C"])
    """

    def check_ratio(seq: Sequence) -> bool:
        if not seq:
            return True

        # First collect valid objects
        valid_objects = []
        for obj in seq:
            try:
                if property_name not in obj.properties:  # Use properties directly
                    continue
                if obj.properties[property_name] is None:  # Use properties directly
                    continue
                valid_objects.append(obj)
            except Exception:  # Catch any access errors
                continue

        if not valid_objects:
            return True

        # Count matching objects
        if filter_rule is None:
            # Without filter, count objects matching the first value
            first_value = valid_objects[0].properties[
                property_name
            ]  # Use properties directly
            count = sum(
                1
                for obj in valid_objects
                if obj.properties[property_name] == first_value
            )
        else:
            try:
                count = sum(1 for obj in valid_objects if filter_rule(obj))
            except Exception:  # Catch any filter function errors
                return True  # Skip if filter function fails

        total = len(valid_objects)
        ratio = count / total
        return min_ratio <= ratio <= max_ratio

    return DSLRule(
        check_ratio, f"ratio must be between {min_ratio:.1%} and {max_ratio:.1%}"
    )


def create_transition_rule(
    property_name: str, valid_transitions: Dict[Any, Set[Any]]
) -> DSLRule:
    """
    Creates a rule enforcing valid transitions between property values.

    Example:
        # Valid note transitions in a scale
        scale_rule = create_transition_rule("pitch", {
            "C": {"D"}, "D": {"E"}, "E": {"F"}, "F": {"G"},
            "G": {"A"}, "A": {"B"}, "B": {"C"}
        })
    """

    def check_transitions(seq: Sequence) -> bool:
        if len(seq) <= 1:
            return True

        # First check if we have any valid transitions to check
        has_valid_pair = False
        last_valid_value = None

        for obj in seq:
            try:
                value = obj.properties[property_name]
                if value is None:
                    continue

                if last_valid_value is not None:
                    if last_valid_value in valid_transitions:
                        has_valid_pair = True
                        if value not in valid_transitions[last_valid_value]:
                            return False
                last_valid_value = value

            except (KeyError, TypeError):
                continue  # Skip invalid transitions

        # If we found no valid pairs to check, pass
        if not has_valid_pair:
            return True

        return True

    return DSLRule(
        check_transitions, f"transitions between {property_name} values must be valid"
    )


def create_running_stat_rule(
    property_name: str,
    stat_func: Callable[[List[float]], float],
    min_value: float,
    max_value: float,
    window: int,
) -> DSLRule:
    """
    Creates a rule checking a running statistic over a sliding window.

    Example:
        # Moving average of temperatures must be between 20-30
        moving_avg = create_running_stat_rule(
            "temp", lambda x: sum(x)/len(x), 20, 30, window=3
        )
    """

    def check_stat(seq: Sequence) -> bool:
        if len(seq) < window:
            return True

        # Check each window
        for i in range(len(seq) - window + 1):
            window_values = []
            valid_window = True

            # Try to get all values in window
            for obj in seq[i : i + window]:
                try:
                    value = float(obj.properties[property_name])
                    window_values.append(value)
                except (ValueError, TypeError, KeyError):
                    valid_window = False
                    break

            # Skip invalid windows
            if not valid_window or len(window_values) < window:
                continue

            try:
                stat = stat_func(window_values)
                if not (min_value <= stat <= max_value):
                    return False
            except (ValueError, ZeroDivisionError):
                continue

        # If we get here, either all windows were skipped or all were valid
        return True

    return DSLRule(
        check_stat, f"running statistic must be between {min_value} and {max_value}"
    )


def create_unique_property_rule(property_name: str, scope: str = "global") -> DSLRule:
    """
    Creates a rule requiring property values to be unique within a scope.

    Example:
        # No duplicate IDs globally
        unique_ids = create_unique_property_rule("id", scope="global")
        # No adjacent duplicate values
        no_adjacent = create_unique_property_rule("value", scope="adjacent")
    """

    def check_unique(seq: Sequence) -> bool:
        if not seq:
            return True

        if scope == "global":
            values = []
            for obj in seq:
                if property_name not in obj.properties:
                    raise KeyError(property_name)
                values.append(obj.properties[property_name])
            return len(values) == len(set(values))
        elif scope == "adjacent":
            for i in range(len(seq) - 1):
                if (
                    property_name not in seq[i].properties
                    or property_name not in seq[i + 1].properties
                ):
                    raise KeyError(property_name)
                if (
                    seq[i].properties[property_name]
                    == seq[i + 1].properties[property_name]
                ):
                    return False
            return True
        return True

    return DSLRule(
        check_unique, f"{property_name} values must be unique within {scope} scope"
    )


def create_property_trend_rule(
    property_name: str, trend: str = "increasing"
) -> DSLRule:
    """
    Creates a rule requiring property values to follow a trend.

    Example:
        # Values must strictly increase
        increasing = create_property_trend_rule("value", "increasing")
        # Values must be non-increasing
        non_increasing = create_property_trend_rule("value", "non-increasing")
    """

    def check_trend(seq: Sequence) -> bool:
        if len(seq) <= 1:
            return True

        # Collect valid values first
        values = []
        for obj in seq:
            try:
                if property_name not in obj.properties:
                    continue
                value = obj.properties[property_name]
                if value is None:
                    continue
                try:
                    values.append(float(value))
                except (ValueError, TypeError):
                    continue  # Skip non-numeric values
            except Exception:
                continue

        # If we don't have enough valid values, pass
        if len(values) <= 1:
            return True

        # Check trend between consecutive valid values
        for i in range(len(values) - 1):
            current = values[i]
            next_value = values[i + 1]

            if trend == "increasing":
                if not (current < next_value):
                    return False
            elif trend == "decreasing":
                if not (current > next_value):
                    return False
            elif trend == "non-increasing":
                if not (current >= next_value):
                    return False
            elif trend == "non-decreasing":
                if not (next_value >= current):
                    return False

        return True

    return DSLRule(check_trend, f"{property_name} values must be {trend}")


def create_balanced_rule(
    property_name: str, groups: Dict[Any, Set[Any]], tolerance: float = 0.1
) -> DSLRule:
    """
    Creates a rule requiring balanced representation of property value groups.

    Example:
        # Equal number of red and black cards (±10%)
        balanced_colors = create_balanced_rule("color", {
            "red": {"red"}, "black": {"black"}
        })
    """

    def check_balance(seq: Sequence) -> bool:
        if not seq:
            return True

        # Count occurrences in each group
        counts = {group: 0 for group in groups}
        for obj in seq:
            try:
                value = obj.properties[property_name]  # Use properties directly
                if value is None:
                    continue
                for group, members in groups.items():
                    if value in members:
                        counts[group] += 1
            except (KeyError, TypeError):
                continue  # Skip missing or invalid properties

        if not counts or not any(counts.values()):
            return True  # No valid values found

        # Check if counts are balanced within tolerance
        avg = sum(counts.values()) / len(counts)
        max_deviation = max(avg * tolerance, 1)  # Allow at least 1 deviation

        return all(abs(count - avg) <= max_deviation for count in counts.values())

    return DSLRule(check_balance, f"{property_name} groups must be balanced")

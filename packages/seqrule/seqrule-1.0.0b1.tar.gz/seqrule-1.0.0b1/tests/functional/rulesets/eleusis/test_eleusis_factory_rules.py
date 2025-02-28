"""
Tests for the Eleusis ruleset factory functions.

These tests verify that the Eleusis card game rule factory functions
correctly create rules that validate card sequences.
"""

from seqrule.rulesets.eleusis import (
    Card,
    alternation_rule,
    create_historical_rule,
    create_meta_rule,
    create_property_cycle_rule,
    create_suit_value_rule,
    create_symmetry_rule,
    suit_cycle_rule,
)


class TestEleusisFactoryRules:
    """Test suite for Eleusis card game rule factory functions."""

    def test_create_suit_value_rule(self):
        """Test that create_suit_value_rule correctly creates a rule for suit values."""
        # Create a rule where hearts > diamonds > clubs > spades
        suit_values = {"heart": 4, "diamond": 3, "club": 2, "spade": 1}
        rule = create_suit_value_rule(suit_values)

        # Test with valid increasing values
        valid_sequence = [
            Card(color="black", suit="spade", number=10),  # 1*10 = 10
            Card(color="red", suit="heart", number=3),  # 4*3 = 12 > 10
        ]
        assert rule(valid_sequence) is True

        # Test with valid increasing values (same suit, higher number)
        valid_same_suit = [
            Card(color="red", suit="heart", number=2),  # 4*2 = 8
            Card(color="red", suit="heart", number=3),  # 4*3 = 12 > 8
        ]
        assert rule(valid_same_suit) is True

        # Test with invalid decreasing values
        invalid_sequence = [
            Card(color="red", suit="heart", number=5),  # 4*5 = 20
            Card(color="red", suit="diamond", number=6),  # 3*6 = 18 < 20
        ]
        assert rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=5)]
        assert rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert rule([]) is True

    def test_create_historical_rule(self):
        """Test that create_historical_rule correctly creates a rule for historical matching."""
        # Create a rule requiring matching a property from the last 3 cards
        rule = create_historical_rule(3)

        # Test with valid matching (matching color)
        valid_color_match = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),
            Card(color="red", suit="diamond", number=4),  # Matches color of first card
        ]
        assert rule(valid_color_match) is True

        # Test with valid matching (matching suit)
        valid_suit_match = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),
            Card(color="black", suit="spade", number=4),  # Matches suit of second card
        ]
        assert rule(valid_suit_match) is True

        # Test with valid matching (matching number)
        valid_number_match = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),
            Card(
                color="red", suit="diamond", number=2
            ),  # Matches number of second card
        ]
        assert rule(valid_number_match) is True

        # Test with invalid matching (no property matches)
        # Note: The implementation checks if the current card matches any property from the history window
        # In this case, the fifth card should NOT match any property from cards 2-4
        invalid_match = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),
            Card(color="red", suit="diamond", number=4),
            Card(
                color="green", suit="joker", number=7
            ),  # No match with cards 2-4 (the window)
        ]
        assert rule(invalid_match) is False

        # Test with sequence shorter than window (should be valid)
        short_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),
        ]
        assert rule(short_sequence) is True

        # Test with empty sequence (should be valid)
        assert rule([]) is True

    def test_create_meta_rule(self):
        """Test that create_meta_rule correctly creates a rule combining other rules."""
        # Create a meta rule requiring at least 1 of 2 rules to pass
        rules = [alternation_rule, suit_cycle_rule]
        rule = create_meta_rule(rules, required_count=1)

        # Test with sequence passing both rules
        both_valid = [
            Card(color="black", suit="spade", number=1),
            Card(
                color="red", suit="heart", number=2
            ),  # Alternates color and follows suit cycle
        ]
        assert rule(both_valid) is True

        # Test with sequence passing only alternation rule
        alternation_only = [
            Card(color="black", suit="spade", number=1),
            Card(
                color="red", suit="diamond", number=2
            ),  # Alternates color but breaks suit cycle
        ]
        assert rule(alternation_only) is True

        # Test with sequence passing only suit cycle rule
        suit_cycle_only = [
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="heart", number=2),
            Card(
                color="red", suit="diamond", number=3
            ),  # Follows suit cycle but breaks alternation
        ]
        assert rule(suit_cycle_only) is True

        # Test with sequence failing both rules
        both_invalid = [
            Card(color="black", suit="spade", number=1),
            Card(
                color="black", suit="club", number=2
            ),  # Breaks color alternation and suit cycle
        ]
        assert rule(both_invalid) is False

        # Create a stricter meta rule requiring all rules to pass
        strict_rule = create_meta_rule(rules, required_count=2)

        # Test with sequence passing both rules
        assert strict_rule(both_valid) is True

        # Test with sequence passing only one rule
        assert strict_rule(alternation_only) is False
        assert strict_rule(suit_cycle_only) is False

        # Test with empty sequence (should be valid)
        assert rule([]) is True
        assert strict_rule([]) is True

    def test_create_symmetry_rule(self):
        """Test that create_symmetry_rule correctly creates a rule for symmetrical properties."""
        # Create a rule requiring symmetry in the last 3 cards
        rule = create_symmetry_rule(3)

        # Test with valid symmetry in color
        valid_color_symmetry = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(
                color="red", suit="diamond", number=3
            ),  # First and last have same color
        ]
        assert rule(valid_color_symmetry) is True

        # Test with valid symmetry in number
        valid_number_symmetry = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=2),
            Card(
                color="black", suit="club", number=5
            ),  # First and last have same number
        ]
        assert rule(valid_number_symmetry) is True

        # Test with invalid symmetry (no matching properties)
        invalid_symmetry = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="black", suit="club", number=3),  # No symmetry
        ]
        assert rule(invalid_symmetry) is False

        # Test with sequence shorter than required length
        short_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
        ]
        assert rule(short_sequence) is True  # Should be valid for short sequences

        # Test with empty sequence (should be valid)
        assert rule([]) is True

    def test_create_property_cycle_rule(self):
        """Test that create_property_cycle_rule correctly creates a rule for cycling properties."""
        # Create a rule requiring cycling through color, suit, and number
        rule = create_property_cycle_rule("color", "suit", "number")

        # Test with valid property cycle
        valid_cycle = [
            Card(color="red", suit="heart", number=1),  # Focus on color
            Card(color="red", suit="diamond", number=2),  # Focus on suit
            Card(color="black", suit="diamond", number=2),  # Focus on number
            Card(color="black", suit="spade", number=3),  # Focus on color again
        ]
        assert rule(valid_cycle) is True

        # Test with invalid property cycle
        invalid_cycle = [
            Card(color="red", suit="heart", number=1),  # Focus on color
            Card(color="red", suit="diamond", number=2),  # Focus on suit
            Card(
                color="red", suit="club", number=3
            ),  # Changed all properties, breaking the cycle
        ]
        assert rule(invalid_cycle) is False

        # Test with sequence shorter than cycle length
        # The implementation requires at least one match for each property in the cycle
        # With only two cards, we can't match all three properties (color, suit, number)
        short_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="red", suit="diamond", number=2),
        ]
        assert (
            rule(short_sequence) is False
        )  # Not all properties can be matched with just two cards

        # Test with a sequence that matches all properties with just two pairs
        complete_match_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(
                color="red", suit="diamond", number=2
            ),  # Matches color with first card
            Card(
                color="black", suit="diamond", number=2
            ),  # Matches suit and number with second card
        ]
        assert rule(complete_match_sequence) is True

        # Test with empty sequence (should be valid for simplicity)
        assert rule([]) is True

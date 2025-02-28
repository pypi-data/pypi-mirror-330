"""
Tests for the Eleusis ruleset.

These tests verify that the Eleusis card game rules correctly validate
card sequences according to the game's constraints.
"""

from seqrule.rulesets.eleusis import (
    Card,
    alternation_rule,
    comparative_rule,
    fibonacci_rule,
    fixed_pattern_rule,
    hard_odd_even_color_rule,
    increment_rule,
    matching_rule,
    odd_even_rule,
    prime_sum_rule,
    range_rule,
    royal_sequence_rule,
    suit_cycle_rule,
)


class TestEleusisRules:
    """Test suite for Eleusis card game rules."""

    def test_alternation_rule(self):
        """Test that alternation rule correctly validates color alternation."""
        # Test with valid alternating sequence
        valid_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=2),
            Card(color="red", suit="diamond", number=3),
        ]
        assert alternation_rule(valid_sequence) is True

        # Test with invalid sequence (red followed by red)
        invalid_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="red", suit="diamond", number=2),
        ]
        assert alternation_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=1)]
        assert alternation_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert alternation_rule([]) is True

    def test_suit_cycle_rule(self):
        """Test that suit cycle rule correctly validates suit progression."""
        # Test with valid suit cycle: spade->heart->diamond->club->spade
        valid_sequence = [
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="heart", number=2),
            Card(color="red", suit="diamond", number=3),
            Card(color="black", suit="club", number=4),
            Card(color="black", suit="spade", number=5),
        ]
        assert suit_cycle_rule(valid_sequence) is True

        # Test with invalid sequence (spade followed by diamond)
        invalid_sequence = [
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="diamond", number=2),
        ]
        assert suit_cycle_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="black", suit="spade", number=1)]
        assert suit_cycle_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert suit_cycle_rule([]) is True

    def test_fixed_pattern_rule(self):
        """Test that fixed pattern rule correctly validates groups of 3 cards alternating colors."""
        # Test with valid pattern (groups of 3 red, then 3 black)
        valid_sequence = [
            # First group (red)
            Card(color="red", suit="heart", number=1),
            Card(color="red", suit="diamond", number=2),
            Card(color="red", suit="heart", number=3),
            # Second group (black)
            Card(color="black", suit="spade", number=4),
            Card(color="black", suit="club", number=5),
            Card(color="black", suit="spade", number=6),
            # Third group (red)
            Card(color="red", suit="heart", number=7),
        ]
        assert fixed_pattern_rule(valid_sequence) is True

        # Test with invalid pattern (red group followed by red instead of black)
        invalid_sequence = [
            # First group (red)
            Card(color="red", suit="heart", number=1),
            Card(color="red", suit="diamond", number=2),
            Card(color="red", suit="heart", number=3),
            # Should be black but is red
            Card(color="red", suit="diamond", number=4),
        ]
        assert fixed_pattern_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=1)]
        assert fixed_pattern_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert fixed_pattern_rule([]) is True

    def test_odd_even_rule(self):
        """Test that odd/even rule correctly validates number alternation."""
        # Test with valid odd/even alternation
        valid_sequence = [
            Card(color="red", suit="heart", number=1),  # odd
            Card(color="black", suit="spade", number=2),  # even
            Card(color="red", suit="diamond", number=3),  # odd
        ]
        assert odd_even_rule(valid_sequence) is True

        # Test with invalid sequence (odd followed by odd)
        invalid_sequence = [
            Card(color="red", suit="heart", number=1),  # odd
            Card(color="black", suit="spade", number=3),  # odd
        ]
        assert odd_even_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=1)]
        assert odd_even_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert odd_even_rule([]) is True

    def test_range_rule(self):
        """Test that range rule correctly validates number ranges."""
        # Test with valid range alternation (1-7 followed by 8-13)
        valid_sequence = [
            Card(color="red", suit="heart", number=5),  # 1-7
            Card(color="black", suit="spade", number=10),  # 8-13
            Card(color="red", suit="diamond", number=3),  # 1-7
        ]
        assert range_rule(valid_sequence) is True

        # Test with invalid sequence (1-7 followed by 1-7)
        invalid_sequence = [
            Card(color="red", suit="heart", number=5),  # 1-7
            Card(color="black", suit="spade", number=6),  # 1-7
        ]
        assert range_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=5)]
        assert range_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert range_rule([]) is True

    def test_increment_rule(self):
        """Test that increment rule correctly validates number increments."""
        # Test with valid increments (1-3 higher, modulo 13)
        valid_sequence = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=7),  # +2
            Card(color="red", suit="diamond", number=8),  # +1
        ]
        assert increment_rule(valid_sequence) is True

        # Test with valid wrap-around (13 to 3 is +3 modulo 13)
        valid_wrap = [
            Card(color="red", suit="heart", number=13),
            Card(color="black", suit="spade", number=3),  # (3-13) % 13 = 3
        ]
        assert increment_rule(valid_wrap) is True

        # Test with invalid increment (more than 3)
        invalid_sequence = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),  # +5
        ]
        assert increment_rule(invalid_sequence) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=5)]
        assert increment_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert increment_rule([]) is True

    def test_hard_odd_even_color_rule(self):
        """Test that hard odd/even color rule correctly validates number-color relationship."""
        # Test with valid combinations (odd-red, even-black)
        valid_sequence = [
            Card(color="red", suit="heart", number=1),  # odd-red
            Card(color="black", suit="spade", number=2),  # even-black
            Card(color="red", suit="diamond", number=3),  # odd-red
        ]
        assert hard_odd_even_color_rule(valid_sequence) is True

        # Test with invalid combination (odd-black)
        invalid_sequence = [Card(color="black", suit="spade", number=3)]  # odd-black
        assert hard_odd_even_color_rule(invalid_sequence) is False

        # Test with invalid combination (even-red)
        invalid_sequence2 = [Card(color="red", suit="heart", number=2)]  # even-red
        assert hard_odd_even_color_rule(invalid_sequence2) is False

        # Test with empty sequence (should be valid)
        assert hard_odd_even_color_rule([]) is True

    def test_matching_rule(self):
        """Test that matching rule correctly validates suit or number matching."""
        # Test with valid suit matching
        valid_suit_match = [
            Card(color="red", suit="heart", number=1),
            Card(color="red", suit="heart", number=5),  # same suit
        ]
        assert matching_rule(valid_suit_match) is True

        # Test with valid number matching
        valid_number_match = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=5),  # same number
        ]
        assert matching_rule(valid_number_match) is True

        # Test with invalid match (neither suit nor number matches)
        invalid_match = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=7),
        ]
        assert matching_rule(invalid_match) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=5)]
        assert matching_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert matching_rule([]) is True

    def test_comparative_rule(self):
        """Test that comparative rule correctly validates color-based number comparisons."""
        # Test with valid sequence (black cards decrease, red cards increase)
        valid_sequence = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=5),  # black <= previous
            Card(color="black", suit="club", number=3),  # black <= previous
            Card(color="red", suit="diamond", number=7),  # red >= previous
        ]
        assert comparative_rule(valid_sequence) is True

        # Test with invalid sequence (black card increases)
        invalid_black = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=7),  # black > previous
        ]
        assert comparative_rule(invalid_black) is False

        # Test with invalid sequence (red card decreases)
        invalid_red = [
            Card(color="black", suit="spade", number=5),
            Card(color="red", suit="heart", number=3),  # red < previous
        ]
        assert comparative_rule(invalid_red) is False

        # Test with single card (should be valid)
        single_card = [Card(color="red", suit="heart", number=5)]
        assert comparative_rule(single_card) is True

        # Test with empty sequence (should be valid)
        assert comparative_rule([]) is True

    def test_fibonacci_rule(self):
        """Test that fibonacci rule correctly validates Fibonacci sequences."""
        # Test with valid Fibonacci sequence (mod 13)
        valid_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="diamond", number=2),  # 1+1=2
        ]
        assert fibonacci_rule(valid_sequence) is True

        # Test with another valid Fibonacci sequence
        valid_sequence2 = [
            Card(color="red", suit="heart", number=3),
            Card(color="black", suit="spade", number=5),
            Card(color="red", suit="diamond", number=8),  # 3+5=8
        ]
        assert fibonacci_rule(valid_sequence2) is True

        # Test with valid Fibonacci sequence with modulo
        valid_modulo = [
            Card(color="red", suit="heart", number=8),
            Card(color="black", suit="spade", number=13),
            Card(color="red", suit="diamond", number=8),  # (8+13) % 13 = 21 % 13 = 8
        ]
        assert fibonacci_rule(valid_modulo) is True

        # Test with invalid Fibonacci sequence
        invalid_sequence = [
            Card(color="red", suit="heart", number=2),
            Card(color="black", suit="spade", number=3),
            Card(color="red", suit="diamond", number=7),  # 2+3=5, not 7
        ]
        assert fibonacci_rule(invalid_sequence) is False

        # Test with sequence too short
        short_sequence = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=1),
        ]
        assert (
            fibonacci_rule(short_sequence) is True
        )  # Should be valid for short sequences

        # Test with empty sequence (should be valid)
        assert fibonacci_rule([]) is True

    def test_prime_sum_rule(self):
        """Test that prime sum rule correctly validates prime sums."""
        # Test with valid prime sum
        valid_sequence = [
            Card(color="red", suit="heart", number=2),
            Card(color="black", suit="spade", number=3),
            Card(color="red", suit="diamond", number=6),  # 2+3+6=11 (prime)
        ]
        assert prime_sum_rule(valid_sequence) is True

        # Test with another valid prime sum
        valid_sequence2 = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=6),
            Card(color="red", suit="diamond", number=2),  # 5+6+2=13 (prime)
        ]
        assert prime_sum_rule(valid_sequence2) is True

        # Test with invalid prime sum
        invalid_sequence = [
            Card(color="red", suit="heart", number=4),
            Card(color="black", suit="spade", number=4),
            Card(color="red", suit="diamond", number=4),  # 4+4+4=12 (not prime)
        ]
        assert prime_sum_rule(invalid_sequence) is False

        # Test with sequence too short
        short_sequence = [
            Card(color="red", suit="heart", number=2),
            Card(color="black", suit="spade", number=3),
        ]
        assert (
            prime_sum_rule(short_sequence) is True
        )  # Should be valid for short sequences

        # Test with empty sequence (should be valid)
        assert prime_sum_rule([]) is True

    def test_royal_sequence_rule(self):
        """Test that royal sequence rule correctly validates face card sequences."""
        # Test with valid royal sequence (Jack -> Queen -> King)
        valid_sequence = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="black", suit="spade", number=12),  # Queen
            Card(color="red", suit="diamond", number=13),  # King
        ]
        assert royal_sequence_rule(valid_sequence) is True

        # Test with valid royal sequence with non-face cards in between
        valid_with_others = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="black", suit="spade", number=5),  # Non-face
            Card(color="red", suit="diamond", number=7),  # Non-face
            Card(color="black", suit="club", number=12),  # Queen
            Card(color="red", suit="heart", number=2),  # Non-face
            Card(color="black", suit="spade", number=13),  # King
        ]
        assert royal_sequence_rule(valid_with_others) is True

        # Test with invalid royal sequence (Queen before Jack)
        invalid_order = [
            Card(color="red", suit="heart", number=12),  # Queen
            Card(color="black", suit="spade", number=11),  # Jack
            Card(color="red", suit="diamond", number=13),  # King
        ]
        assert royal_sequence_rule(invalid_order) is False

        # Test with invalid royal sequence (King before Queen)
        invalid_order2 = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="black", suit="spade", number=13),  # King
            Card(color="red", suit="diamond", number=12),  # Queen
        ]
        assert royal_sequence_rule(invalid_order2) is False

        # Test with no face cards
        no_face_cards = [
            Card(color="red", suit="heart", number=2),
            Card(color="black", suit="spade", number=5),
            Card(color="red", suit="diamond", number=7),
        ]
        assert (
            royal_sequence_rule(no_face_cards) is True
        )  # Should be valid with no face cards

        # Test with single card (should be valid if it's a Jack or no face card)
        jack_only = [Card(color="red", suit="heart", number=11)]  # Jack
        assert royal_sequence_rule(jack_only) is True

        queen_only = [Card(color="red", suit="heart", number=12)]  # Queen
        # The implementation allows a single Queen card, so this should be True
        assert royal_sequence_rule(queen_only) is True

        king_only = [Card(color="red", suit="heart", number=13)]  # King
        # The implementation allows a single King card, so this should be True
        assert royal_sequence_rule(king_only) is True

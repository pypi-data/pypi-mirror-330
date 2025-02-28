import unittest

from seqrule.dsl import DSLRule
from seqrule.rulesets.eleusis import (
    Card,
    comparative_rule,
    create_historical_rule,
    create_meta_rule,
    create_property_cycle_rule,
    create_suit_value_rule,
    create_symmetry_rule,
    fibonacci_rule,
    prime_sum_rule,
    royal_sequence_rule,
)


class TestEleusisCoverage(unittest.TestCase):
    """Test cases to improve coverage for eleusis.py."""

    def test_comparative_rule(self):
        """Test comparative_rule with various inputs."""
        # Create a sequence of cards with valid comparative relationships
        # Black cards must have numbers <= previous card
        # Red cards must have numbers >= previous card
        cards = [
            Card(color="black", suit="spade", number=10),
            Card(
                color="black", suit="club", number=8
            ),  # Black, number decreases (valid)
            Card(
                color="red", suit="heart", number=9
            ),  # Red, number increases from previous (valid)
            Card(
                color="red", suit="diamond", number=12
            ),  # Red, number increases (valid)
        ]

        # Check that the sequence satisfies the rule
        result = comparative_rule(cards)
        self.assertTrue(result)

        # Create a sequence with invalid comparative relationships
        invalid_cards = [
            Card(color="black", suit="spade", number=5),
            Card(
                color="black", suit="club", number=8
            ),  # Black, number increases (invalid)
            Card(
                color="red", suit="heart", number=6
            ),  # Red, number decreases (invalid)
        ]

        # Check that the sequence does not satisfy the rule
        result = comparative_rule(invalid_cards)
        self.assertFalse(result)

        # Test with a single card (should pass)
        single_card = [Card(color="red", suit="heart", number=10)]
        result = comparative_rule(single_card)
        self.assertTrue(result)

        # Test with an empty sequence (should pass)
        empty_seq = []
        result = comparative_rule(empty_seq)
        self.assertTrue(result)

    def test_fibonacci_rule(self):
        """Test fibonacci_rule with various inputs."""
        # Create a sequence of cards with Fibonacci relationship (mod 13)
        # 1, 1, 2, 3, 5, 8, 13, 8, 8, 3, ...
        cards = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="diamond", number=2),  # 1+1=2 (valid)
            Card(color="black", suit="club", number=3),  # 1+2=3 (valid)
            Card(color="red", suit="heart", number=5),  # 2+3=5 (valid)
        ]

        # Check that the sequence satisfies the rule
        result = fibonacci_rule(cards)
        self.assertTrue(result)

        # Create a sequence with invalid Fibonacci relationship
        invalid_cards = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=1),
            Card(color="red", suit="diamond", number=3),  # 1+1=2, not 3 (invalid)
        ]

        # Check that the sequence does not satisfy the rule
        result = fibonacci_rule(invalid_cards)
        self.assertFalse(result)

        # Test with fewer than 3 cards (should pass)
        short_seq = [
            Card(color="red", suit="heart", number=1),
            Card(color="black", suit="spade", number=1),
        ]
        result = fibonacci_rule(short_seq)
        self.assertTrue(result)

        # Test with modulo 13 (13 ≡ 0 mod 13)
        mod_cards = [
            Card(color="red", suit="heart", number=8),
            Card(color="black", suit="spade", number=5),
            Card(
                color="red", suit="diamond", number=0
            ),  # (8+5) mod 13 = 13 mod 13 = 0 (valid)
        ]

        # Check that the sequence satisfies the rule (since 0 is equivalent to 13 mod 13)
        result = fibonacci_rule(mod_cards)
        self.assertTrue(result)

    def test_prime_sum_rule(self):
        """Test the prime_sum_rule function."""
        # Test with a sequence where the sum of the last three cards is prime
        cards = [
            Card(color="red", suit="heart", number=2),
            Card(color="red", suit="diamond", number=2),
            Card(color="black", suit="spade", number=3),
        ]
        # Sum is 2 + 2 + 3 = 7, which is prime
        assert prime_sum_rule(cards) is True

        # Test with a sequence where the sum of the last three cards is not prime
        cards = [
            Card(color="red", suit="heart", number=2),
            Card(color="red", suit="diamond", number=2),
            Card(color="black", suit="spade", number=4),
        ]
        # Sum is 2 + 2 + 4 = 8, which is not prime
        assert prime_sum_rule(cards) is False

        # Test with a sequence where the sum is less than 2 (to cover line 176)
        cards = [
            Card(color="red", suit="heart", number=0),
            Card(color="red", suit="diamond", number=0),
            Card(color="black", suit="spade", number=1),
        ]
        # Sum is 0 + 0 + 1 = 1, which is not prime (less than 2)
        assert prime_sum_rule(cards) is False

    def test_royal_sequence_rule(self):
        """Test the royal_sequence_rule function."""
        # Test with a valid royal sequence
        cards = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="red", suit="diamond", number=12),  # Queen
            Card(color="black", suit="spade", number=13),  # King
        ]
        assert royal_sequence_rule(cards) is True

        # Test with an invalid royal sequence (Queen followed by non-King)
        # This specifically tests line 203 where Queen must be followed by King
        cards = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="red", suit="diamond", number=12),  # Queen
            Card(color="black", suit="spade", number=11),  # Jack (not King)
        ]
        assert royal_sequence_rule(cards) is False

        # Test with an invalid royal sequence (Jack followed by non-Queen)
        cards = [
            Card(color="red", suit="heart", number=11),  # Jack
            Card(color="red", suit="diamond", number=13),  # King (not Queen)
        ]
        assert royal_sequence_rule(cards) is False

    def test_create_suit_value_rule(self):
        """Test create_suit_value_rule with various inputs."""
        # Create a rule where hearts > diamonds > clubs > spades
        suit_values = {"heart": 4, "diamond": 3, "club": 2, "spade": 1}
        rule = create_suit_value_rule(suit_values)

        # Create a sequence of cards with increasing values
        cards = [
            Card(color="black", suit="spade", number=10),  # Value: 1*10=10
            Card(color="black", suit="club", number=6),  # Value: 2*6=12 > 10 (valid)
            Card(color="red", suit="diamond", number=5),  # Value: 3*5=15 > 12 (valid)
            Card(color="red", suit="heart", number=4),  # Value: 4*4=16 > 15 (valid)
        ]

        # Check that the sequence satisfies the rule
        result = rule(cards)
        self.assertTrue(result)

        # Create a sequence with decreasing values
        invalid_cards = [
            Card(color="red", suit="heart", number=5),  # Value: 4*5=20
            Card(color="red", suit="diamond", number=6),  # Value: 3*6=18 < 20 (invalid)
            Card(color="black", suit="club", number=8),  # Value: 2*8=16 < 18 (invalid)
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(invalid_cards)
        self.assertFalse(result)

        # Test with a single card (should pass)
        single_card = [Card(color="red", suit="heart", number=5)]
        result = rule(single_card)
        self.assertTrue(result)

        # Test with an empty sequence (should pass)
        empty_seq = []
        result = rule(empty_seq)
        self.assertTrue(result)

    def test_create_historical_rule(self):
        """Test create_historical_rule with various inputs."""
        # Create a rule requiring new cards to match a property from the last 2 cards
        rule = create_historical_rule(window=2)

        # Create a sequence where each card matches a property from the historical window
        cards = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
            Card(
                color="red", suit="diamond", number=10
            ),  # Matches number=10 from previous card (valid)
            Card(
                color="black", suit="club", number=5
            ),  # Matches number=5 from first card (valid)
        ]

        # Check that the sequence satisfies the rule
        result = rule(cards)
        self.assertTrue(result)

        # Create a sequence where the last card doesn't match any property from the historical window
        # The window is 2, so we need to check against the 3rd and 4th cards
        invalid_cards = [
            Card(color="red", suit="heart", number=5),  # 1st card
            Card(color="black", suit="spade", number=10),  # 2nd card
            Card(color="red", suit="diamond", number=10),  # 3rd card - in window
            Card(color="black", suit="club", number=7),  # 4th card - in window
            Card(
                color="green", suit="joker", number=9
            ),  # 5th card - doesn't match any property from window
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(invalid_cards)
        self.assertFalse(result)

        # Test with a sequence shorter than the window (should pass)
        short_seq = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
        ]
        result = rule(short_seq)
        self.assertTrue(result)

    def test_create_meta_rule(self):
        """Test create_meta_rule with various inputs."""
        # Create individual rules
        rule1 = DSLRule(
            lambda seq: all(card["color"] == "red" for card in seq), "all red"
        )
        rule2 = DSLRule(
            lambda seq: all(card["suit"] == "heart" for card in seq), "all hearts"
        )
        rule3 = DSLRule(
            lambda seq: all(card["number"] > 5 for card in seq), "all numbers > 5"
        )

        # Create a meta-rule requiring at least 2 of the 3 rules to be satisfied
        meta_rule = create_meta_rule([rule1, rule2, rule3], required_count=2)

        # Create a sequence that satisfies 2 of the 3 rules
        cards = [
            Card(color="red", suit="heart", number=3),
            Card(color="red", suit="heart", number=4),
        ]
        # Satisfies: all red, all hearts, but not all numbers > 5

        # Check that the sequence satisfies the meta-rule
        result = meta_rule(cards)
        self.assertTrue(result)

        # Create a sequence that satisfies only 1 of the 3 rules
        invalid_cards = [
            Card(color="red", suit="diamond", number=3),
            Card(color="red", suit="club", number=4),
        ]
        # Satisfies: all red, but not all hearts or all numbers > 5

        # Check that the sequence does not satisfy the meta-rule
        result = meta_rule(invalid_cards)
        self.assertFalse(result)

        # Create a sequence that satisfies all 3 rules
        all_rules_cards = [
            Card(color="red", suit="heart", number=6),
            Card(color="red", suit="heart", number=7),
        ]
        # Satisfies: all red, all hearts, all numbers > 5

        # Check that the sequence satisfies the meta-rule
        result = meta_rule(all_rules_cards)
        self.assertTrue(result)

    def test_create_symmetry_rule(self):
        """Test create_symmetry_rule with various inputs."""
        # Create a rule requiring symmetry in card properties over a window of 3
        rule = create_symmetry_rule(length=3)

        # Create a sequence with symmetric properties (A-B-A pattern)
        cards = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
            Card(
                color="red", suit="diamond", number=5
            ),  # Matches number=5 from first card (valid)
        ]

        # Check that the sequence satisfies the rule
        result = rule(cards)
        self.assertTrue(result)

        # Create a sequence without symmetric properties
        invalid_cards = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
            Card(
                color="black", suit="club", number=7
            ),  # Doesn't match any property from first card (invalid)
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(invalid_cards)
        self.assertFalse(result)

        # Test with a sequence shorter than the required length (should pass)
        short_seq = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
        ]
        result = rule(short_seq)
        self.assertTrue(result)

        # Test with a longer symmetric sequence (A-B-C-B-A pattern)
        long_sym_rule = create_symmetry_rule(length=5)
        long_sym_cards = [
            Card(color="red", suit="heart", number=5),
            Card(color="black", suit="spade", number=10),
            Card(color="red", suit="diamond", number=7),
            Card(color="black", suit="spade", number=10),  # Matches second card
            Card(color="red", suit="heart", number=5),  # Matches first card
        ]

        # Check that the sequence satisfies the rule
        result = long_sym_rule(long_sym_cards)
        self.assertTrue(result)

    def test_create_property_cycle_rule(self):
        """Test create_property_cycle_rule with various inputs."""
        # Create a rule requiring at least one consecutive pair to match on each property
        rule = create_property_cycle_rule("color", "suit", "number")

        # Create a sequence where consecutive pairs match on all required properties
        cards = [
            Card(color="red", suit="heart", number=5),
            Card(
                color="red", suit="diamond", number=10
            ),  # Matches color=red from previous card
            Card(
                color="black", suit="diamond", number=10
            ),  # Matches suit=diamond and number=10 from previous card
            Card(
                color="black", suit="spade", number=10
            ),  # Matches color=black and number=10 from previous card
        ]

        # Check that the sequence satisfies the rule
        result = rule(cards)
        self.assertTrue(result)

        # Create a sequence where no consecutive pairs match on "suit"
        invalid_cards = [
            Card(color="red", suit="heart", number=5),
            Card(
                color="red", suit="diamond", number=5
            ),  # Matches color=red and number=5 from previous card
            Card(
                color="black", suit="spade", number=5
            ),  # Matches number=5 from previous card
            Card(
                color="black", suit="club", number=10
            ),  # Matches color=black from previous card
        ]
        # No consecutive pair matches on "suit"

        # Check that the sequence does not satisfy the rule
        result = rule(invalid_cards)
        self.assertFalse(result)

        # Test with a sequence shorter than 2 cards (should pass)
        short_seq = [Card(color="red", suit="heart", number=5)]
        result = rule(short_seq)
        self.assertTrue(result)

        # Test with a single property
        single_prop_rule = create_property_cycle_rule("color")
        single_prop_cards = [
            Card(color="red", suit="heart", number=5),
            Card(
                color="red", suit="diamond", number=10
            ),  # Matches color=red from previous card
            Card(color="black", suit="spade", number=7),
        ]

        # Check that the sequence satisfies the rule
        result = single_prop_rule(single_prop_cards)
        self.assertTrue(result)

"""
Tests for the DNA ruleset.

These tests verify that the DNA-specific rule factories create rules that
correctly validate DNA sequences according to biological constraints.
"""

from seqrule import AbstractObject
from seqrule.rulesets.dna import (
    create_complementary_rule,
    create_complexity_rule,
    create_gc_content_rule,
    create_motif_rule,
    create_no_consecutive_rule,
)


class TestDNARules:
    """Test suite for DNA-specific rules."""

    def test_gc_content_rule(self):
        """Test that GC content rule correctly validates DNA sequences based on GC content."""
        # Create a rule that checks if GC content is between 40% and 60%
        rule = create_gc_content_rule(min_percent=40, max_percent=60)

        # Test with 50% GC content
        balanced_sequence = [
            AbstractObject(base="G"),
            AbstractObject(base="C"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
        ]  # 2/4 = 50% GC
        assert rule(balanced_sequence) is True

        # Test with 100% GC content (outside range)
        high_gc_sequence = [
            AbstractObject(base="G"),
            AbstractObject(base="C"),
            AbstractObject(base="G"),
            AbstractObject(base="C"),
        ]  # 4/4 = 100% GC
        assert rule(high_gc_sequence) is False

        # Test with 0% GC content (outside range)
        low_gc_sequence = [
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
        ]  # 0/4 = 0% GC
        assert rule(low_gc_sequence) is False

        # Test empty sequence
        assert rule([]) is False  # Empty sequence has no GC content

    def test_motif_rule(self):
        """Test that motif rule correctly identifies DNA sequence motifs."""
        # Create a rule that checks for the "GATA" motif
        rule = create_motif_rule("GATA")

        # Test with sequence containing the motif
        sequence_with_motif = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="A"),
            AbstractObject(base="C"),
        ]
        assert rule(sequence_with_motif) is True  # GATA found in GATAC

        # Correct sequence with motif
        correct_sequence = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="A"),
        ]
        assert rule(correct_sequence) is True  # GATA found

        # Test with sequence not containing the motif
        sequence_without_motif = [
            AbstractObject(base="A"),
            AbstractObject(base="C"),
            AbstractObject(base="G"),
            AbstractObject(base="T"),
        ]
        assert rule(sequence_without_motif) is False  # GATA not found

    def test_complementary_rule(self):
        """Test that complementary rule correctly identifies complementary sequences."""
        # Create complementary sequence for GAATTC
        complementary_seq = [
            AbstractObject(base="C"),
            AbstractObject(base="T"),
            AbstractObject(base="T"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="G"),
        ]

        # Create rule checking for complementarity to that sequence
        rule = create_complementary_rule(complementary_seq)

        # Test with sequence that is complementary
        matching_sequence = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="T"),
            AbstractObject(base="C"),
        ]
        assert rule(matching_sequence) is True

        # Test with sequence that is not complementary
        non_matching_sequence = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="T"),
            AbstractObject(base="G"),  # Changed C to G
        ]
        assert rule(non_matching_sequence) is False

        # Test with sequence that has wrong length
        wrong_length = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
        ]
        assert rule(wrong_length) is False  # Wrong length

    def test_complexity_rule(self):
        """Test that complexity rule correctly identifies complex DNA sequences."""
        # Create a rule for sequences with minimum complexity
        rule = create_complexity_rule(min_complexity=0.8)

        # Test with high complexity sequence (all different bases)
        high_complexity = [
            AbstractObject(base="G"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="C"),
            AbstractObject(base="G"),
            AbstractObject(base="A"),
        ]
        assert rule(high_complexity) is True

        # Test with low complexity sequence (repeating)
        low_complexity = [
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
        ]
        assert rule(low_complexity) is False

        # Test with sequence too short
        short_sequence = [AbstractObject(base="A"), AbstractObject(base="T")]
        assert rule(short_sequence) is False  # Too short to have high complexity

    def test_no_consecutive_rule(self):
        """Test that no consecutive rule correctly identifies sequences without repeats."""
        # Create a rule that checks for no more than 2 consecutive identical nucleotides
        rule = create_no_consecutive_rule(2)

        # Test with valid sequence (no more than 2 consecutive identical bases)
        valid_sequence = [
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="G"),
            AbstractObject(base="G"),
            AbstractObject(base="C"),
        ]
        assert rule(valid_sequence) is True

        # Test with invalid sequence (3 consecutive As)
        invalid_sequence = [
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="G"),
        ]
        assert rule(invalid_sequence) is False

        # Test with barely valid sequence
        barely_valid = [
            AbstractObject(base="A"),
            AbstractObject(base="A"),
            AbstractObject(base="T"),
            AbstractObject(base="T"),
            AbstractObject(base="G"),
            AbstractObject(base="G"),
        ]
        assert rule(barely_valid) is True  # 2 consecutive bases throughout is allowed

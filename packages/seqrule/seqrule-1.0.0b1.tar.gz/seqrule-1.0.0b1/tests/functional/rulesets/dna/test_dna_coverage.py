"""
Coverage tests for the DNA ruleset.

These tests focus on covering specific lines and edge cases in the DNA ruleset
that aren't covered by the main test suite.
"""

import pytest

from seqrule.rulesets.dna import (
    BaseType,
    MethylationState,
    Nucleotide,
    create_gc_skew_rule,
    create_methylation_rule,
    create_motif_rule,
    create_no_consecutive_rule,
    nucleotide_base_is,
    nucleotide_type_is,
)


class TestDNACoverage:
    """Test suite for DNA ruleset coverage."""

    class TestCore:
        """Core functionality tests."""

        def test_nucleotide_initialization(self):
            """Test that nucleotides can be properly initialized."""
            # Core case: Valid nucleotide
            nucleotide = Nucleotide("A")
            assert nucleotide["base"] == "A"
            assert BaseType.PURINE in nucleotide["types"]
            assert BaseType.WEAK in nucleotide["types"]
            assert BaseType.AMINO in nucleotide["types"]

            # Test repr method
            assert repr(nucleotide) == "Nucleotide(A)"

            # Test predicate functions
            is_a = nucleotide_base_is("A")
            assert is_a(nucleotide) is True

            is_purine = nucleotide_type_is(BaseType.PURINE)
            assert is_purine(nucleotide) is True

        def test_gc_skew_rule(self):
            """Test that GC skew rule correctly validates sequences."""
            # Core case: Valid sequence with acceptable skew
            rule = create_gc_skew_rule(window_size=3, threshold=0.5)

            # Balanced GC content (no skew)
            balanced_sequence = [
                Nucleotide("G"),
                Nucleotide("C"),
                Nucleotide("G"),
                Nucleotide("C"),
            ]
            assert rule(balanced_sequence) is True

        def test_methylation_rule(self):
            """Test that methylation rule correctly validates methylation patterns."""
            # Core case: Correctly methylated CpG sites
            rule = create_methylation_rule(pattern="CG")

            # Sequence with methylated CpG sites
            methylated_sequence = [
                Nucleotide("A"),
                Nucleotide("C", methylation=MethylationState.METHYLATED),
                Nucleotide("G", methylation=MethylationState.METHYLATED),
                Nucleotide("T"),
            ]
            assert rule(methylated_sequence) is True

    class TestEdgeCases:
        """Edge case tests."""

        def test_nucleotide_invalid_base(self):
            """Test that invalid nucleotide bases raise ValueError."""
            # Edge case: Invalid base
            with pytest.raises(
                ValueError, match="Invalid base: X. Must be one of A, T, G, C"
            ):
                Nucleotide("X")

        def test_gc_skew_rule_edge_cases(self):
            """Test edge cases for GC skew rule."""
            # Edge case 1: Sequence shorter than window size
            rule = create_gc_skew_rule(window_size=5, threshold=0.5)
            short_sequence = [Nucleotide("G"), Nucleotide("C"), Nucleotide("A")]
            assert (
                rule(short_sequence) is True
            )  # Should pass for sequences shorter than window

            # Edge case 2: Zero G+C in window
            rule = create_gc_skew_rule(window_size=3, threshold=0.5)
            no_gc_sequence = [
                Nucleotide("A"),
                Nucleotide("T"),
                Nucleotide("A"),
                Nucleotide("T"),
            ]
            assert rule(no_gc_sequence) is True  # Should skip windows with no G or C

            # Edge case 3: High skew (should fail)
            rule = create_gc_skew_rule(window_size=3, threshold=0.2)
            skewed_sequence = [
                Nucleotide("G"),
                Nucleotide("G"),
                Nucleotide("G"),
                Nucleotide("C"),
            ]
            assert rule(skewed_sequence) is False  # High skew should fail

        def test_motif_rule_with_iupac_disabled(self):
            """Test motif rule with IUPAC codes disabled."""
            # Edge case: IUPAC codes disabled
            rule = create_motif_rule("GATA", allow_iupac=False)

            # Create a sequence with the motif
            sequence = [
                Nucleotide("G"),
                Nucleotide("A"),
                Nucleotide("T"),
                Nucleotide("A"),
            ]
            assert rule(sequence) is True

            # This test ensures the code path for allow_iupac=False is covered
            # We can't directly test with IUPAC codes since they're invalid nucleotide bases

        def test_no_consecutive_rule_short_sequence(self):
            """Test no consecutive rule with sequences shorter than count."""
            # Edge case: Sequence shorter than consecutive count
            rule = create_no_consecutive_rule(4)
            short_sequence = [Nucleotide("A"), Nucleotide("A"), Nucleotide("A")]
            assert rule(short_sequence) is True  # Too short to violate rule

    class TestCoverage:
        """Tests specifically designed to increase coverage."""

        def test_methylation_rule_unmethylated(self):
            """Test methylation rule with unmethylated sites."""
            # Coverage: Test with unmethylated CpG site (should fail)
            rule = create_methylation_rule(pattern="CG")

            unmethylated_sequence = [
                Nucleotide("A"),
                Nucleotide("C", methylation=MethylationState.UNMETHYLATED),
                Nucleotide("G", methylation=MethylationState.METHYLATED),
                Nucleotide("T"),
            ]
            assert rule(unmethylated_sequence) is False

        def test_complexity_rule_repeating_sequence(self):
            """Test complexity rule with repeating sequence."""
            # Coverage: Test with repeating sequence (all same base)
            from seqrule.rulesets.dna import create_complexity_rule

            rule = create_complexity_rule(min_complexity=0.5)
            repeating_sequence = [
                Nucleotide("A"),
                Nucleotide("A"),
                Nucleotide("A"),
                Nucleotide("A"),
            ]
            assert rule(repeating_sequence) is False  # All same base = 0 complexity

        def test_complexity_rule_short_sequences(self):
            """Test complexity rule with short sequences."""
            # Coverage: Test with sequences shorter than 3 bases
            from seqrule.rulesets.dna import create_complexity_rule

            rule = create_complexity_rule(min_complexity=0.5)

            # Test with empty sequence
            empty_sequence = []
            assert rule(empty_sequence) is False

            # Test with single base sequence
            single_base = [Nucleotide("A")]
            assert rule(single_base) is False

            # Test with two-base sequence (specifically to cover line 267)
            two_base = [Nucleotide("A"), Nucleotide("T")]
            assert rule(two_base) is False

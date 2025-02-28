"""
Tests for the generators module integration.

These tests verify that the different generator types (lazy, constrained, patterns)
work together correctly and can be used interchangeably.
"""

import pytest

from seqrule import AbstractObject
from seqrule.generators import (
    ConstrainedGenerator,
    Constraint,
    LazyGenerator,
    PropertyPattern,
    generate_counter_examples,
    generate_sequences,
)


@pytest.fixture
def domain():
    """Provide a domain of abstract objects for testing."""
    return [
        AbstractObject(value=1, color="red"),
        AbstractObject(value=2, color="blue"),
        AbstractObject(value=3, color="green"),
    ]


class TestGeneratorIntegration:
    """Test suite for generator integration."""

    def test_lazy_with_constrained_filter(self, domain):
        """Test using a constrained generator's constraint as a filter for a lazy generator."""

        # Create a constraint
        def constraint_func(seq):
            return all(obj["value"] <= 2 for obj in seq)

        # Create a constrained generator with the constraint
        constrained_gen = ConstrainedGenerator(domain)
        constrained_gen.add_constraint(constraint_func)

        # Create a lazy generator with the same constraint as filter
        lazy_gen = LazyGenerator(domain, max_length=2, filter_rule=constraint_func)

        # Generate sequences from both generators
        constrained_sequences = list(constrained_gen.generate(max_length=2))
        lazy_sequences = [lazy_gen() for _ in range(10)]

        # Both should only contain sequences where all values are <= 2
        for seq in constrained_sequences:
            assert all(obj["value"] <= 2 for obj in seq)

        for seq in lazy_sequences:
            if seq:  # Skip empty sequence
                assert all(obj["value"] <= 2 for obj in seq)

    def test_pattern_with_multiple_generators(self, domain):
        """Test using the same pattern with different generator types."""
        # Create a pattern for alternating colors
        pattern = PropertyPattern("color", ["red", "blue"], is_cyclic=True)

        # Create a constrained generator with the pattern
        constrained_gen = ConstrainedGenerator(domain)
        constrained_gen.add_pattern(pattern)

        # Create a filter function based on the pattern
        def pattern_filter(seq):
            return pattern.matches(seq)

        # Create a lazy generator with the pattern filter
        lazy_gen = LazyGenerator(domain, max_length=3, filter_rule=pattern_filter)

        # Generate sequences from both generators
        constrained_sequences = list(constrained_gen.generate(max_length=3))
        lazy_sequences = [lazy_gen() for _ in range(10)]

        # Both should only contain sequences with alternating red and blue
        for seq in constrained_sequences:
            if len(seq) >= 2:
                for i in range(len(seq) - 1):
                    if i % 2 == 0:
                        assert seq[i]["color"] == "red"
                        assert seq[i + 1]["color"] == "blue"
                    else:
                        assert seq[i]["color"] == "blue"
                        assert seq[i + 1]["color"] == "red"

        for seq in lazy_sequences:
            if len(seq) >= 2:
                for i in range(len(seq) - 1):
                    if i % 2 == 0:
                        assert seq[i]["color"] == "red"
                        assert seq[i + 1]["color"] == "blue"
                    else:
                        assert seq[i]["color"] == "blue"
                        assert seq[i + 1]["color"] == "red"

    def test_counter_examples_with_constrained_generator(self, domain):
        """Test generating counter examples using constraints."""

        # Create a rule that requires all values to be even
        def even_constraint_func(seq):
            return all(obj["value"] % 2 == 0 for obj in seq)

        # Create a DSL rule
        from seqrule import DSLRule

        rule = DSLRule(even_constraint_func)

        # Generate counter examples
        counter_examples = generate_counter_examples(rule, domain, max_length=2)

        # Should have counter examples (sequences with odd values)
        assert len(counter_examples) > 0
        for seq in counter_examples:
            assert not all(obj["value"] % 2 == 0 for obj in seq)
            assert any(obj["value"] % 2 != 0 for obj in seq)

    def test_generate_sequences_with_pattern_constraint(self, domain):
        """Test generating sequences with both pattern and constraint."""
        # Create a pattern for red objects
        red_pattern = PropertyPattern("color", ["red"], is_cyclic=True)

        # Create a constraint for even values
        def even_constraint_func(seq):
            return all(obj["value"] % 2 == 0 for obj in seq)

        # Create a filter combining both
        def combined_filter(seq):
            return red_pattern.matches(seq) and even_constraint_func(seq)

        # Generate sequences
        sequences = generate_sequences(
            domain, max_length=2, filter_rule=combined_filter
        )

        # Check that all sequences satisfy both conditions
        for seq in sequences:
            if seq:  # Skip empty sequence
                assert all(obj["color"] == "red" for obj in seq)
                assert all(obj["value"] % 2 == 0 for obj in seq)

    def test_constraint_object_with_generators(self, domain):
        """Test using Constraint objects with different generators."""
        # Create a Constraint object
        constraint = Constraint(
            property_name="value",
            condition=lambda x: x > 1,
            description="Value must be greater than 1",
        )

        # Create a filter function using the constraint
        def constraint_filter(seq):
            return all(constraint(obj["value"]) for obj in seq)

        # Create a lazy generator with the constraint filter
        lazy_gen = LazyGenerator(domain, max_length=2, filter_rule=constraint_filter)

        # Generate sequences
        sequences = [lazy_gen() for _ in range(10)]

        # Check that all sequences satisfy the constraint
        for seq in sequences:
            if seq:  # Skip empty sequence
                assert all(obj["value"] > 1 for obj in seq)

"""
Unit tests for the constrained sequence generation functionality.
"""

import pytest

from seqrule import AbstractObject
from seqrule.generators import ConstrainedGenerator, PropertyPattern


@pytest.fixture
def card_domain():
    """A domain of playing card-like objects."""
    return [
        AbstractObject(color="red", suit="heart", value=1),
        AbstractObject(color="red", suit="diamond", value=2),
        AbstractObject(color="black", suit="spade", value=3),
        AbstractObject(color="black", suit="club", value=4),
    ]


def test_constrained_generator_creation(card_domain):
    """Test creating a constrained generator."""
    generator = ConstrainedGenerator(card_domain)

    # Should have empty constraints and patterns initially
    assert len(generator.constraints) == 0
    assert len(generator.patterns) == 0


def test_add_constraint(card_domain):
    """Test adding constraints to a generator."""
    generator = ConstrainedGenerator(card_domain)

    # Create and add a constraint
    def constraint_func(seq):
        return all(obj["value"] <= 3 for obj in seq)

    generator.add_constraint(constraint_func)

    # Should have one constraint
    assert len(generator.constraints) == 1

    # Should return self for chaining
    result = generator.add_constraint(lambda seq: len(seq) <= 3)
    assert result is generator
    assert len(generator.constraints) == 2


def test_add_pattern(card_domain):
    """Test adding patterns to a generator."""
    generator = ConstrainedGenerator(card_domain)

    # Create and add a pattern
    pattern = PropertyPattern("color", ["red", "black"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Should have one pattern
    assert len(generator.patterns) == 1

    # Should return self for chaining
    result = generator.add_pattern(
        PropertyPattern("suit", ["heart", "spade"], is_cyclic=True)
    )
    assert result is generator
    assert len(generator.patterns) == 2


def test_satisfies_constraints(card_domain):
    """Test checking if a sequence satisfies all constraints."""
    generator = ConstrainedGenerator(card_domain)

    # Add some constraints
    def even_values_constraint(seq):
        return all(obj["value"] % 2 == 0 for obj in seq)  # Only even values

    generator.add_constraint(even_values_constraint)

    def length_constraint(seq):
        return len(seq) <= 2  # Length limit

    generator.add_constraint(length_constraint)

    # Check various sequences
    assert generator._satisfies_constraints([]) is True  # Empty sequence satisfies all

    # Sequence with only even values, length <= 2
    assert generator._satisfies_constraints([card_domain[1]]) is True  # value=2

    # Sequence with odd values, should not satisfy
    assert generator._satisfies_constraints([card_domain[0]]) is False  # value=1

    # Sequence too long
    long_seq = [card_domain[1], card_domain[1], card_domain[1]]  # 3 cards with value=2
    assert generator._satisfies_constraints(long_seq) is False


def test_satisfies_patterns(card_domain):
    """Test checking if a sequence satisfies all patterns."""
    generator = ConstrainedGenerator(card_domain)

    # Add a color alternation pattern
    pattern = PropertyPattern("color", ["red", "black"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Check sequences
    assert generator._satisfies_patterns([]) is True  # Empty sequence matches

    # Valid alternating sequence
    valid_seq = [card_domain[0], card_domain[2]]  # red, black
    assert generator._satisfies_patterns(valid_seq) is True

    # Invalid sequence (red, red)
    invalid_seq = [card_domain[0], card_domain[1]]
    assert generator._satisfies_patterns(invalid_seq) is False


def test_predict_next(card_domain):
    """Test predicting next possible items in a sequence."""
    generator = ConstrainedGenerator(card_domain)

    # Add color alternation pattern
    pattern = PropertyPattern("color", ["red", "black"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Add constraint: values must be ascending
    def ascending_values(seq):
        return all(seq[i]["value"] < seq[i + 1]["value"] for i in range(len(seq) - 1))

    generator.add_constraint(ascending_values)

    # Start with empty sequence - should predict all red cards
    candidates = generator.predict_next([])
    assert len(candidates) == 2  # Two red cards
    assert all(obj["color"] == "red" for obj in candidates)

    # After a red card, should predict black cards with higher value
    red_card = [obj for obj in card_domain if obj["color"] == "red"][0]
    candidates = generator.predict_next([red_card])
    assert len(candidates) == 2  # Two black cards
    assert all(obj["color"] == "black" for obj in candidates)
    assert all(obj["value"] > red_card["value"] for obj in candidates)


def test_generate(card_domain):
    """Test generating sequences with constraints and patterns."""
    generator = ConstrainedGenerator(card_domain)

    # Add pattern: alternate red and black
    pattern = PropertyPattern("color", ["red", "black"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Add constraint: values must be ascending
    def ascending_values(seq):
        return all(seq[i]["value"] < seq[i + 1]["value"] for i in range(len(seq) - 1))

    generator.add_constraint(ascending_values)

    # Generate some sequences
    sequences = list(generator.generate(max_length=3))

    # Should have generated some sequences
    assert len(sequences) > 0

    # All sequences should satisfy the constraints and patterns
    for seq in sequences:
        # Check length
        assert len(seq) <= 3

        # Check ascending values
        if len(seq) > 1:
            assert all(
                seq[i]["value"] < seq[i + 1]["value"] for i in range(len(seq) - 1)
            )

        # Check alternating colors
        if len(seq) > 1:
            assert all(
                seq[i]["color"] != seq[i + 1]["color"] for i in range(len(seq) - 1)
            )


def test_generate_with_constraints_only(card_domain):
    """Test generating sequences with constraints but no patterns."""
    generator = ConstrainedGenerator(card_domain)

    # Add constraint: only red cards
    generator.add_constraint(lambda seq: all(obj["color"] == "red" for obj in seq))

    # Generate sequences
    sequences = list(generator.generate(max_length=2))

    # Should have generated some sequences
    assert len(sequences) > 0

    # All sequences should only have red cards
    for seq in sequences:
        assert all(obj["color"] == "red" for obj in seq)


def test_generate_with_patterns_only(card_domain):
    """Test generating sequences with patterns but no constraints."""
    generator = ConstrainedGenerator(card_domain)

    # Add pattern: alternate suits
    pattern = PropertyPattern("suit", ["heart", "spade"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Generate sequences
    sequences = list(generator.generate(max_length=2))

    # Should have generated some sequences
    assert len(sequences) > 0

    # All sequences should follow the pattern
    for seq in sequences:
        if len(seq) >= 1:
            assert seq[0]["suit"] == "heart"
        if len(seq) >= 2:
            assert seq[1]["suit"] == "spade"


def test_generate_with_max_length_edge_cases(card_domain):
    """Test generating sequences with edge cases for max_length."""
    generator = ConstrainedGenerator(card_domain)

    # Test with max_length=0 (should only yield empty sequence)
    sequences = list(generator.generate(max_length=0))
    assert len(sequences) == 1
    assert len(sequences[0]) == 0

    # Test with empty domain (should yield empty sequence)
    empty_generator = ConstrainedGenerator([])
    sequences = list(empty_generator.generate(max_length=3))
    assert len(sequences) == 1
    assert len(sequences[0]) == 0

    # Test with a constraint that rejects all sequences
    generator.add_constraint(lambda seq: False)
    sequences = list(generator.generate(max_length=3))
    assert len(sequences) == 0  # No sequences should satisfy the constraint


def test_generate_with_no_valid_candidates(card_domain):
    """Test generating sequences when there are no valid candidates for the next position."""
    generator = ConstrainedGenerator(card_domain)

    # Add a pattern that can't be satisfied after the first element
    # First must be heart, second must be diamond, but we don't have a diamond in the domain
    pattern = PropertyPattern("suit", ["heart", "diamond"], is_cyclic=False)
    generator.add_pattern(pattern)

    # Filter the domain to only include hearts
    heart_domain = [obj for obj in card_domain if obj["suit"] == "heart"]
    heart_generator = ConstrainedGenerator(heart_domain)
    heart_generator.add_pattern(pattern)

    # Generate sequences - should only get sequences of length 0 or 1
    sequences = list(heart_generator.generate(max_length=3))
    assert all(len(seq) <= 1 for seq in sequences)


def test_generate_with_failing_constraints(card_domain):
    """Test generating sequences with constraints that fail for some candidates."""
    generator = ConstrainedGenerator(card_domain)

    # Add a constraint that only accepts the first candidate but rejects others
    first_candidate = card_domain[0]
    first_suit = first_candidate["suit"]

    # This constraint will pass for the first candidate but fail for others
    def selective_constraint(seq):
        if not seq:
            return True
        # Only accept sequences where all elements have the same suit as the first candidate
        return all(obj["suit"] == first_suit for obj in seq)

    generator.add_constraint(selective_constraint)

    # Generate sequences
    sequences = list(generator.generate(max_length=2))

    # Should have generated some sequences
    assert len(sequences) > 0

    # All sequences should only contain elements with the first suit
    for seq in sequences:
        if seq:  # Skip empty sequence
            assert all(obj["suit"] == first_suit for obj in seq)


def test_generate_with_pattern_constraint_interaction(card_domain):
    """Test generating sequences with both patterns and constraints that interact."""
    generator = ConstrainedGenerator(card_domain)

    # Add a pattern that requires alternating suits
    heart_suit = "heart"
    spade_suit = "spade"
    pattern = PropertyPattern("suit", [heart_suit, spade_suit], is_cyclic=True)
    generator.add_pattern(pattern)

    # Add a constraint that requires values to be in ascending order
    def ascending_values(seq):
        if len(seq) <= 1:
            return True
        return all(seq[i]["value"] < seq[i + 1]["value"] for i in range(len(seq) - 1))

    generator.add_constraint(ascending_values)

    # Generate sequences
    sequences = list(generator.generate(max_length=3))

    # Verify that all sequences satisfy both the pattern and constraint
    for seq in sequences:
        # Skip empty sequence
        if len(seq) >= 1:
            # Check pattern: alternating suits
            for i, obj in enumerate(seq):
                expected_suit = heart_suit if i % 2 == 0 else spade_suit
                assert obj["suit"] == expected_suit

        # Check constraint: ascending values
        if len(seq) > 1:
            for i in range(len(seq) - 1):
                assert seq[i]["value"] < seq[i + 1]["value"]


def test_generate_with_no_candidates_at_intermediate_step(card_domain):
    """Test generating sequences when there are no candidates at an intermediate step."""
    generator = ConstrainedGenerator(card_domain)

    # Create a custom constraint that will allow the first element but make predict_next return empty list
    # for the second position
    original_predict_next = generator.predict_next

    def modified_predict_next(sequence):
        # For sequences of length 1, return empty list to trigger the branch
        if len(sequence) == 1:
            return []
        # Otherwise use the original implementation
        return original_predict_next(sequence)

    # Replace the predict_next method with our modified version
    generator.predict_next = modified_predict_next

    # Generate sequences
    sequences = list(generator.generate(max_length=3))

    # Should have the empty sequence and sequences of length 1, but none of length 2
    assert any(len(seq) == 0 for seq in sequences)
    assert any(len(seq) == 1 for seq in sequences)
    assert not any(len(seq) == 2 for seq in sequences)

    # Restore the original method
    generator.predict_next = original_predict_next


def test_generate_with_always_empty_candidates(card_domain):
    """Test generating sequences when predict_next always returns empty list."""
    generator = ConstrainedGenerator(card_domain)

    # Save the original method
    original_predict_next = generator.predict_next

    # Replace with a version that always returns empty list
    generator.predict_next = lambda seq: []

    # Generate sequences - should only get the empty sequence
    sequences = list(generator.generate(max_length=3))

    # Should only have the empty sequence
    assert len(sequences) == 1
    assert len(sequences[0]) == 0

    # Restore the original method
    generator.predict_next = original_predict_next


def test_generate_with_candidate_failing_patterns(card_domain):
    """Test generating sequences when a candidate passes constraints but fails patterns."""
    generator = ConstrainedGenerator(card_domain)

    # Add a pattern that requires alternating suits
    pattern = PropertyPattern("suit", ["heart", "spade"], is_cyclic=True)
    generator.add_pattern(pattern)

    # Save the original methods
    original_satisfies_constraints = generator._satisfies_constraints
    original_satisfies_patterns = generator._satisfies_patterns

    # Replace with versions that have specific behavior
    # Always pass constraints, but fail patterns for specific sequences
    def modified_satisfies_constraints(seq):
        return True

    def modified_satisfies_patterns(seq, start_idx=0):
        # Pass for empty sequence and sequences of length 1
        if len(seq) <= 1:
            return True
        # Fail for sequences of length 2 where the second element is a diamond
        if len(seq) == 2 and seq[1]["suit"] == "diamond":
            return False
        # Otherwise use original implementation
        return original_satisfies_patterns(seq, start_idx)

    # Replace the methods
    generator._satisfies_constraints = modified_satisfies_constraints
    generator._satisfies_patterns = modified_satisfies_patterns

    # Generate sequences
    sequences = list(generator.generate(max_length=2))

    # Should have sequences but none with a diamond as the second element
    assert any(len(seq) == 1 for seq in sequences)
    assert not any(len(seq) == 2 and seq[1]["suit"] == "diamond" for seq in sequences)

    # Restore the original methods
    generator._satisfies_constraints = original_satisfies_constraints
    generator._satisfies_patterns = original_satisfies_patterns

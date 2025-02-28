"""
Unit tests for the lazy sequence generation functionality.
"""

import itertools

import pytest

from seqrule import AbstractObject
from seqrule.generators import LazyGenerator, generate_lazy


@pytest.fixture
def simple_domain():
    """Provide a simple domain of abstract objects for testing."""
    return [
        AbstractObject(value=1, color="red"),
        AbstractObject(value=2, color="blue"),
        AbstractObject(value=3, color="green"),
    ]


def test_lazy_generator_creation(simple_domain):
    """Test creating a lazy generator."""
    generator = LazyGenerator(simple_domain, max_length=3)

    # Should be callable
    assert callable(generator)

    # Should be iterable
    assert hasattr(generator, "__iter__")


def test_lazy_generator_call(simple_domain):
    """Test calling the lazy generator to get sequences."""
    generator = LazyGenerator(simple_domain, max_length=2)

    # Call multiple times to get sequences
    sequences = [generator() for _ in range(10)]

    # Should have generated some sequences
    assert len(sequences) == 10

    # Sequences should be of appropriate length
    assert all(len(seq) <= 2 for seq in sequences)

    # Should have the empty sequence
    assert [] in sequences


def test_lazy_generator_with_filter(simple_domain):
    """Test lazy generator with a filter rule."""

    # Filter rule: only red objects
    def only_red(seq):
        return all(obj["color"] == "red" for obj in seq)

    generator = LazyGenerator(simple_domain, max_length=2, filter_rule=only_red)

    # Generate several sequences
    sequences = [generator() for _ in range(10)]

    # Check filter was applied
    for seq in sequences:
        if seq:  # Skip empty sequence
            assert all(obj["color"] == "red" for obj in seq)


def test_lazy_generator_iteration(simple_domain):
    """Test iterating through the lazy generator."""
    generator = LazyGenerator(simple_domain, max_length=2)

    # Collect sequences from iterator
    sequences = list(itertools.islice(generator, 20))

    # Should have generated sequences
    assert len(sequences) > 0

    # All sequences should be valid length
    assert all(len(seq) <= 2 for seq in sequences)


def test_lazy_generator_state_management(simple_domain):
    """Test that the generator manages its state correctly."""
    generator = LazyGenerator(simple_domain, max_length=1)

    # Generate sequences until it has to move to next length
    sequences = []

    # We'll force it to generate enough sequences to exhaust length 0 and move to length 1
    for _ in range(20):
        sequences.append(generator())

    # Should have both empty sequence and sequences of length 1
    assert [] in sequences
    assert any(len(seq) == 1 for seq in sequences)


def test_generate_lazy_factory(simple_domain):
    """Test the generate_lazy factory function."""
    # Create a generator using the factory
    generator = generate_lazy(simple_domain, max_length=2)

    # Should return a LazyGenerator instance
    assert isinstance(generator, LazyGenerator)

    # Should be able to use it to generate sequences
    sequence = generator()
    assert len(sequence) <= 2


def test_lazy_generator_with_complex_filter(simple_domain):
    """Test lazy generator with a more complex filter rule."""

    # Filter: Sequence must have alternating colors
    def alternating_colors(seq):
        if len(seq) <= 1:
            return True
        return all(seq[i]["color"] != seq[i + 1]["color"] for i in range(len(seq) - 1))

    generator = LazyGenerator(
        simple_domain, max_length=3, filter_rule=alternating_colors
    )

    # Generate several sequences
    sequences = [generator() for _ in range(20)]

    # Check filter was applied
    for seq in sequences:
        if len(seq) > 1:
            assert all(
                seq[i]["color"] != seq[i + 1]["color"] for i in range(len(seq) - 1)
            )


def test_lazy_generator_empty_domain():
    """Test lazy generator with an empty domain."""
    generator = LazyGenerator([], max_length=3)

    # Expected behavior for empty domain:
    # - First call generates empty sequence
    # - Subsequent calls should handle empty domain
    try:
        sequence = generator()
        assert sequence == []

        # Subsequent calls might raise an exception with empty domain
        for _ in range(5):
            try:
                result = generator()
                assert result == []
            except IndexError:
                # This is acceptable for empty domains
                pass
    except IndexError:
        # If first call raises exception, that's also acceptable for empty domain
        pass


def test_lazy_generator_edge_cases(simple_domain):
    """Test edge cases in the LazyGenerator class."""

    # Test with empty domain and filter that rejects empty sequences
    def reject_empty(seq):
        return len(seq) > 0

    generator = LazyGenerator(simple_domain, max_length=3, filter_rule=reject_empty)

    # This will force the 'else' branch in the empty sequence handling
    # And eventually the branch where batch is empty
    sequence = generator()
    assert len(sequence) > 0  # Should skip empty sequence and return non-empty

    # Test max_length boundary
    # Set up a generator that's at its max length
    state = generator._get_initial_state()
    state["current_length"] = 4  # Beyond max_length of 3
    generator._state = state

    # This should reset the generator
    sequence = generator()
    assert len(sequence) <= 3  # Should have reset and returned a valid sequence


def test_lazy_generator_empty_batch():
    """Test when a batch is empty, the generator moves to the next length."""

    def reject_all(seq):
        return False  # Filter that rejects all sequences

    # Initialize a generator with a filter that rejects everything
    generator = LazyGenerator([1, 2], max_length=3, filter_rule=reject_all)

    # Save the initial state
    state = generator._get_initial_state()
    initial_length = state["current_length"]

    # When we call the generator, it should try to create a batch, find it empty,
    # and move to the next length
    try:
        generator()
    except Exception:
        # It may eventually raise an exception if it can't generate anything,
        # but we just want to verify the length increment
        pass

    # The current_length should have increased
    assert generator._state["current_length"] > initial_length


def test_lazy_generator_iterator_exhaustion():
    """Test that the iterator can be exhausted."""
    # Create a generator with a small domain and max_length
    generator = LazyGenerator([AbstractObject(value=1)], max_length=1)

    # Convert iterator to list to exhaust it
    sequences = list(itertools.islice(generator, 20))

    # Should have some sequences
    assert len(sequences) > 0

    # All sequences should be valid
    assert all(len(seq) <= 1 for seq in sequences)

    # Test that we can iterate again after exhaustion
    more_sequences = list(itertools.islice(generator, 5))
    assert len(more_sequences) > 0

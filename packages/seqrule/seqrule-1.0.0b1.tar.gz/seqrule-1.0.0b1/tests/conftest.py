"""
Shared fixtures for the SeqRule test suite.

This module provides fixtures that can be used across multiple test files.
"""

import pytest
import os
import sys

# Add the root directory to the Python path so we can import from scripts/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seqrule import AbstractObject


@pytest.fixture
def basic_sequence():
    """Create a basic sequence of abstract objects."""
    return [
        AbstractObject(value=1, color="red", size="small"),
        AbstractObject(value=2, color="blue", size="medium"),
        AbstractObject(value=3, color="green", size="large"),
    ]


@pytest.fixture
def empty_sequence():
    """Create an empty sequence."""
    return []


@pytest.fixture
def nested_properties_sequence():
    """Create a sequence with nested property structures."""
    return [
        AbstractObject(
            value=1,
            metadata={"type": "important", "priority": 1},
            nested={"deep": {"value": 10}},
        ),
        AbstractObject(
            value=2, metadata={"type": "normal", "priority": 2}, tags=["tag1", "tag2"]
        ),
        AbstractObject(
            value=3,
            metadata={"type": "important", "priority": 3},
            nested={"deep": {"value": 30}},
        ),
    ]


@pytest.fixture
def varying_size_sequences():
    """Create sequences of different sizes for testing scalability."""
    sequences = []
    for size in [5, 10, 20]:
        seq = [AbstractObject(value=i, index=i) for i in range(size)]
        sequences.append(seq)
    return sequences

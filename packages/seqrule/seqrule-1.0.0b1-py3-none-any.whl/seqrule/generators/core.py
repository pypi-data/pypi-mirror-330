"""
Core sequence generation functions.

This module provides the main functions for generating sequences,
including generate_sequences and generate_counter_examples.
"""

import random
from typing import List

from ..core import AbstractObject, FormalRule, Sequence


def generate_counter_examples(
    rule: FormalRule,
    domain: List[AbstractObject],
    max_length: int,
    max_attempts: int = 1000,
) -> List[Sequence]:
    """
    Generate sequences that don't satisfy the rule.

    Args:
        rule: The rule to generate counter-examples for
        domain: Domain of objects to choose from
        max_length: Maximum length of generated sequences
        max_attempts: Maximum number of generation attempts

    Returns:
        List of sequences that don't satisfy the rule
    """
    counter_examples = []
    attempts = 0

    while attempts < max_attempts and len(counter_examples) < 5:
        # Generate a random sequence
        length = random.randint(1, max_length)
        sequence = random.choices(domain, k=length)

        # Check if it's a counter-example
        if not rule(sequence):
            counter_examples.append(sequence)

        attempts += 1

    return counter_examples


def generate_sequences(domain, max_length=10, filter_rule=None):
    """
    Generate sequences from a domain of objects.

    Args:
        domain: List of objects to generate sequences from
        max_length: Maximum length of generated sequences
        filter_rule: Optional rule to filter generated sequences

    Returns:
        List of valid sequences
    """
    sequences = []

    # Empty sequence is always included if no filter or it passes the filter
    if not filter_rule or filter_rule([]):
        sequences.append([])

    # Generate sequences of length 1..max_length
    for length in range(1, max_length + 1):
        # Generate all sequences of this length
        for _ in range(min(100, 10**length)):  # Limit number of sequences per length
            # Generate a random sequence of this length
            sequence = random.choices(domain, k=length)

            # Apply filter if provided
            if not filter_rule or filter_rule(sequence):
                sequences.append(sequence)

            # Stop if we have enough sequences
            if len(sequences) >= 100:
                return sequences

    return sequences

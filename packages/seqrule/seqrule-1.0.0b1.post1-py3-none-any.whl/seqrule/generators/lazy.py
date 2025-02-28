"""
Lazy sequence generation.

This module provides functionality for lazy sequence generation,
which only generates sequences as they are requested.
"""

import random


class LazyGenerator:
    """
    Generator that lazily produces sequences.

    This generator only creates sequences when they are requested, making
    it more memory efficient for large domains or long sequences.
    """

    def __init__(self, domain, max_length=10, filter_rule=None):
        """
        Initialize with generation parameters.

        Args:
            domain: List of objects to generate sequences from
            max_length: Maximum length of generated sequences
            filter_rule: Optional rule to filter generated sequences
        """
        self.domain = domain
        self.max_length = max_length
        self.filter_rule = filter_rule
        self._state = self._get_initial_state()

    def _get_initial_state(self):
        """Get the initial generator state."""
        return {"generated": 0, "current_length": 0, "current_batch": []}

    def __call__(self):
        """Generate the next sequence."""
        # Shortcut if we've already generated some for this length
        if self._state["current_batch"]:
            return self._state["current_batch"].pop()

        # If we've reached the max length, start over
        if self._state["current_length"] > self.max_length:
            self._state = self._get_initial_state()

        # Try to generate a sequence of the current length
        length = self._state["current_length"]

        # Empty sequence is a special case
        if length == 0:
            self._state["current_length"] = 1
            if not self.filter_rule or self.filter_rule([]):
                return []
            else:
                return self()

        # Generate a batch of sequences for this length
        batch_size = min(10, 100 // length)  # Generate fewer longer sequences
        batch = []

        for _ in range(batch_size * 10):  # Try harder for filtered sequences
            if len(batch) >= batch_size:
                break

            sequence = random.choices(self.domain, k=length)

            if not self.filter_rule or self.filter_rule(sequence):
                batch.append(sequence)

        # If we couldn't generate any, move to next length
        if not batch:
            self._state["current_length"] += 1
            return self()

        # Store the batch and return one
        self._state["current_batch"] = batch[:-1]
        self._state["generated"] += len(batch)

        # If we've generated enough sequences of this length, move to next length
        if self._state["generated"] >= 10 * (length + 1):
            self._state["current_length"] += 1
            self._state["generated"] = 0

        return batch[-1]

    def __iter__(self):
        """Return an iterator that generates sequences."""
        for length in range(self.max_length + 1):
            # Yield a batch for each length
            for _ in range(
                min(100, 10**length)
            ):  # Limit number of sequences per length
                yield self()


def generate_lazy(domain, max_length=10, filter_rule=None):
    """
    Create a lazy sequence generator.

    Args:
        domain: List of objects to generate sequences from
        max_length: Maximum length of generated sequences
        filter_rule: Optional rule to filter generated sequences

    Returns:
        LazyGenerator instance
    """
    return LazyGenerator(domain, max_length, filter_rule)

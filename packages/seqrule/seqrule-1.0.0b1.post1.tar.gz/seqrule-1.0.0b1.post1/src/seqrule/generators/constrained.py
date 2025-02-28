"""
Constrained sequence generation.

This module provides functionality for generating sequences
that satisfy a set of constraints.
"""

import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, Union

from ..core import AbstractObject, Sequence
from .patterns import PropertyPattern

T = TypeVar("T")


@dataclass
class GeneratorConfig:
    """Configuration options for constrained generators."""

    max_attempts: int = 100
    randomize_candidates: bool = True
    max_candidates_per_step: int = 10
    backtracking_enabled: bool = False


class ConstrainedGenerator:
    """Generator that produces sequences satisfying constraints and patterns."""

    def __init__(
        self,
        domain: List[Union[Dict[str, Any], AbstractObject]],
        config: Optional[GeneratorConfig] = None,
    ):
        """
        Initialize with a domain of possible objects.

        Args:
            domain: List of objects that can be included in the sequence
            config: Optional configuration settings for the generator
        """
        # Normalize domain to ensure all items are AbstractObjects
        self.domain = [
            obj if isinstance(obj, AbstractObject) else AbstractObject(**obj)
            for obj in domain
        ]
        self.constraints: List[Callable[[Sequence], bool]] = []
        self.patterns: List[PropertyPattern] = []
        self.config = config or GeneratorConfig()

    def add_constraint(
        self, constraint: Callable[[Sequence], bool]
    ) -> "ConstrainedGenerator":
        """
        Add a constraint function that the generated sequences must satisfy.

        Args:
            constraint: A function that takes a sequence and returns True if the constraint is satisfied

        Returns:
            Self for method chaining
        """
        self.constraints.append(constraint)
        return self

    def add_pattern(self, pattern: PropertyPattern) -> "ConstrainedGenerator":
        """
        Add a property pattern that the generated sequences must follow.

        Args:
            pattern: A PropertyPattern instance defining a pattern to match

        Returns:
            Self for method chaining
        """
        self.patterns.append(pattern)
        return self

    def _satisfies_constraints(self, sequence: Sequence) -> bool:
        """Check if the sequence satisfies all constraints."""
        return all(constraint(sequence) for constraint in self.constraints)

    def _satisfies_patterns(self, sequence: Sequence, start_idx: int = 0) -> bool:
        """Check if the sequence satisfies all patterns starting from start_idx."""
        return all(pattern.matches(sequence, start_idx) for pattern in self.patterns)

    def predict_next(self, sequence: Sequence) -> List[AbstractObject]:
        """
        Predict the next possible items in the sequence.

        Returns a list of possible next items that would satisfy all
        constraints and patterns.

        Args:
            sequence: The current sequence to predict next items for

        Returns:
            List of candidate objects that could be appended to the sequence
        """
        if not sequence:
            # Empty sequence - return all domain items that satisfy constraints
            return [
                item
                for item in self.domain
                if self._satisfies_constraints([item])
                and self._satisfies_patterns([item])
            ]

        # Try each domain item as a potential next item
        candidates = []
        for item in self.domain:
            # Create a new sequence with this item added
            new_sequence = sequence + [item]

            # Check if it satisfies constraints and patterns
            if self._satisfies_constraints(new_sequence) and self._satisfies_patterns(
                new_sequence, len(sequence) - 1
            ):
                candidates.append(item)

        return candidates

    def generate(self, max_length: int = 10) -> Iterator[Sequence]:
        """
        Generate sequences satisfying all constraints and patterns.

        Args:
            max_length: Maximum length of generated sequences

        Yields:
            Valid sequences of increasing length
        """
        # Start with empty sequence
        sequences_to_process = [[]]

        while sequences_to_process:
            current = sequences_to_process.pop(0)

            # Yield if valid
            if self._satisfies_constraints(current) and self._satisfies_patterns(
                current
            ):
                yield current

            # Stop extending if we've reached max length
            if len(current) >= max_length:
                continue

            # Get candidates for the next position
            candidates = self.predict_next(current)
            if not candidates:
                # No valid candidates to extend this sequence
                continue

            # Randomize order to get variety
            if self.config.randomize_candidates:
                shuffled = list(candidates)
                random.shuffle(shuffled)

                # Limit the number of candidates if configured
                if self.config.max_candidates_per_step > 0:
                    shuffled = shuffled[: self.config.max_candidates_per_step]
            else:
                shuffled = candidates

            # Add new sequences to process
            for candidate in shuffled:
                new_sequence = current + [candidate]
                if self._satisfies_constraints(
                    new_sequence
                ) and self._satisfies_patterns(
                    new_sequence
                ):  # pragma: no branch
                    sequences_to_process.append(new_sequence)

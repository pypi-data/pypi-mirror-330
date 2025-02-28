"""
Pattern-based sequence generation.

This module provides functionality for pattern-based sequence generation
and pattern matching.
"""

from typing import Any, Dict, List


class PropertyPattern:
    """
    Represents a pattern of property values to match or generate from.

    A PropertyPattern tracks values of a specific property across a sequence,
    and can be used to verify patterns or predict next values.
    """

    def __init__(self, property_name: str, values: List[Any], is_cyclic: bool = False):
        """
        Initialize a property pattern.

        Args:
            property_name: The name of the property to track
            values: The expected sequence of values for this property
            is_cyclic: Whether the pattern repeats cyclically
        """
        self.property_name = property_name
        self.values = values
        self.is_cyclic = is_cyclic

    def _get_property_value(self, obj: Any) -> Any:
        """Get property value from either AbstractObject or dict."""
        if hasattr(obj, "properties"):
            return obj.properties.get(self.property_name)
        elif hasattr(obj, "__getitem__"):
            try:
                return obj[self.property_name]
            except (KeyError, TypeError):
                return None
        return getattr(obj, self.property_name, None)

    def matches(self, sequence: List[Dict[str, Any]], start_idx: int = 0) -> bool:
        """Check if the sequence matches the pattern starting from start_idx."""
        if not sequence:
            return True

        # For cyclic patterns, we need to check each position relative to the pattern start
        if self.is_cyclic:
            # Special case for single-value patterns
            if len(self.values) == 1:
                expected_value = self.values[0]
                return all(
                    self._get_property_value(obj) == expected_value
                    for obj in sequence[start_idx:]
                )

            # Check each position against the pattern
            pattern_pos = 0
            for i in range(start_idx, len(sequence)):
                obj = sequence[i]
                expected_value = self.values[pattern_pos]
                actual_value = self._get_property_value(obj)

                if actual_value != expected_value:
                    return False

                # Move to next position in pattern, wrapping around if needed
                pattern_pos = (pattern_pos + 1) % len(self.values)

            return True
        else:
            # Non-cyclic pattern: must match exactly
            pattern_length = len(self.values)
            remaining_length = len(sequence) - start_idx

            # Pattern is longer than remaining sequence
            if pattern_length > remaining_length:
                return False

            # Check each position against the pattern
            for i in range(pattern_length):
                obj = sequence[start_idx + i]
                expected_value = self.values[i]
                actual_value = self._get_property_value(obj)

                if actual_value != expected_value:
                    return False

            return True

    def get_next_value(self, sequence: List[Dict[str, Any]]) -> Any:
        """Predict the next value based on the pattern and current sequence."""
        if not self.values:
            return None

        # For single-value patterns, always return that value
        if len(self.values) == 1:
            return self.values[0]

        # For cyclic patterns, calculate the next position
        if self.is_cyclic:
            next_pos = len(sequence) % len(self.values)
            return self.values[next_pos]

        # For non-cyclic patterns, if we've reached the end, return None
        matched_length = min(len(sequence), len(self.values))
        if matched_length >= len(self.values):
            return None

        # Otherwise, return the next value in the pattern
        return self.values[matched_length]

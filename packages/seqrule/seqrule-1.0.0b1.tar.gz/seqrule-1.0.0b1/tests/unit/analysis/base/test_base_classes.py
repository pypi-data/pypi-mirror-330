"""
Tests for the base classes and enums in the analysis module.

These tests verify that the fundamental types used throughout the analysis system
work correctly, including complexity classes, property access types, and utility classes.
"""

import pytest

from seqrule.analysis.base import (
    AnalysisError,
    ComplexityClass,
    ComplexityScore,
    PropertyAccess,
    PropertyAccessType,
    ValidatedAccessTypeSet,
)


class TestComplexityClass:
    """Test suite for the ComplexityClass enum."""

    def test_ordering(self):
        """Test that ComplexityClass instances can be compared correctly."""
        # Test less than
        assert ComplexityClass.CONSTANT < ComplexityClass.LINEAR
        assert ComplexityClass.LINEAR < ComplexityClass.QUADRATIC
        assert ComplexityClass.QUADRATIC < ComplexityClass.EXPONENTIAL
        assert ComplexityClass.EXPONENTIAL < ComplexityClass.FACTORIAL

        # Test less than or equal
        assert ComplexityClass.CONSTANT <= ComplexityClass.CONSTANT
        assert ComplexityClass.LINEAR <= ComplexityClass.QUADRATIC

        # Test greater than
        assert ComplexityClass.FACTORIAL > ComplexityClass.EXPONENTIAL
        assert ComplexityClass.EXPONENTIAL > ComplexityClass.CUBIC
        assert ComplexityClass.CUBIC > ComplexityClass.QUADRATIC
        assert ComplexityClass.QUADRATIC > ComplexityClass.LINEAR

        # Test greater than or equal
        assert ComplexityClass.FACTORIAL >= ComplexityClass.FACTORIAL
        assert ComplexityClass.EXPONENTIAL >= ComplexityClass.CUBIC

    def test_string_representation(self):
        """Test that ComplexityClass instances have correct string representations."""
        assert str(ComplexityClass.CONSTANT) == "O(1)"
        assert str(ComplexityClass.LOGARITHMIC) == "O(log n)"
        assert str(ComplexityClass.LINEAR) == "O(n)"
        assert str(ComplexityClass.LINEARITHMIC) == "O(n log n)"
        assert str(ComplexityClass.QUADRATIC) == "O(n²)"
        assert str(ComplexityClass.CUBIC) == "O(n³)"
        assert str(ComplexityClass.EXPONENTIAL) == "O(2ⁿ)"
        assert str(ComplexityClass.FACTORIAL) == "O(n!)"


class TestPropertyAccessType:
    """Test suite for the PropertyAccessType enum."""

    def test_enum_values(self):
        """Test that PropertyAccessType has the expected values."""
        assert PropertyAccessType.READ is not None
        assert PropertyAccessType.CONDITIONAL is not None
        assert PropertyAccessType.COMPARISON is not None
        assert PropertyAccessType.METHOD is not None
        assert PropertyAccessType.NESTED is not None

        # Ensure they're all different
        access_types = [
            PropertyAccessType.READ,
            PropertyAccessType.CONDITIONAL,
            PropertyAccessType.COMPARISON,
            PropertyAccessType.METHOD,
            PropertyAccessType.NESTED,
        ]
        assert len(set(access_types)) == 5


class TestValidatedAccessTypeSet:
    """Test suite for the ValidatedAccessTypeSet class."""

    def test_valid_additions(self):
        """Test that valid PropertyAccessType values can be added."""
        access_set = ValidatedAccessTypeSet()

        # Add valid types
        access_set.add(PropertyAccessType.READ)
        access_set.add(PropertyAccessType.CONDITIONAL)

        # Check that they were added
        assert PropertyAccessType.READ in access_set
        assert PropertyAccessType.CONDITIONAL in access_set
        assert len(access_set) == 2

    def test_invalid_additions(self):
        """Test that invalid values cannot be added."""
        access_set = ValidatedAccessTypeSet()

        # Try to add invalid types
        with pytest.raises(ValueError):
            access_set.add("READ")  # String instead of enum

        with pytest.raises(ValueError):
            access_set.add(123)  # Integer instead of enum


class TestPropertyAccess:
    """Test suite for the PropertyAccess class."""

    def test_initialization(self):
        """Test that PropertyAccess instances can be properly initialized."""
        # Basic initialization
        access = PropertyAccess(name="value")
        assert access.name == "value"
        assert access.access_count == 0
        assert isinstance(access.access_types, ValidatedAccessTypeSet)
        assert len(access.access_types) == 0
        assert len(access.nested_properties) == 0

        # Add access types
        access.access_types.add(PropertyAccessType.READ)
        assert PropertyAccessType.READ in access.access_types

        # Add nested properties
        access.nested_properties.add("nested_prop")
        assert "nested_prop" in access.nested_properties

        # Increment access count
        access.access_count += 1
        assert access.access_count == 1


class TestComplexityScore:
    """Test suite for the ComplexityScore enum."""

    def test_ordering(self):
        """Test that ComplexityScore instances can be compared correctly."""
        # Test less than
        assert ComplexityScore.TRIVIAL < ComplexityScore.SIMPLE
        assert ComplexityScore.SIMPLE < ComplexityScore.MODERATE
        assert ComplexityScore.MODERATE < ComplexityScore.COMPLEX
        assert ComplexityScore.COMPLEX < ComplexityScore.VERY_COMPLEX
        assert ComplexityScore.VERY_COMPLEX < ComplexityScore.EXTREME

        # Test less than or equal
        assert ComplexityScore.TRIVIAL <= ComplexityScore.TRIVIAL
        assert ComplexityScore.SIMPLE <= ComplexityScore.MODERATE

        # Test greater than
        assert ComplexityScore.EXTREME > ComplexityScore.VERY_COMPLEX
        assert ComplexityScore.VERY_COMPLEX > ComplexityScore.COMPLEX
        assert ComplexityScore.COMPLEX > ComplexityScore.MODERATE
        assert ComplexityScore.MODERATE > ComplexityScore.SIMPLE
        assert ComplexityScore.SIMPLE > ComplexityScore.TRIVIAL

        # Test greater than or equal
        assert ComplexityScore.EXTREME >= ComplexityScore.EXTREME
        assert ComplexityScore.VERY_COMPLEX >= ComplexityScore.COMPLEX


class TestAnalysisError:
    """Test suite for the AnalysisError exception."""

    def test_error_creation(self):
        """Test that AnalysisError instances can be created with messages."""
        error = AnalysisError("Test error message")
        assert str(error) == "Test error message"

        # Test raising the error
        with pytest.raises(AnalysisError) as excinfo:
            raise AnalysisError("Custom error")
        assert "Custom error" in str(excinfo.value)

"""
Tests for the base module in the analysis package.

This module tests the base classes and enums used throughout the analysis system.
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
    """Test the ComplexityClass enum and its comparison methods."""

    def test_complexity_class_ordering(self):
        """Test that ComplexityClass instances can be compared correctly."""
        # Test less than
        assert ComplexityClass.CONSTANT < ComplexityClass.LINEAR
        assert ComplexityClass.LINEAR < ComplexityClass.QUADRATIC
        assert ComplexityClass.QUADRATIC < ComplexityClass.CUBIC
        assert ComplexityClass.CUBIC < ComplexityClass.EXPONENTIAL
        assert ComplexityClass.EXPONENTIAL < ComplexityClass.FACTORIAL

        # Test less than or equal
        assert ComplexityClass.CONSTANT <= ComplexityClass.CONSTANT
        assert ComplexityClass.LINEAR <= ComplexityClass.LINEAR
        assert ComplexityClass.LINEAR <= ComplexityClass.QUADRATIC

        # Test greater than
        assert ComplexityClass.FACTORIAL > ComplexityClass.EXPONENTIAL
        assert ComplexityClass.EXPONENTIAL > ComplexityClass.CUBIC
        assert ComplexityClass.CUBIC > ComplexityClass.QUADRATIC
        assert ComplexityClass.QUADRATIC > ComplexityClass.LINEAR
        assert ComplexityClass.LINEAR > ComplexityClass.CONSTANT

        # Test greater than or equal
        assert ComplexityClass.FACTORIAL >= ComplexityClass.FACTORIAL
        assert ComplexityClass.EXPONENTIAL >= ComplexityClass.EXPONENTIAL
        assert ComplexityClass.FACTORIAL >= ComplexityClass.EXPONENTIAL

    def test_complexity_class_comparison_with_non_complexity(self):
        """Test comparison with non-ComplexityClass objects."""
        # These should return NotImplemented, which Python then handles
        # by trying the reverse operation or raising TypeError
        with pytest.raises(TypeError):
            assert ComplexityClass.LINEAR < "not a complexity class"

        with pytest.raises(TypeError):
            assert ComplexityClass.LINEAR <= "not a complexity class"

        with pytest.raises(TypeError):
            assert ComplexityClass.LINEAR > "not a complexity class"

        with pytest.raises(TypeError):
            assert ComplexityClass.LINEAR >= "not a complexity class"

    def test_complexity_class_string_representation(self):
        """Test the string representation of ComplexityClass."""
        assert str(ComplexityClass.CONSTANT) == "O(1)"
        assert str(ComplexityClass.LOGARITHMIC) == "O(log n)"
        assert str(ComplexityClass.LINEAR) == "O(n)"
        assert str(ComplexityClass.LINEARITHMIC) == "O(n log n)"
        assert str(ComplexityClass.QUADRATIC) == "O(n²)"
        assert str(ComplexityClass.CUBIC) == "O(n³)"
        assert str(ComplexityClass.EXPONENTIAL) == "O(2ⁿ)"
        assert str(ComplexityClass.FACTORIAL) == "O(n!)"


class TestPropertyAccessType:
    """Test the PropertyAccessType enum."""

    def test_property_access_types(self):
        """Test that all expected PropertyAccessType values exist."""
        assert PropertyAccessType.READ
        assert PropertyAccessType.CONDITIONAL
        assert PropertyAccessType.COMPARISON
        assert PropertyAccessType.METHOD
        assert PropertyAccessType.NESTED


class TestValidatedAccessTypeSet:
    """Test the ValidatedAccessTypeSet class."""

    def test_valid_access_type(self):
        """Test adding valid PropertyAccessType to the set."""
        access_set = ValidatedAccessTypeSet()
        access_set.add(PropertyAccessType.READ)
        access_set.add(PropertyAccessType.CONDITIONAL)

        assert PropertyAccessType.READ in access_set
        assert PropertyAccessType.CONDITIONAL in access_set
        assert len(access_set) == 2

    def test_invalid_access_type(self):
        """Test adding invalid types raises ValueError."""
        access_set = ValidatedAccessTypeSet()

        with pytest.raises(ValueError):
            access_set.add("not a property access type")

        with pytest.raises(ValueError):
            access_set.add(123)


class TestPropertyAccess:
    """Test the PropertyAccess dataclass."""

    def test_property_access_initialization(self):
        """Test initializing PropertyAccess with default and custom values."""
        # Default initialization
        access = PropertyAccess(name="test_property")
        assert access.name == "test_property"
        assert isinstance(access.access_types, ValidatedAccessTypeSet)
        assert access.access_count == 0
        assert access.nested_properties == set()

        # Custom initialization
        access_types = ValidatedAccessTypeSet()
        access_types.add(PropertyAccessType.READ)

        access = PropertyAccess(
            name="custom_property",
            access_types=access_types,
            access_count=5,
            nested_properties={"nested1", "nested2"},
        )

        assert access.name == "custom_property"
        assert access.access_types == access_types
        assert access.access_count == 5
        assert access.nested_properties == {"nested1", "nested2"}


class TestComplexityScore:
    """Test the ComplexityScore enum and its comparison methods."""

    def test_complexity_score_ordering(self):
        """Test that ComplexityScore instances can be compared correctly."""
        # Test less than
        assert ComplexityScore.TRIVIAL < ComplexityScore.SIMPLE
        assert ComplexityScore.SIMPLE < ComplexityScore.MODERATE
        assert ComplexityScore.MODERATE < ComplexityScore.COMPLEX
        assert ComplexityScore.COMPLEX < ComplexityScore.VERY_COMPLEX
        assert ComplexityScore.VERY_COMPLEX < ComplexityScore.EXTREME

        # Test less than or equal
        assert ComplexityScore.TRIVIAL <= ComplexityScore.TRIVIAL
        assert ComplexityScore.SIMPLE <= ComplexityScore.SIMPLE
        assert ComplexityScore.SIMPLE <= ComplexityScore.MODERATE

        # Test greater than
        assert ComplexityScore.EXTREME > ComplexityScore.VERY_COMPLEX
        assert ComplexityScore.VERY_COMPLEX > ComplexityScore.COMPLEX
        assert ComplexityScore.COMPLEX > ComplexityScore.MODERATE
        assert ComplexityScore.MODERATE > ComplexityScore.SIMPLE
        assert ComplexityScore.SIMPLE > ComplexityScore.TRIVIAL

        # Test greater than or equal
        assert ComplexityScore.EXTREME >= ComplexityScore.EXTREME
        assert ComplexityScore.VERY_COMPLEX >= ComplexityScore.VERY_COMPLEX
        assert ComplexityScore.EXTREME >= ComplexityScore.VERY_COMPLEX

    def test_complexity_score_comparison_with_non_score(self):
        """Test comparison with non-ComplexityScore objects."""
        # These should return NotImplemented, which Python then handles
        # by trying the reverse operation or raising TypeError
        with pytest.raises(TypeError):
            assert ComplexityScore.MODERATE < "not a complexity score"

        with pytest.raises(TypeError):
            assert ComplexityScore.MODERATE <= "not a complexity score"

        with pytest.raises(TypeError):
            assert ComplexityScore.MODERATE > "not a complexity score"

        with pytest.raises(TypeError):
            assert ComplexityScore.MODERATE >= "not a complexity score"


class TestAnalysisError:
    """Test the AnalysisError exception."""

    def test_analysis_error(self):
        """Test that AnalysisError can be raised with a message."""
        error_message = "Test analysis error"

        with pytest.raises(AnalysisError) as excinfo:
            raise AnalysisError(error_message)

        assert str(excinfo.value) == error_message

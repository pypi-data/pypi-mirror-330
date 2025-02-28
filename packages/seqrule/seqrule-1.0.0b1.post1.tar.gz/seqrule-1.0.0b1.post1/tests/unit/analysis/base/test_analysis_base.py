"""
Tests for the analysis base module.

These tests focus on the base classes and enums in the analysis module,
particularly targeting edge cases and methods that may not be covered
by other tests.
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


class TestComplexityClassEdgeCases:
    """Test edge cases for the ComplexityClass enum."""

    def test_complexity_class_comparison_with_non_enum(self):
        """Test comparing ComplexityClass with non-enum values."""
        # Should handle comparison with non-enum values gracefully
        assert not (ComplexityClass.LINEAR == "O(n)")
        assert ComplexityClass.LINEAR != "O(n)"

        # Test with None
        assert ComplexityClass.LINEAR is not None
        assert ComplexityClass.LINEAR is not None

        # Test with integers
        assert not (ComplexityClass.LINEAR == 1)
        assert ComplexityClass.LINEAR != 1

    def test_complexity_class_hash(self):
        """Test that ComplexityClass instances can be hashed."""
        # Create a dictionary with ComplexityClass keys
        complexity_dict = {
            ComplexityClass.CONSTANT: "Constant time",
            ComplexityClass.LINEAR: "Linear time",
            ComplexityClass.QUADRATIC: "Quadratic time",
        }

        # Test dictionary access
        assert complexity_dict[ComplexityClass.CONSTANT] == "Constant time"
        assert complexity_dict[ComplexityClass.LINEAR] == "Linear time"
        assert complexity_dict[ComplexityClass.QUADRATIC] == "Quadratic time"

        # Test set operations
        complexity_set = {ComplexityClass.CONSTANT, ComplexityClass.LINEAR}
        assert ComplexityClass.CONSTANT in complexity_set
        assert ComplexityClass.LINEAR in complexity_set
        assert ComplexityClass.QUADRATIC not in complexity_set


class TestPropertyAccessTypeEdgeCases:
    """Test edge cases for the PropertyAccessType enum."""

    def test_property_access_type_comparison(self):
        """Test comparing PropertyAccessType with other values."""
        # Should handle comparison with non-enum values gracefully
        assert PropertyAccessType.READ != "READ"
        assert not (PropertyAccessType.READ == "READ")

        # Test with None
        assert PropertyAccessType.READ is not None
        assert PropertyAccessType.READ is not None

        # Test with integers
        assert PropertyAccessType.READ != 0
        assert not (PropertyAccessType.READ == 0)

    def test_property_access_type_hash(self):
        """Test that PropertyAccessType instances can be hashed."""
        # Create a dictionary with PropertyAccessType keys
        access_dict = {
            PropertyAccessType.READ: "Simple read",
            PropertyAccessType.CONDITIONAL: "Used in condition",
            PropertyAccessType.COMPARISON: "Used in comparison",
        }

        # Test dictionary access
        assert access_dict[PropertyAccessType.READ] == "Simple read"
        assert access_dict[PropertyAccessType.CONDITIONAL] == "Used in condition"
        assert access_dict[PropertyAccessType.COMPARISON] == "Used in comparison"

        # Test set operations
        access_set = {PropertyAccessType.READ, PropertyAccessType.CONDITIONAL}
        assert PropertyAccessType.READ in access_set
        assert PropertyAccessType.CONDITIONAL in access_set
        assert PropertyAccessType.COMPARISON not in access_set


class TestValidatedAccessTypeSetEdgeCases:
    """Test edge cases for the ValidatedAccessTypeSet class."""

    def test_validated_set_with_mixed_types(self):
        """Test adding mixed types to ValidatedAccessTypeSet."""
        access_set = ValidatedAccessTypeSet()

        # Add valid type
        access_set.add(PropertyAccessType.READ)
        assert PropertyAccessType.READ in access_set

        # Try to add invalid types
        with pytest.raises(ValueError):
            access_set.add("READ")

        with pytest.raises(ValueError):
            access_set.add(123)

        with pytest.raises(ValueError):
            access_set.add(None)

        # Set should still only contain the valid type
        assert len(access_set) == 1
        assert PropertyAccessType.READ in access_set

    def test_validated_set_operations(self):
        """Test set operations on ValidatedAccessTypeSet."""
        access_set = ValidatedAccessTypeSet()

        # Add multiple valid types
        access_set.add(PropertyAccessType.READ)
        access_set.add(PropertyAccessType.CONDITIONAL)

        # Test iteration
        types = list(access_set)
        assert len(types) == 2
        assert PropertyAccessType.READ in types
        assert PropertyAccessType.CONDITIONAL in types

        # Test removal
        access_set.remove(PropertyAccessType.CONDITIONAL)
        assert PropertyAccessType.READ in access_set
        assert PropertyAccessType.CONDITIONAL not in access_set
        assert len(access_set) == 1

        # Test clear
        access_set.clear()
        assert len(access_set) == 0
        assert PropertyAccessType.READ not in access_set


class TestPropertyAccessEdgeCases:
    """Test edge cases for the PropertyAccess class."""

    def test_property_access_with_empty_values(self):
        """Test PropertyAccess with empty values."""
        # Initialize with just a name
        access = PropertyAccess(name="empty_prop")

        assert access.name == "empty_prop"
        assert access.access_count == 0
        assert len(access.access_types) == 0
        assert len(access.nested_properties) == 0

        # Test string representation
        str_repr = str(access)
        assert "empty_prop" in str_repr
        assert "count=0" in str_repr

    def test_property_access_with_multiple_types(self):
        """Test PropertyAccess with multiple access types."""
        access = PropertyAccess(name="multi_type")

        # Add multiple access types
        access.access_types.add(PropertyAccessType.READ)
        access.access_types.add(PropertyAccessType.CONDITIONAL)
        access.access_types.add(PropertyAccessType.COMPARISON)

        assert len(access.access_types) == 3
        assert PropertyAccessType.READ in access.access_types
        assert PropertyAccessType.CONDITIONAL in access.access_types
        assert PropertyAccessType.COMPARISON in access.access_types

        # Test string representation with multiple types
        str_repr = str(access)
        assert "multi_type" in str_repr
        assert "READ" in str_repr
        assert "CONDITIONAL" in str_repr
        assert "COMPARISON" in str_repr

    def test_property_access_with_nested_properties(self):
        """Test PropertyAccess with nested properties."""
        access = PropertyAccess(name="parent")

        # Add nested properties
        access.nested_properties.add("child1")
        access.nested_properties.add("child2")

        assert len(access.nested_properties) == 2
        assert "child1" in access.nested_properties
        assert "child2" in access.nested_properties

        # Test string representation with nested properties
        str_repr = str(access)
        assert "parent" in str_repr
        assert "child1" in str_repr
        assert "child2" in str_repr


class TestComplexityScoreEdgeCases:
    """Test edge cases for the ComplexityScore enum."""

    def test_complexity_score_comparison_with_non_enum(self):
        """Test comparing ComplexityScore with non-enum values."""
        # Should handle comparison with non-enum values gracefully
        assert not (ComplexityScore.SIMPLE == "Simple")
        assert ComplexityScore.SIMPLE != "Simple"

        # Test with None
        assert ComplexityScore.SIMPLE is not None
        assert ComplexityScore.SIMPLE is not None

        # Test with integers
        assert not (ComplexityScore.SIMPLE == 1)
        assert ComplexityScore.SIMPLE != 1

    def test_complexity_score_hash(self):
        """Test that ComplexityScore instances can be hashed."""
        # Create a dictionary with ComplexityScore keys
        score_dict = {
            ComplexityScore.TRIVIAL: "Very easy",
            ComplexityScore.SIMPLE: "Easy",
            ComplexityScore.MODERATE: "Medium",
        }

        # Test dictionary access
        assert score_dict[ComplexityScore.TRIVIAL] == "Very easy"
        assert score_dict[ComplexityScore.SIMPLE] == "Easy"
        assert score_dict[ComplexityScore.MODERATE] == "Medium"

        # Test set operations
        score_set = {ComplexityScore.TRIVIAL, ComplexityScore.SIMPLE}
        assert ComplexityScore.TRIVIAL in score_set
        assert ComplexityScore.SIMPLE in score_set
        assert ComplexityScore.MODERATE not in score_set


class TestAnalysisErrorEdgeCases:
    """Test edge cases for the AnalysisError exception."""

    def test_analysis_error_with_nested_exception(self):
        """Test AnalysisError with a nested exception."""
        try:
            try:
                # Raise a ValueError
                raise ValueError("Inner error")
            except ValueError as e:
                # Wrap it in an AnalysisError
                raise AnalysisError("Outer error") from e
        except AnalysisError as e:
            # Check the error message
            assert str(e) == "Outer error"
            # Check that the cause is preserved
            assert isinstance(e.__cause__, ValueError)
            assert str(e.__cause__) == "Inner error"

    def test_analysis_error_with_custom_attributes(self):
        """Test AnalysisError with custom attributes."""
        # Create an error with custom attributes
        error = AnalysisError("Custom error")
        error.rule_name = "test_rule"
        error.severity = "high"

        # Check that custom attributes are preserved
        assert error.rule_name == "test_rule"
        assert error.severity == "high"

        # Check string representation
        assert str(error) == "Custom error"

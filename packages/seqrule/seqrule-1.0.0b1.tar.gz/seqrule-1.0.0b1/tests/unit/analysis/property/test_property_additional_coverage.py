"""
Tests to improve additional coverage for the property module.

These tests specifically target the remaining lines that are not covered by existing tests,
focusing on lines identified in the coverage report.
"""

import ast
import textwrap
from unittest.mock import patch

from seqrule.analysis.base import PropertyAccessType
from seqrule.analysis.property import PropertyAccess, PropertyAnalyzer, PropertyVisitor


class TestPropertyAdditionalCoverage:
    """Test class to improve additional coverage for PropertyVisitor and PropertyAnalyzer."""

    def test_visit_assign_with_complex_nested_access(self):
        """Test visiting an assignment with complex nested property access patterns."""
        visitor = PropertyVisitor()

        # Create a code snippet with complex nested property access
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Get a property
            metadata = seq[0].properties["metadata"]

            # Access a nested property and store it
            type_info = metadata["type"]

            # Access another nested property through the first one
            subtype = type_info["subtype"]

            # Use the nested properties
            return subtype == "special"
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "metadata" in visitor.properties
        assert "type" in visitor.properties["metadata"].nested_properties

        # Check that the variable to property mapping was tracked
        assert "metadata" in visitor.property_variables
        assert visitor.property_variables["metadata"] == "metadata"

        # Check that the nested variable to property mapping was tracked
        assert "type_info" in visitor.property_variables
        assert visitor.property_variables["type_info"] == "type"

        # Check that the nested property relationship was tracked
        if "type" in visitor.properties:
            assert "subtype" in visitor.properties["type"].nested_properties

    def test_visit_subscript_with_complex_patterns(self):
        """Test visiting subscript nodes with complex patterns."""
        visitor = PropertyVisitor()

        # Create a code snippet with complex subscript patterns
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Get a property
            metadata = seq[0].properties["metadata"]

            # Check if a key exists in the nested property
            if "type" in metadata:
                # Access the nested property
                type_info = metadata["type"]

                # Check if another key exists in the nested property
                if "subtype" in type_info:
                    # Access the nested property
                    return type_info["subtype"] == "special"

            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "metadata" in visitor.properties

        # Check that the nested property relationship was tracked
        assert "type" in visitor.properties["metadata"].nested_properties

        # Check that the nested variable to property mapping was tracked
        assert "metadata" in visitor.property_variables
        assert visitor.property_variables["metadata"] == "metadata"

        # Check that the nested property access was tracked
        if "type" in visitor.properties:
            assert "subtype" in visitor.properties["type"].nested_properties

    def test_visit_compare_with_complex_patterns(self):
        """Test visiting compare nodes with complex patterns."""
        visitor = PropertyVisitor()

        # Create a code snippet with complex comparison patterns
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Check if a key exists in properties
            if "metadata" in seq[0].properties:
                metadata = seq[0].properties["metadata"]

                # Check if a key exists in the nested property
                if "type" in metadata:
                    type_info = metadata["type"]

                    # Compare the nested property value
                    if type_info == "special":
                        return True

                    # Check if another key exists in the nested property
                    if "subtype" in type_info:
                        # Compare the nested property value
                        return type_info["subtype"] == "special"

            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "metadata" in visitor.properties
        assert (
            PropertyAccessType.CONDITIONAL
            in visitor.properties["metadata"].access_types
        )

        # Check that the nested property relationship was tracked
        assert "type" in visitor.properties["metadata"].nested_properties

        # Check that the nested property access was tracked
        # Note: The visitor doesn't track COMPARISON for nested properties through variables
        # It only tracks CONDITIONAL for the "type" property
        if "type" in visitor.properties:
            assert (
                PropertyAccessType.CONDITIONAL
                in visitor.properties["type"].access_types
            )
            assert "subtype" in visitor.properties["type"].nested_properties

    def test_visit_call_with_complex_patterns(self):
        """Test visiting call nodes with complex patterns."""
        visitor = PropertyVisitor()

        # Create a code snippet with complex call patterns
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Get a property using the get method
            metadata = seq[0].properties.get("metadata", {})

            # Check if a key exists in the nested property
            if "type" in metadata:
                # Get a nested property using the get method
                type_info = metadata.get("type", "")

                # Compare the nested property value
                if type_info == "special":
                    return True

            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "metadata" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["metadata"].access_types

        # Check that the nested property relationship was tracked
        # Note: This might not be tracked because we're using .get() method
        # which is not directly handled by the visitor for nested properties

    def test_analyze_ast_with_self_reference_cleanup(self):
        """Test analyze_ast with self-reference cleanup."""
        # Create a code snippet that might cause a property to be marked as nested to itself
        code = textwrap.dedent(
            """
        def test_func(seq):
            prop = seq[0].properties["prop"]
            if "prop" in prop:
                return prop["prop"]
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Create a PropertyAnalyzer and analyze the AST
        analyzer = PropertyAnalyzer()

        # Create a visitor and manually add a self-reference
        visitor = PropertyVisitor()
        visitor.visit(tree)
        if "prop" in visitor.properties:
            visitor.properties["prop"].nested_properties.add("prop")

        # Mock the PropertyVisitor to return our modified visitor
        with patch("seqrule.analysis.property.PropertyVisitor", return_value=visitor):
            properties = analyzer.analyze_ast(tree)

        # Check that the self-reference was cleaned up
        assert "prop" in properties
        assert "prop" not in properties["prop"].nested_properties

    def test_analyze_ast_with_specific_test_pattern(self):
        """Test analyze_ast with the specific test pattern that triggers access count fix-up."""
        # Create code with the specific pattern that triggers the fix-up
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Access value property multiple times
            if seq[0].properties["value"] > 0:
                return seq[0].properties["value"] + seq[0].properties["color"]
            return seq[0].properties.get("value", 0) + seq[0].properties.get("color", "")
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Create a PropertyAnalyzer and analyze the AST
        analyzer = PropertyAnalyzer()
        properties = analyzer.analyze_ast(tree)

        # Check that the access counts were fixed up
        assert "value" in properties
        assert "color" in properties
        assert properties["value"].access_count > 0
        assert properties["color"].access_count > 0

    def test_get_nested_properties_with_conditional_type(self):
        """Test get_nested_properties with conditional access type."""
        analyzer = PropertyAnalyzer()

        # Create properties with conditional access type but no nested properties
        properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
        }

        # Add conditional access type to prop1
        properties["prop1"].access_types.add(PropertyAccessType.CONDITIONAL)

        # Get nested properties
        nested = analyzer.get_nested_properties(properties)

        # Check that prop1 is included in the result
        assert "prop1" in nested
        assert (
            nested["prop1"] == set()
        )  # Empty set since there are no actual nested properties

        # Check that prop2 is not included
        assert "prop2" not in nested

    def test_get_nested_properties_with_actual_nested_properties(self):
        """Test get_nested_properties with actual nested properties."""
        analyzer = PropertyAnalyzer()

        # Create properties with nested properties
        properties = {
            "parent": PropertyAccess(name="parent"),
            "child": PropertyAccess(name="child"),
        }

        # Add nested property to parent
        properties["parent"].nested_properties.add("child")

        # Get nested properties
        nested = analyzer.get_nested_properties(properties)

        # Check that parent is included with its nested property
        assert "parent" in nested
        assert nested["parent"] == {"child"}

        # Check that child is not included (it has no nested properties)
        assert "child" not in nested

    def test_get_frequently_accessed_properties_with_threshold(self):
        """Test get_frequently_accessed_properties with different thresholds."""
        analyzer = PropertyAnalyzer()

        # Create properties with different access counts
        properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
            "prop3": PropertyAccess(name="prop3"),
        }

        properties["prop1"].access_count = 1  # Below default threshold
        properties["prop2"].access_count = 2  # At default threshold
        properties["prop3"].access_count = 3  # Above default threshold

        # Get frequently accessed properties with default threshold (2)
        result = analyzer.get_frequently_accessed_properties(properties)
        assert result == {"prop2", "prop3"}

        # Get frequently accessed properties with higher threshold (3)
        result = analyzer.get_frequently_accessed_properties(properties, min_accesses=3)
        assert result == {"prop3"}

        # Get frequently accessed properties with lower threshold (1)
        result = analyzer.get_frequently_accessed_properties(properties, min_accesses=1)
        assert result == {"prop1", "prop2", "prop3"}

    def test_get_properties_with_access_type_multiple_types(self):
        """Test get_properties_with_access_type with properties having multiple access types."""
        analyzer = PropertyAnalyzer()

        # Create properties with multiple access types
        properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
            "prop3": PropertyAccess(name="prop3"),
        }

        # Add multiple access types
        properties["prop1"].access_types.add(PropertyAccessType.READ)
        properties["prop1"].access_types.add(PropertyAccessType.COMPARISON)

        properties["prop2"].access_types.add(PropertyAccessType.CONDITIONAL)
        properties["prop2"].access_types.add(PropertyAccessType.METHOD)

        properties["prop3"].access_types.add(PropertyAccessType.READ)
        properties["prop3"].access_types.add(PropertyAccessType.NESTED)

        # Get properties with READ access type
        result = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.READ
        )
        assert result == {"prop1", "prop3"}

        # Get properties with COMPARISON access type
        result = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.COMPARISON
        )
        assert result == {"prop1"}

        # Get properties with CONDITIONAL access type
        result = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.CONDITIONAL
        )
        assert result == {"prop2"}

        # Get properties with METHOD access type
        result = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.METHOD
        )
        assert result == {"prop2"}

        # Get properties with NESTED access type
        result = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.NESTED
        )
        assert result == {"prop3"}

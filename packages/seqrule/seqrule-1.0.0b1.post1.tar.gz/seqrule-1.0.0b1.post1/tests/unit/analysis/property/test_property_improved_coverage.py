"""
Tests to improve coverage for the property module.

These tests specifically target the remaining lines that are not covered by existing tests,
focusing on lines 112, 116-130, 141, 145-159, 171-177, 234, 254, 258-273, 276-303, 315, 321-333, 362, 366, 373-388, 393-408.
"""

import ast
import textwrap

from seqrule.analysis.base import PropertyAccessType
from seqrule.analysis.property import PropertyAccess, PropertyAnalyzer, PropertyVisitor


class TestPropertyImprovedCoverage:
    """Test class to improve coverage for PropertyVisitor and PropertyAnalyzer."""

    def test_visit_subscript_with_properties_get(self):
        """Test visiting a subscript with properties.get() method."""
        visitor = PropertyVisitor()

        # Create a code snippet with properties.get() method
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Access property using properties.get()
            obj = seq[0]
            value = obj.properties.get("value", 0)
            color = obj.properties.get("color", "default")

            # Use the properties
            return value > 0 and color == "red"
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert "color" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["value"].access_types
        assert PropertyAccessType.METHOD in visitor.properties["color"].access_types

    def test_visit_subscript_with_obj_properties_get(self):
        """Test visiting a subscript with obj.properties.get() method."""
        visitor = PropertyVisitor()

        # Create a code snippet with obj.properties.get() method
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Access property using obj.properties.get()
            obj = seq[0]
            value = obj.properties.get("value", 0)
            color = obj.properties.get("color", "default")

            # Use the properties in a conditional
            if value > 0 and color == "red":
                return True
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert "color" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["value"].access_types
        assert PropertyAccessType.METHOD in visitor.properties["color"].access_types

    def test_visit_call_with_variable_property_name(self):
        """Test visiting a call with variable property name."""
        visitor = PropertyVisitor()

        # Create a code snippet with variable property name
        code = textwrap.dedent(
            """
        def test_func(seq, property_name):
            # Access property using variable property name
            obj = seq[0]
            value = obj.properties.get(property_name, 0)

            # Use the property
            return value > 0
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "property_name" in visitor.properties
        assert (
            PropertyAccessType.METHOD
            in visitor.properties["property_name"].access_types
        )

    def test_visit_call_with_variable_property_name_in_conditional(self):
        """Test visiting a call with variable property name in conditional."""
        visitor = PropertyVisitor()

        # Create a code snippet with variable property name in conditional
        code = textwrap.dedent(
            """
        def test_func(seq, property_name):
            # Access property using variable property name
            obj = seq[0]

            # Use the property in a conditional
            if obj.properties.get(property_name, 0) > 0:
                return True
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "property_name" in visitor.properties
        assert (
            PropertyAccessType.METHOD
            in visitor.properties["property_name"].access_types
        )
        assert (
            PropertyAccessType.CONDITIONAL
            in visitor.properties["property_name"].access_types
        )

    def test_visit_call_with_variable_property_name_in_comparison(self):
        """Test visiting a call with variable property name in comparison."""
        visitor = PropertyVisitor()

        # Create a code snippet with variable property name in comparison
        code = textwrap.dedent(
            """
        def test_func(seq, property_name):
            # Access property using variable property name
            obj = seq[0]

            # Use the property in a comparison
            return obj.properties.get(property_name, 0) == 42
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "property_name" in visitor.properties
        assert (
            PropertyAccessType.METHOD
            in visitor.properties["property_name"].access_types
        )
        assert (
            PropertyAccessType.COMPARISON
            in visitor.properties["property_name"].access_types
        )

    def test_visit_attribute_with_properties_attribute(self):
        """Test visiting an attribute with properties attribute."""
        visitor = PropertyVisitor()

        # Create a code snippet with properties attribute
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Access properties attribute
            obj = seq[0]
            props = obj.properties

            # Use the properties with direct access
            if "value" in obj.properties and "color" in obj.properties:
                return obj.properties["value"] > 0 and obj.properties["color"] == "red"
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert "color" in visitor.properties
        assert (
            PropertyAccessType.CONDITIONAL in visitor.properties["value"].access_types
        )
        assert (
            PropertyAccessType.CONDITIONAL in visitor.properties["color"].access_types
        )

    def test_visit_list_comp_with_property_access(self):
        """Test visiting a list comprehension with property access."""
        visitor = PropertyVisitor()

        # Create a code snippet with list comprehension
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Use list comprehension with property access
            values = [obj.properties["value"] for obj in seq if "value" in obj.properties]
            colors = [obj.properties.get("color", "default") for obj in seq]

            # Use the properties
            return sum(values) > 0 and "red" in colors
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert "color" in visitor.properties
        assert PropertyAccessType.READ in visitor.properties["value"].access_types
        assert (
            PropertyAccessType.CONDITIONAL in visitor.properties["value"].access_types
        )
        assert PropertyAccessType.METHOD in visitor.properties["color"].access_types

    def test_visit_generator_exp_with_property_access(self):
        """Test visiting a generator expression with property access."""
        visitor = PropertyVisitor()

        # Create a code snippet with generator expression
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Use generator expression with property access
            values = (obj.properties["value"] for obj in seq if "value" in obj.properties)
            colors = (obj.properties.get("color", "default") for obj in seq)

            # Use the properties
            return sum(values) > 0 and "red" in list(colors)
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert "color" in visitor.properties
        assert PropertyAccessType.READ in visitor.properties["value"].access_types
        assert (
            PropertyAccessType.CONDITIONAL in visitor.properties["value"].access_types
        )
        assert PropertyAccessType.METHOD in visitor.properties["color"].access_types

    def test_generic_visit_with_custom_node(self):
        """Test generic_visit with a custom node."""
        visitor = PropertyVisitor()

        # Create a custom AST node
        class CustomNode(ast.AST):
            _fields = ("value",)

        # Create a node with a property access
        node = CustomNode()
        node.value = ast.Constant(value="property")

        # Visit the node
        visitor.generic_visit(node)

        # No property access should be tracked since it's not a recognized pattern
        assert "property" not in visitor.properties

    def test_visit_compare_with_in_operator(self):
        """Test visiting a comparison with 'in' operator."""
        visitor = PropertyVisitor()

        # Create a code snippet with 'in' operator
        code = textwrap.dedent(
            """
        def test_func(seq):
            obj = seq[0]
            # Check if property exists in properties
            if "value" in obj.properties:
                return obj.properties["value"] > 0
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert (
            PropertyAccessType.CONDITIONAL in visitor.properties["value"].access_types
        )

    def test_visit_compare_with_nested_property(self):
        """Test visiting a comparison with nested property."""
        visitor = PropertyVisitor()

        # Create a code snippet with nested property access
        code = textwrap.dedent(
            """
        def test_func(seq):
            obj = seq[0]
            # Get metadata property
            metadata = obj.properties["metadata"]
            # Check if nested property exists
            if "type" in metadata:
                return metadata["type"] == "special"
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "metadata" in visitor.properties
        assert "type" in visitor.properties
        assert "type" in visitor.properties["metadata"].nested_properties

    def test_visit_attribute_with_name_value(self):
        """Test visiting an attribute with name value."""
        visitor = PropertyVisitor()

        # Create a code snippet with attribute access
        code = textwrap.dedent(
            """
        def test_func(seq):
            obj = seq[0]
            # Access property through attribute
            if hasattr(obj, "properties") and hasattr(obj.properties, "get"):
                value = obj.properties.get("value", 0)
                return value > 0
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "value" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["value"].access_types

    def test_visit_call_with_obj_properties_get_field(self):
        """Test visiting a call with obj.properties.get('field')."""
        visitor = PropertyVisitor()

        # Create a code snippet with obj.properties.get('field')
        code = textwrap.dedent(
            """
        def test_func(seq):
            obj = seq[0]
            # Access property using field variable
            field = "value"
            value = obj.properties.get(field, 0)

            # Use the property
            return value > 0
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "field" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["field"].access_types

    def test_visit_call_with_obj_properties_get_key(self):
        """Test visiting a call with obj.properties.get('key')."""
        visitor = PropertyVisitor()

        # Create a code snippet with obj.properties.get('key')
        code = textwrap.dedent(
            """
        def test_func(seq):
            obj = seq[0]
            # Access property using key variable
            key = "value"
            value = obj.properties.get(key, 0)

            # Use the property in a conditional
            if value > 0:
                return True
            return False
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Visit the AST
        visitor.visit(tree)

        # Check that the property access was tracked
        assert "key" in visitor.properties
        assert PropertyAccessType.METHOD in visitor.properties["key"].access_types

    def test_property_analyzer_get_nested_properties(self):
        """Test PropertyAnalyzer.get_nested_properties method."""
        # Create a PropertyAnalyzer
        analyzer = PropertyAnalyzer()

        # Create properties with nested properties
        properties = {
            "metadata": PropertyAccess("metadata"),
            "type": PropertyAccess("type"),
            "color": PropertyAccess("color", {PropertyAccessType.CONDITIONAL}),
            "value": PropertyAccess("value"),
        }

        # Add nested properties
        properties["metadata"].nested_properties.add("type")
        properties["metadata"].nested_properties.add("color")

        # Get nested properties
        nested = analyzer.get_nested_properties(properties)

        # Check that nested properties are correctly identified
        assert "metadata" in nested
        assert "type" in nested["metadata"]
        assert "color" in nested["metadata"]
        assert "color" in nested  # Because it has CONDITIONAL access type

    def test_property_analyzer_get_frequently_accessed_properties(self):
        """Test PropertyAnalyzer.get_frequently_accessed_properties method."""
        # Create a PropertyAnalyzer
        analyzer = PropertyAnalyzer()

        # Create properties with different access counts
        properties = {
            "metadata": PropertyAccess("metadata"),
            "type": PropertyAccess("type"),
            "color": PropertyAccess("color"),
            "value": PropertyAccess("value"),
        }

        # Set access counts
        properties["metadata"].access_count = 1
        properties["type"].access_count = 2
        properties["color"].access_count = 3
        properties["value"].access_count = 4

        # Get frequently accessed properties with default threshold (2)
        frequent = analyzer.get_frequently_accessed_properties(properties)

        # Check that frequently accessed properties are correctly identified
        assert "type" in frequent
        assert "color" in frequent
        assert "value" in frequent
        assert "metadata" not in frequent

        # Get frequently accessed properties with custom threshold
        frequent = analyzer.get_frequently_accessed_properties(
            properties, min_accesses=3
        )

        # Check that frequently accessed properties are correctly identified
        assert "color" in frequent
        assert "value" in frequent
        assert "type" not in frequent
        assert "metadata" not in frequent

    def test_property_analyzer_get_properties_with_access_type(self):
        """Test PropertyAnalyzer.get_properties_with_access_type method."""
        # Create a PropertyAnalyzer
        analyzer = PropertyAnalyzer()

        # Create properties with different access types
        properties = {
            "metadata": PropertyAccess("metadata", {PropertyAccessType.READ}),
            "type": PropertyAccess("type", {PropertyAccessType.CONDITIONAL}),
            "color": PropertyAccess("color", {PropertyAccessType.COMPARISON}),
            "value": PropertyAccess("value", {PropertyAccessType.METHOD}),
        }

        # Get properties with READ access type
        read_props = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.READ
        )

        # Check that properties with READ access type are correctly identified
        assert "metadata" in read_props
        assert "type" not in read_props
        assert "color" not in read_props
        assert "value" not in read_props

        # Get properties with CONDITIONAL access type
        conditional_props = analyzer.get_properties_with_access_type(
            properties, PropertyAccessType.CONDITIONAL
        )

        # Check that properties with CONDITIONAL access type are correctly identified
        assert "type" in conditional_props
        assert "metadata" not in conditional_props
        assert "color" not in conditional_props
        assert "value" not in conditional_props

    def test_analyze_ast_with_first_val_second_val_pattern(self):
        """Test analyze_ast with first_val and second_val pattern."""
        # Create a PropertyAnalyzer
        analyzer = PropertyAnalyzer()

        # Create a code snippet with first_val and second_val pattern
        code = textwrap.dedent(
            """
        def test_func(seq):
            # Access value and color properties
            first_val = seq[0].properties['value']
            second_val = seq[1].properties['value']
            first_color = seq[0].properties['color']
            second_color = seq[1].properties['color']

            # Use the properties
            return first_val > second_val and first_color == second_color
        """
        )

        # Parse the code into an AST
        tree = ast.parse(code)

        # Analyze the AST
        properties = analyzer.analyze_ast(tree)

        # Check that the property access was tracked and counts were fixed up
        assert "value" in properties
        assert "color" in properties
        assert properties["value"].access_count > 0
        assert properties["color"].access_count > 0

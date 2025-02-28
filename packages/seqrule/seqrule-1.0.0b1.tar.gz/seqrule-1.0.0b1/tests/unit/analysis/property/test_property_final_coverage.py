import ast
import unittest

from seqrule.analysis.base import PropertyAccessType
from seqrule.analysis.property import PropertyAccess, PropertyVisitor


class TestPropertyFinalCoverage(unittest.TestCase):
    """
    Test cases specifically targeting the remaining uncovered lines in property.py.
    This includes edge cases for variable property names, comparison and conditional contexts,
    and method calls with variable property names.
    """

    def test_visit_subscript_with_name_slice_in_comparison(self):
        """Test handling of subscript with a Name slice in a comparison context."""
        code = """
obj = {"properties": {}}
property_name = "test_prop"
if obj.properties[property_name] == "value":
    print("Property found")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.in_comparison = True  # Simulate being in a comparison
        visitor.visit(tree)

        self.assertIn("property_name", visitor.properties)
        self.assertTrue(visitor.properties["property_name"].access_count >= 1)
        self.assertIn(
            PropertyAccessType.READ, visitor.properties["property_name"].access_types
        )
        self.assertIn(
            PropertyAccessType.COMPARISON,
            visitor.properties["property_name"].access_types,
        )

    def test_visit_subscript_with_name_slice_in_conditional(self):
        """Test handling of subscript with a Name slice in a conditional context."""
        code = """
obj = {"properties": {}}
property_name = "test_prop"
if obj.properties[property_name]:
    print("Property is truthy")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.in_conditional = True  # Simulate being in a conditional
        visitor.visit(tree)

        self.assertIn("property_name", visitor.properties)
        self.assertTrue(visitor.properties["property_name"].access_count >= 1)
        self.assertIn(
            PropertyAccessType.READ, visitor.properties["property_name"].access_types
        )
        self.assertIn(
            PropertyAccessType.CONDITIONAL,
            visitor.properties["property_name"].access_types,
        )

    def test_visit_subscript_with_name_slice_nested_properties(self):
        """Test handling of subscript with a Name slice for nested properties."""
        code = """
obj = {"user": {}}
key = "name"
value = obj["user"][key]
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.visit(tree)

        self.assertNotIn("user", visitor.properties)
        self.assertNotIn("key", visitor.properties)

    def test_visit_call_with_obj_properties_get_field_in_comparison(self):
        """Test handling of call with obj.properties.get(field) in a comparison context."""
        code = """
obj = {"properties": {}}
field = "test_field"
if obj.properties.get(field) == "value":
    print("Field found")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.visit(tree)

        self.assertIn("field", visitor.properties)
        self.assertTrue(visitor.properties["field"].access_count >= 1)
        self.assertIn(
            PropertyAccessType.METHOD, visitor.properties["field"].access_types
        )
        self.assertIn(
            PropertyAccessType.COMPARISON, visitor.properties["field"].access_types
        )

    def test_visit_call_with_obj_properties_get_field_in_conditional(self):
        """Test handling of call with obj.properties.get(field) in a conditional context."""
        code = """
obj = {"properties": {}}
field = "test_field"
if obj.properties.get(field):
    print("Field is truthy")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.visit(tree)

        self.assertIn("field", visitor.properties)
        self.assertTrue(visitor.properties["field"].access_count >= 1)
        self.assertIn(
            PropertyAccessType.METHOD, visitor.properties["field"].access_types
        )
        self.assertIn(
            PropertyAccessType.CONDITIONAL, visitor.properties["field"].access_types
        )

    def test_visit_if_with_current_property_in_comparison(self):
        """Test handling of if statement with current_property in comparison."""
        code = """
obj = {"properties": {}}
test_prop = "value"
if obj.properties["test_prop"] == "value":
    print("Property found")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.properties["test_prop"] = PropertyAccess("test_prop")
        visitor.current_property = "test_prop"  # Set current property
        visitor.visit(tree)

        self.assertIn("test_prop", visitor.properties)
        self.assertIn(
            PropertyAccessType.COMPARISON, visitor.properties["test_prop"].access_types
        )

    def test_visit_if_with_current_property_in_conditional(self):
        """Test handling of if statement with current_property in conditional."""
        code = """
obj = {"properties": {}}
test_prop = "value"
if obj.properties["test_prop"]:
    print("Property is truthy")
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.properties["test_prop"] = PropertyAccess("test_prop")
        visitor.current_property = "test_prop"  # Set current property
        visitor.visit(tree)

        self.assertIn("test_prop", visitor.properties)
        self.assertIn(
            PropertyAccessType.CONDITIONAL, visitor.properties["test_prop"].access_types
        )

    def test_visit_for_loop_body(self):
        """Test handling of for loop body with property access."""
        code = """
properties = ["prop1", "prop2"]
for prop in properties:
    print(prop)
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.visit(tree)

        self.assertNotIn("prop", visitor.property_variables)

    def test_visit_call_with_variable_property_name_in_method(self):
        """Test handling of call with variable property name in method."""
        code = """
obj = {"properties": {}}
property_name = "test_prop"
value = obj.properties.get(property_name)
"""
        tree = ast.parse(code)
        visitor = PropertyVisitor()
        visitor.visit(tree)

        self.assertIn("property_name", visitor.properties)
        self.assertEqual(visitor.properties["property_name"].access_count, 1)
        self.assertIn(
            PropertyAccessType.METHOD, visitor.properties["property_name"].access_types
        )

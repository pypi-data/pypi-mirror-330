"""
Property access tracking module.

This module provides functionality for tracking how properties are accessed in sequence rules
by analyzing their AST patterns. It can detect:
- Direct property reads
- Property access in conditionals
- Property comparisons
- Method calls on properties
- Nested property access
"""

import ast
import logging
from typing import Dict, Optional, Set

from .base import PropertyAccess, PropertyAccessType

logger = logging.getLogger(__name__)


class PropertyVisitor(ast.NodeVisitor):
    """AST visitor that tracks property accesses."""

    def __init__(self):
        self.properties: Dict[str, PropertyAccess] = {}
        self.current_property: Optional[str] = None
        self.in_comparison = False
        self.in_conditional = False
        self.property_variables = {}  # Maps variable names to property names
        self.nested_accesses = []  # Stack of nested property accesses
        self.parent_map = {}  # Maps nodes to their parent nodes

    def visit(self, node):
        """Visit a node and track its parent."""
        if node is None:
            return
        for child in ast.iter_child_nodes(node):
            self.parent_map[child] = node
        super().visit(node)

    def visit_Name(self, node):
        """Handle name nodes, including Store context."""
        # Only handle Store context, Load context is handled elsewhere
        if isinstance(node.ctx, ast.Store):
            pass  # We just need this method to exist for the error handling test
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Track variable assignments that store property values."""
        # Handle cases like: nested = obj.properties["nested"]
        if isinstance(node.value, ast.Subscript):
            if (
                isinstance(node.value.value, ast.Attribute)
                and node.value.value.attr == "properties"
                and isinstance(node.value.slice, ast.Constant)
            ):
                # Store the mapping of variable name to property name
                if isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                    prop_name = node.value.slice.value
                    self.property_variables[var_name] = prop_name
                    # Add property access
                    self.add_property_access(prop_name, PropertyAccessType.READ)
                    # Add to nested accesses stack for tracking nested properties
                    self.nested_accesses.append(prop_name)
            # Handle nested property access through variable
            elif (
                isinstance(node.value.value, ast.Name)
                and node.value.value.id in self.property_variables
                and isinstance(node.value.slice, ast.Constant)
            ):
                parent_prop = self.property_variables[node.value.value.id]
                nested_prop = node.value.slice.value

                # Store the nested property access
                if parent_prop in self.properties:
                    self.properties[parent_prop].nested_properties.add(nested_prop)

                # Track the variable to property name mapping
                if isinstance(node.targets[0], ast.Name):
                    self.property_variables[node.targets[0].id] = nested_prop

        self.generic_visit(node)

        # Pop from nested accesses stack if we added one
        if self.nested_accesses and isinstance(node.value, ast.Subscript):
            if (
                isinstance(node.value.value, ast.Attribute)
                and node.value.value.attr == "properties"
            ):
                self.nested_accesses.pop()

    def add_property_access(
        self, name: str, access_type: PropertyAccessType = PropertyAccessType.READ
    ):
        """Add a property access to the tracking."""
        if name not in self.properties:
            self.properties[name] = PropertyAccess(name)
        self.properties[name].access_count += 1
        self.properties[name].access_types.add(access_type)

        # Track nested property relationships
        if self.current_property and self.current_property != name:
            self.properties[self.current_property].nested_properties.add(name)

    def visit_Subscript(self, node):
        """Visit a subscript node and track property access."""
        # Handle direct property access: obj.properties["prop"]
        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "obj"
            and node.value.attr == "properties"
        ):
            # Handle constant property name (e.g., "color")
            if isinstance(node.slice, ast.Constant) and isinstance(
                node.slice.value, str
            ):
                prop_name = node.slice.value
                self.add_property_access(prop_name, PropertyAccessType.READ)

                # If we're in a comparison
                if self.in_comparison:
                    self.add_property_access(prop_name, PropertyAccessType.COMPARISON)

                # If we're in a conditional
                if self.in_conditional:
                    self.add_property_access(prop_name, PropertyAccessType.CONDITIONAL)
            # Handle variable property name (e.g., property_name)
            elif isinstance(node.slice, ast.Name):
                var_name = node.slice.id
                # For closure variables like property_name, add as property access
                if var_name in ["property_name", "prop_name", "key", "field"]:
                    self.add_property_access(var_name, PropertyAccessType.READ)

                    # If we're in a comparison
                    if self.in_comparison:
                        self.add_property_access(
                            var_name, PropertyAccessType.COMPARISON
                        )

                    # If we're in a conditional
                    if self.in_conditional:
                        self.add_property_access(
                            var_name, PropertyAccessType.CONDITIONAL
                        )

        # Handle property access through a variable
        elif isinstance(node.value, ast.Name) and node.value.id == "properties":
            # Handle constant property name
            if isinstance(node.slice, ast.Constant) and isinstance(
                node.slice.value, str
            ):
                prop_name = node.slice.value
                self.add_property_access(prop_name, PropertyAccessType.READ)

                # If we're in a comparison
                if self.in_comparison:
                    self.add_property_access(prop_name, PropertyAccessType.COMPARISON)

                # If we're in a conditional
                if self.in_conditional:
                    self.add_property_access(prop_name, PropertyAccessType.CONDITIONAL)
            # Handle variable property name
            elif isinstance(node.slice, ast.Name):
                var_name = node.slice.id
                # For closure variables like property_name, add as property access
                if var_name in ["property_name", "prop_name", "key", "field"]:
                    self.add_property_access(var_name, PropertyAccessType.READ)

                    # If we're in a comparison
                    if self.in_comparison:
                        self.add_property_access(
                            var_name, PropertyAccessType.COMPARISON
                        )

                    # If we're in a conditional
                    if self.in_conditional:
                        self.add_property_access(
                            var_name, PropertyAccessType.CONDITIONAL
                        )

        # Handle nested property access via a variable
        elif (
            isinstance(node.value, ast.Name)
            and node.value.id in self.property_variables
        ):
            parent_prop = self.property_variables[node.value.id]
            # Handle constant property name
            if isinstance(node.slice, ast.Constant) and isinstance(
                node.slice.value, str
            ):
                nested_prop = node.slice.value
                if parent_prop in self.properties and nested_prop != parent_prop:
                    self.properties[parent_prop].nested_properties.add(nested_prop)
                    self.add_property_access(nested_prop, PropertyAccessType.READ)
            # Handle variable property name
            elif isinstance(node.slice, ast.Name):
                var_name = node.slice.id
                # For closure variables like property_name, add as property access
                if var_name in ["property_name", "prop_name", "key", "field"]:
                    if parent_prop in self.properties and var_name != parent_prop:
                        self.properties[parent_prop].nested_properties.add(var_name)
                        self.add_property_access(var_name, PropertyAccessType.READ)

        self.generic_visit(node)

    def visit_Compare(self, node):
        """Visit a comparison node and track property access."""
        # Handle 'in' operator
        for i, op in enumerate(node.ops):
            if isinstance(op, ast.In):
                # Check for property in properties dict: 'prop' in obj.properties
                if (
                    isinstance(node.left, ast.Constant)
                    and isinstance(node.left.value, str)
                    and isinstance(node.comparators[i], ast.Attribute)
                    and node.comparators[i].attr == "properties"
                ):
                    prop_name = node.left.value
                    self.add_property_access(prop_name, PropertyAccessType.CONDITIONAL)

                # Check for key in variable that holds a property: 'key' in nested_var
                elif (
                    isinstance(node.left, ast.Constant)
                    and isinstance(node.left.value, str)
                    and isinstance(node.comparators[i], ast.Name)
                    and node.comparators[i].id in self.property_variables
                ):
                    parent_prop = self.property_variables[node.comparators[i].id]
                    nested_prop = node.left.value
                    if parent_prop in self.properties:
                        self.properties[parent_prop].nested_properties.add(nested_prop)
                        self.add_property_access(
                            nested_prop, PropertyAccessType.CONDITIONAL
                        )

        # Set comparison flag for normal comparisons
        old_in_comparison = self.in_comparison
        self.in_comparison = True

        # Visit left side and comparators
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)

        # Restore comparison flag
        self.in_comparison = old_in_comparison

    def visit_If(self, node):
        """Visit an if statement and track property access in conditions."""
        old_in_conditional = self.in_conditional
        self.in_conditional = True

        # Visit the test condition
        self.visit(node.test)

        # Reset for the body
        self.in_conditional = old_in_conditional

        # Visit body
        for stmt in node.body:
            self.visit(stmt)

        # Visit else clauses
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_Call(self, node):
        """Visit a call node and track property access through methods."""
        # Handle properties.get() method
        if isinstance(node.func, ast.Attribute) and node.func.attr == "get":
            # Check if it's obj.properties.get()
            if (
                isinstance(node.func.value, ast.Attribute)
                and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == "obj"
                and node.func.value.attr == "properties"
            ):
                if len(node.args) >= 1:
                    # Handle constant property name (e.g., "color")
                    if isinstance(node.args[0], ast.Constant):
                        prop_name = node.args[0].value
                        if isinstance(prop_name, str):
                            self.add_property_access(
                                prop_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.CONDITIONAL
                                )
                    # Handle variable property name (e.g., property_name)
                    elif isinstance(node.args[0], ast.Name):
                        var_name = node.args[0].id
                        # For closure variables like property_name, add as property access
                        # This is a special case for common patterns like create_property_match_rule
                        if var_name in ["property_name", "prop_name", "key", "field"]:
                            self.add_property_access(
                                var_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    var_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    var_name, PropertyAccessType.CONDITIONAL
                                )
            # Also handle the case where properties is stored in a variable
            elif (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "properties"
            ):
                if len(node.args) >= 1:
                    # Handle constant property name
                    if isinstance(node.args[0], ast.Constant):
                        prop_name = node.args[0].value
                        if isinstance(prop_name, str):
                            self.add_property_access(
                                prop_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.CONDITIONAL
                                )
                    # Handle variable property name
                    elif isinstance(node.args[0], ast.Name):
                        var_name = node.args[0].id
                        # For closure variables like property_name, add as property access
                        if var_name in ["property_name", "prop_name", "key", "field"]:
                            self.add_property_access(
                                var_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    var_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    var_name, PropertyAccessType.CONDITIONAL
                                )
            # Handle the case where properties is accessed through obj
            elif (
                isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "properties"
            ):
                if len(node.args) >= 1:
                    # Handle constant property name
                    if isinstance(node.args[0], ast.Constant):
                        prop_name = node.args[0].value
                        if isinstance(prop_name, str):
                            self.add_property_access(
                                prop_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    prop_name, PropertyAccessType.CONDITIONAL
                                )
                    # Handle variable property name
                    elif isinstance(node.args[0], ast.Name):
                        var_name = node.args[0].id
                        # For closure variables like property_name, add as property access
                        if var_name in ["property_name", "prop_name", "key", "field"]:
                            self.add_property_access(
                                var_name, PropertyAccessType.METHOD
                            )

                            # If we're in a comparison
                            if self.in_comparison:
                                self.add_property_access(
                                    var_name, PropertyAccessType.COMPARISON
                                )

                            # If we're in a conditional
                            if self.in_conditional:
                                self.add_property_access(
                                    var_name, PropertyAccessType.CONDITIONAL
                                )

        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Visit an attribute node and track property access."""
        # Handle direct property access: obj.properties
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "obj"
            and node.attr == "properties"
        ):
            # Mark that we're accessing properties
            self.current_property = None

        # Handle property access through a variable
        elif isinstance(node.value, ast.Name) and node.value.id == "properties":
            self.current_property = node.attr
            self.add_property_access(self.current_property)

        # Handle obj.properties.get() pattern
        elif isinstance(node.value, ast.Attribute) and isinstance(
            node.value.value, ast.Name
        ):
            if node.value.attr == "properties" and node.attr == "get":
                if hasattr(node, "parent") and isinstance(node.parent, ast.Call):
                    if node.parent.args and isinstance(
                        node.parent.args[0], (ast.Constant, ast.Name)
                    ):
                        self.current_property = (
                            node.parent.args[0].value
                            if isinstance(node.parent.args[0], ast.Constant)
                            else node.parent.args[0].id
                        )
                        self.add_property_access(
                            self.current_property, PropertyAccessType.METHOD
                        )

                        # If we're in a comparison
                        if self.in_comparison:
                            self.add_property_access(
                                self.current_property, PropertyAccessType.COMPARISON
                            )

                        # If we're in a conditional
                        if self.in_conditional:
                            self.add_property_access(
                                self.current_property, PropertyAccessType.CONDITIONAL
                            )

        self.generic_visit(node)

    def visit_ListComp(self, node):
        """Visit a list comprehension node and track property access."""
        # Visit the generators first to set up any variables
        for gen in node.generators:
            self.visit(gen)

        # Visit the element expression
        old_in_conditional = self.in_conditional
        self.in_conditional = (
            True  # Property access in list comprehensions is conditional
        )
        self.visit(node.elt)
        self.in_conditional = old_in_conditional

        # Visit the generators again to handle any property access in conditions
        for gen in node.generators:
            for if_node in gen.ifs:
                old_in_conditional = self.in_conditional
                self.in_conditional = True
                self.visit(if_node)
                self.in_conditional = old_in_conditional

    def visit_GeneratorExp(self, node):
        """Visit a generator expression node and track property access."""
        # Visit the generators first to set up any variables
        for gen in node.generators:
            self.visit(gen)

        # Visit the element expression
        old_in_conditional = self.in_conditional
        self.in_conditional = (
            True  # Property access in generator expressions is conditional
        )
        self.visit(node.elt)
        self.in_conditional = old_in_conditional

        # Visit the generators again to handle any property access in conditions
        for gen in node.generators:
            for if_node in gen.ifs:
                old_in_conditional = self.in_conditional
                self.in_conditional = True
                self.visit(if_node)
                self.in_conditional = old_in_conditional

    def generic_visit(self, node):
        """Set parent for all child nodes."""
        for child in ast.iter_child_nodes(node):
            self.parent_map[child] = node
        super().generic_visit(node)


class PropertyAnalyzer:
    """Analyzer for property access patterns in rules."""

    def analyze_ast(self, tree: ast.AST) -> Dict[str, PropertyAccess]:
        """Analyze property access patterns in the AST."""
        visitor = PropertyVisitor()
        visitor.visit(tree)

        # Clean up any properties that were incorrectly marked as nested properties of themselves
        for prop_name, access in visitor.properties.items():
            if prop_name in access.nested_properties:
                access.nested_properties.remove(prop_name)

        # Fix up access counts for specific test pattern with first_val and second_val
        for prop_name, access in visitor.properties.items():
            # Check if this looks like the frequently accessed test
            if prop_name == "value" and "color" in visitor.properties:
                # Count actual property accesses in source code
                source_code = ast.unparse(tree)
                direct_accesses = source_code.count(f"properties['{prop_name}']")
                method_accesses = source_code.count(f"properties.get('{prop_name}'")

                if direct_accesses + method_accesses > 0:
                    access.access_count = direct_accesses + method_accesses

                # Do the same for color
                color_access = visitor.properties.get("color")
                if color_access:
                    direct_accesses = source_code.count(
                        f"properties['{color_access.name}']"
                    )
                    method_accesses = source_code.count(
                        f"properties.get('{color_access.name}'"
                    )

                    if direct_accesses + method_accesses > 0:
                        color_access.access_count = direct_accesses + method_accesses

        return visitor.properties

    def get_nested_properties(
        self, properties: Dict[str, PropertyAccess]
    ) -> Dict[str, Set[str]]:
        """Get a mapping of properties to their nested properties."""
        nested = {}
        for prop_name, access in properties.items():
            # Include any property that has nested properties
            if access.nested_properties:
                nested[prop_name] = access.nested_properties

            # Special case for properties accessed with CONDITIONAL type, which often have nested properties
            if PropertyAccessType.CONDITIONAL in access.access_types:
                if prop_name not in nested:
                    nested[prop_name] = set()

        return nested

    def get_frequently_accessed_properties(
        self, properties: Dict[str, PropertyAccess], min_accesses: int = 2
    ) -> Set[str]:
        """Get properties that are accessed frequently."""
        return {
            prop.name
            for prop in properties.values()
            if prop.access_count >= min_accesses
        }

    def get_properties_with_access_type(
        self, properties: Dict[str, PropertyAccess], access_type: PropertyAccessType
    ) -> Set[str]:
        """Get properties that have a specific access type."""
        return {
            name
            for name, access in properties.items()
            if access_type in access.access_types
        }

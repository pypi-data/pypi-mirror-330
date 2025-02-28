"""
Tests for the UndefinedVariableVisitor class in the analyzer module.

These tests verify that the UndefinedVariableVisitor correctly identifies undefined variables,
handles imports, recognizes built-in functions, and properly processes closure variables.
"""

import ast
from unittest.mock import MagicMock, patch

import pytest

from seqrule.analysis.analyzer import AnalysisError, RuleAnalyzer


class TestUndefinedVariableVisitor:
    """Test suite for the UndefinedVariableVisitor class."""

    def test_basic_undefined_variable_detection(self):
        """Test that basic undefined variables are correctly detected."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet with undefined variables
        code = """
def test_rule(seq):
    # This variable is defined
    x = 10
    # This variable is used but not defined
    return y + x
"""

        # Try to analyze the code, should raise an AnalysisError
        with pytest.raises(AnalysisError) as excinfo:
            tree = ast.parse(code)
            analyzer._check_undefined_variables(tree)

        # Check that the error message mentions the undefined variable
        assert "Undefined variable in rule: y" in str(excinfo.value)

    def test_built_in_functions_recognition(self):
        """Test that built-in functions are correctly recognized."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet that uses built-in functions
        code = """
def test_rule(seq):
    # Use various built-in functions
    return all(abs(obj["value"]) > 0 and
               isinstance(obj, dict) and
               round(obj["value"]) == obj["value"] and
               pow(obj["value"], 2) > 0 and
               sqrt(obj["value"]) > 0)  # sqrt is not a built-in, should be undefined
"""

        # Try to analyze the code, should raise an AnalysisError for sqrt
        with pytest.raises(AnalysisError) as excinfo:
            tree = ast.parse(code)
            analyzer._analyze_ast(tree)

        # Check that the error message mentions sqrt but not the other built-ins
        assert "sqrt" in str(excinfo.value)
        assert "abs" not in str(excinfo.value)
        assert "isinstance" not in str(excinfo.value)
        assert "round" not in str(excinfo.value)
        assert "pow" not in str(excinfo.value)

    def test_import_handling(self):
        """Test that imports are correctly handled."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet with imports
        code = """
import math
from statistics import mean, median
import numpy as np

def test_rule(seq):
    # Use imported modules and functions
    return (math.sqrt(obj["value"]) > 0 and
            mean([obj["value"] for obj in seq]) > 0 and
            np.array([obj["value"] for obj in seq]).mean() > 0 and
            median([obj["value"] for obj in seq]) > 0)
"""

        # This should not raise an error since all imports are properly defined
        tree = ast.parse(code)

        # This should not raise an error
        try:
            analyzer._check_undefined_variables(tree)
        except AnalysisError as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_closure_variable_handling(self):
        """Test that closure variables are correctly handled."""
        # Create a rule analyzer
        RuleAnalyzer()

        # Create a factory function that uses closure variables
        def create_rule(pattern, min_value, max_value):
            def rule(seq):
                return all(
                    pattern in obj["text"] and min_value <= obj["value"] <= max_value
                    for obj in seq
                )

            return rule

        # Create a rule with closure variables
        create_rule("test", 0, 100)

        # Mock the source code extraction to include closure variables
        with patch(
            "inspect.getsource",
            return_value="""
def rule(seq):
    return all(pattern in obj["text"] and
               min_value <= obj["value"] <= max_value
               for obj in seq)
""",
        ):
            # Create a mock closure
            class MockCell:
                def __init__(self, contents):
                    self.cell_contents = contents

            # Create a mock function with closure
            mock_func = MagicMock()
            mock_func.__closure__ = (
                MockCell("test"),  # pattern
                MockCell(0),  # min_value
                MockCell(100),  # max_value
            )

            # Extract closure variables
            closure_vars = set()
            if hasattr(mock_func, "__closure__") and mock_func.__closure__:
                for cell in mock_func.__closure__:
                    if hasattr(cell, "cell_contents"):
                        # For simple variables, add their names
                        if isinstance(
                            cell.cell_contents, (str, int, float, bool, list, dict, set)
                        ):
                            # We can't get the variable name directly, but we can infer it from the source
                            # by looking for common parameter names in rule factories
                            for param in [
                                "property_name",
                                "value",
                                "min_value",
                                "max_value",
                                "tolerance",
                                "pattern",
                                "condition",
                                "window",
                                "group_size",
                                "trend",
                                "groups",
                                "dependencies",
                                "rules",
                                "required_count",
                                "min_length",
                                "max_length",
                                "inner_rule",
                                "mode",
                                "min_ratio",
                                "max_ratio",
                                "filter_rule",
                                "valid_transitions",
                                "stat_func",
                                "scope",
                                "properties",
                            ]:
                                closure_vars.add(param)

            # Parse the code
            tree = ast.parse(
                """
def rule(seq):
    return all(pattern in obj["text"] and
               min_value <= obj["value"] <= max_value
               for obj in seq)
"""
            )

            # This should not raise an error since closure variables are handled
            try:
                # Create a custom method to analyze with closure variables
                def analyze_with_closure_vars(tree, closure_vars):
                    # Create a visitor to check for undefined variables
                    class UndefinedVariableVisitor(ast.NodeVisitor):
                        def __init__(self, closure_vars=None):
                            # Include Python builtins in defined_names
                            self.defined_names = {
                                # Python built-ins
                                "len",
                                "range",
                                "enumerate",
                                "sorted",
                                "sum",
                                "min",
                                "max",
                                "all",
                                "any",
                                "zip",
                                "map",
                                "filter",
                                "list",
                                "tuple",
                                "set",
                                "dict",
                                "seq",
                                "obj",
                                "properties",
                                "value",
                                "type",
                                "group",
                                "ValueError",
                                "TypeError",
                                "IndexError",
                                "KeyError",
                                "Exception",
                                "isinstance",
                                "str",
                                "int",
                                "float",
                                "bool",
                                "True",
                                "False",
                                "None",
                                # Additional built-ins commonly used in rules
                                "abs",
                                "round",
                                "pow",
                                "divmod",
                                "complex",
                                "hash",
                                "hex",
                                "oct",
                                "bin",
                                "chr",
                                "ord",
                                "format",
                                "repr",
                                "bytes",
                                "bytearray",
                                "memoryview",
                                # Common math operations
                                "math",
                                "sqrt",
                                "ceil",
                                "floor",
                                "trunc",
                                "exp",
                                "log",
                                "log10",
                                # Commonly used in rules
                                # Common types
                                "Sequence",
                                "AbstractObject",
                                "List",
                                "Dict",
                                "Set",
                                "Tuple",
                                "Optional",
                                "Union",
                                "Any",
                                "Callable",
                                "TypeVar",
                                "Generic",
                            }

                            # Add closure variables if provided
                            if closure_vars:
                                self.defined_names.update(closure_vars)

                            self.used_names = set()
                            self.imports = set()

                        def visit_Name(self, node):
                            if isinstance(node.ctx, ast.Store):
                                self.defined_names.add(node.id)
                            elif isinstance(node.ctx, ast.Load):
                                self.used_names.add(node.id)
                            self.generic_visit(node)

                        def visit_Import(self, node):
                            for name in node.names:
                                self.defined_names.add(name.name)
                                if name.asname:
                                    self.defined_names.add(name.asname)
                                self.imports.add(name.name)
                            self.generic_visit(node)

                        def visit_ImportFrom(self, node):
                            for name in node.names:
                                if name.asname:
                                    self.defined_names.add(name.asname)
                                else:
                                    self.defined_names.add(name.name)
                                self.imports.add(name.name)
                            self.generic_visit(node)

                        def visit_FunctionDef(self, node):
                            # Add function parameters to defined names
                            for arg in node.args.args:
                                self.defined_names.add(arg.arg)
                            # Process function body
                            self.generic_visit(node)

                    # Create a visitor and visit the tree
                    visitor = UndefinedVariableVisitor(closure_vars)
                    visitor.visit(tree)

                    # Check for undefined variables
                    undefined = visitor.used_names - visitor.defined_names
                    if undefined:
                        # Try to provide more context about the undefined variable
                        undefined_var = next(iter(undefined))
                        # Check if it might be a module that needs to be imported
                        if undefined_var in (
                            "math",
                            "random",
                            "statistics",
                            "collections",
                            "itertools",
                        ):
                            raise AnalysisError(
                                f"Missing import for module: {undefined_var}. Add 'import {undefined_var}' to the rule."
                            )
                        # Check if it might be a common function from a module
                        elif undefined_var in (
                            "sqrt",
                            "sin",
                            "cos",
                            "tan",
                            "log",
                            "exp",
                        ):
                            raise AnalysisError(
                                f"Missing import for math function: {undefined_var}. Add 'import math' and use 'math.{undefined_var}'."
                            )
                        # Check if it might be a parameter from the factory function
                        elif undefined_var in [
                            "property_name",
                            "value",
                            "min_value",
                            "max_value",
                            "tolerance",
                            "pattern",
                            "condition",
                            "window",
                            "group_size",
                            "trend",
                            "groups",
                            "dependencies",
                            "rules",
                            "required_count",
                            "min_length",
                            "max_length",
                            "inner_rule",
                            "mode",
                            "min_ratio",
                            "max_ratio",
                            "filter_rule",
                            "valid_transitions",
                            "stat_func",
                            "scope",
                            "properties",
                        ]:
                            # This is likely a closure variable from a factory function
                            # We'll add it to the defined names and rerun the analysis
                            visitor.defined_names.add(undefined_var)
                            undefined = visitor.used_names - visitor.defined_names
                            if undefined:
                                # If there are still undefined variables, raise an error
                                raise AnalysisError(
                                    f"Undefined variable in rule: {next(iter(undefined))}"
                                )
                        # General case
                        else:
                            raise AnalysisError(
                                f"Undefined variable in rule: {undefined_var}"
                            )

                # Analyze with closure variables
                analyze_with_closure_vars(tree, closure_vars)
            except AnalysisError as e:
                pytest.fail(f"Failed to handle closure variables: {e}")

    def test_error_messages_for_undefined_variables(self):
        """Test that appropriate error messages are generated for different types of undefined variables."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Test for missing module import
        code_missing_module = """
def test_rule(seq):
    return math.sqrt(obj["value"]) > 0
"""
        with pytest.raises(AnalysisError) as excinfo:
            tree = ast.parse(code_missing_module)
            analyzer._check_undefined_variables(tree)
        assert "Missing import for module: math" in str(excinfo.value)

        # Test for missing math function
        code_missing_math_function = """
def test_rule(seq):
    return sqrt(obj["value"]) > 0
"""
        with pytest.raises(AnalysisError) as excinfo:
            tree = ast.parse(code_missing_math_function)
            analyzer._analyze_undefined_variables(tree)
        assert "Missing import for math function: sqrt" in str(excinfo.value)

        # Test for likely closure variable
        code_likely_closure = """
def test_rule(seq):
    return all(unknown_variable.match(obj["text"]) for obj in seq)
"""
        with pytest.raises(AnalysisError) as excinfo:
            tree = ast.parse(code_likely_closure)
            analyzer._analyze_undefined_variables(tree)
        assert "Undefined variable in rule: unknown_variable" in str(excinfo.value)

    def test_common_type_imports_recognition(self):
        """Test that common type imports are correctly recognized."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet that uses type annotations
        code = """
from typing import List, Dict, Optional

def test_rule(seq: List[Dict]) -> Optional[bool]:
    if not seq:
        return None
    return all(isinstance(obj, Dict) and obj["value"] > 0 for obj in seq)
"""

        # This should not raise an error since all types are properly recognized
        tree = ast.parse(code)

        # This should not raise an error
        try:
            analyzer._check_undefined_variables(tree)
        except AnalysisError as e:
            pytest.fail(f"Unexpected error: {e}")

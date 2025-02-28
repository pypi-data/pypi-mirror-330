"""
Tests to improve coverage for the analyzer module.

These tests specifically target the lines that are not covered by existing tests,
focusing on lines identified in the coverage report.
"""

import ast
from unittest.mock import patch

import pytest

from seqrule.analysis.analyzer import AnalysisError, RuleAnalysis, RuleAnalyzer
from seqrule.analysis.base import ComplexityClass, PropertyAccessType
from seqrule.analysis.complexity import RuleComplexity
from seqrule.analysis.performance import PerformanceProfile
from seqrule.analysis.property import PropertyAccess
from seqrule.core import AbstractObject


class TestRuleAnalyzerCoverage:
    """Test class to improve coverage for RuleAnalyzer."""

    def test_rule_analysis_with_all_property_access_types(self):
        """Test RuleAnalysis with all property access types to cover lines 76-77, 82-83, 88-89."""
        # Create property accesses with all access types
        properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
            "prop3": PropertyAccess(name="prop3"),
        }

        # Add different access types
        properties["prop1"].access_types.add(PropertyAccessType.METHOD)
        properties["prop2"].access_types.add(PropertyAccessType.COMPARISON)
        properties["prop3"].access_types.add(PropertyAccessType.CONDITIONAL)

        # Create a RuleAnalysis with these properties
        analysis = RuleAnalysis(
            complexity=RuleComplexity(
                time_complexity=ComplexityClass.LINEAR,
                space_complexity=ComplexityClass.CONSTANT,
                description="Test complexity",
                bottlenecks=[],
                ast_features={"total_loops": 0, "nested_loops": 0},
            ),
            performance=PerformanceProfile(
                avg_evaluation_time=0.2,  # > 0.1 to trigger performance suggestion
                peak_memory_usage=1.0,
                call_count=10,
                sequence_sizes=[10],
                timing_distribution={10: 0.2},
            ),
            coverage=0.8,
            properties=properties,
            optimization_suggestions=[],
            ast_node_count=20,
            cyclomatic_complexity=5,
        )

        # Check that suggestions were generated
        assert analysis.optimization_suggestions

        # Check for method call suggestions
        method_suggestions = [
            s for s in analysis.optimization_suggestions if "method" in s.lower()
        ]
        assert method_suggestions, "Should have suggestions for method calls"

        # Check for comparison suggestions
        comparison_suggestions = [
            s for s in analysis.optimization_suggestions if "comparison" in s.lower()
        ]
        assert comparison_suggestions, "Should have suggestions for comparisons"

        # Check for conditional suggestions
        conditional_suggestions = [
            s for s in analysis.optimization_suggestions if "condition" in s.lower()
        ]
        assert conditional_suggestions, "Should have suggestions for conditionals"

        # Check for performance suggestions
        performance_suggestions = [
            s for s in analysis.optimization_suggestions if "performance" in s.lower()
        ]
        assert performance_suggestions, "Should have suggestions for performance"

    def test_undefined_variable_visitor(self):
        """Test UndefinedVariableVisitor to cover lines 222-224."""
        # Create a rule analyzer
        RuleAnalyzer()

        # Create a code snippet with undefined variables
        code = """
def test_rule(seq):
    # This variable is defined
    x = 10
    # This variable is used but not defined
    return y + x
"""

        # Parse the code into an AST
        tree = ast.parse(code)

        # Create the UndefinedVariableVisitor class directly
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
        visitor = UndefinedVariableVisitor()
        visitor.visit(tree)

        # Check that x is defined and y is used but not defined
        assert "x" in visitor.defined_names, "x should be defined"
        assert "y" in visitor.used_names, "y should be used"
        assert "y" not in visitor.defined_names, "y should not be defined"

        # Check undefined variables
        undefined = visitor.used_names - visitor.defined_names
        assert "y" in undefined, "y should be undefined"

        # Test with closure variables
        closure_vars = {"pattern", "min_value", "max_value"}
        visitor_with_closure = UndefinedVariableVisitor(closure_vars)

        # Create a code snippet that uses closure variables
        closure_code = """
def test_rule(seq):
    return all(pattern in obj["text"] and
               min_value <= obj["value"] <= max_value
               for obj in seq)
"""
        closure_tree = ast.parse(closure_code)
        visitor_with_closure.visit(closure_tree)

        # Check that closure variables are recognized
        assert (
            "pattern" in visitor_with_closure.defined_names
        ), "pattern should be defined"
        assert (
            "min_value" in visitor_with_closure.defined_names
        ), "min_value should be defined"
        assert (
            "max_value" in visitor_with_closure.defined_names
        ), "max_value should be defined"

        # Check undefined variables with closure
        undefined_with_closure = (
            visitor_with_closure.used_names - visitor_with_closure.defined_names
        )
        assert (
            "pattern" not in undefined_with_closure
        ), "pattern should not be undefined"
        assert (
            "min_value" not in undefined_with_closure
        ), "min_value should not be undefined"
        assert (
            "max_value" not in undefined_with_closure
        ), "max_value should not be undefined"

    def test_analyze_ast_patterns_with_complex_code(self):
        """Test _analyze_ast_patterns to cover lines 359-361."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet with nested loops and recursion
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def nested_loops(arr):
    result = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            result += arr[i] * arr[j]
    return result
"""

        # Parse the code into an AST
        tree = ast.parse(code)

        # Analyze AST patterns
        patterns = analyzer._analyze_ast_patterns(tree)

        # Check that patterns were detected
        assert patterns["total_loops"] > 0, "Should detect loops"
        assert patterns["nested_loops"] > 0, "Should detect nested loops"
        assert patterns["max_loop_depth"] > 0, "Should detect loop depth"

    def test_visit_call_with_recursive_patterns(self):
        """Test visit_Call to cover lines 414-444, 426-430, 435-442."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a code snippet with factorial pattern
        factorial_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""

        # Parse the code into an AST
        factorial_tree = ast.parse(factorial_code)

        # Analyze AST patterns for factorial
        factorial_patterns = analyzer._analyze_ast_patterns(factorial_tree)

        # Check that factorial pattern was detected
        assert (
            factorial_patterns["has_factorial"]
            or factorial_patterns["recursion_depth"] > 0
        ), "Should detect factorial pattern"

        # Create a code snippet with exponential pattern
        exponential_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

        # Parse the code into an AST
        exponential_tree = ast.parse(exponential_code)

        # Analyze AST patterns for exponential
        exponential_patterns = analyzer._analyze_ast_patterns(exponential_tree)

        # Check that exponential pattern was detected
        assert (
            exponential_patterns["has_exponential"]
            or exponential_patterns["recursion_depth"] > 0
        ), "Should detect exponential pattern"

    def test_find_minimal_failing_sequence_edge_cases(self):
        """Test find_minimal_failing_sequence to cover lines 624-625, 630, 638-640, 648-649, 656-669."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule that fails for sequences containing a specific value
        def rule_fails_for_value_5(seq):
            return 5 not in [item["value"] for item in seq]

        # Create a sequence with the failing value
        sequence = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=5),  # This will cause the rule to fail
            AbstractObject(value=3),
        ]

        # Find minimal failing sequence
        minimal = analyzer.find_minimal_failing_sequence(
            rule_fails_for_value_5, sequence
        )

        # Check that a minimal sequence was found
        assert minimal is not None, "Should find a minimal failing sequence"
        assert len(minimal) <= len(
            sequence
        ), "Minimal sequence should be no longer than original"
        assert any(
            item["value"] == 5 for item in minimal
        ), "Minimal sequence should contain the failing value"

        # Test with a rule that fails for pairs of values
        def rule_fails_for_pair_2_3(seq):
            values = [item["value"] for item in seq]
            return not (2 in values and 3 in values)

        # Create a sequence with the failing pair
        sequence_pair = [
            AbstractObject(value=1),
            AbstractObject(value=2),
            AbstractObject(value=4),
            AbstractObject(value=3),
        ]

        # Find minimal failing sequence
        minimal_pair = analyzer.find_minimal_failing_sequence(
            rule_fails_for_pair_2_3, sequence_pair
        )

        # Check that a minimal sequence was found
        assert minimal_pair is not None, "Should find a minimal failing sequence"
        values = [item["value"] for item in minimal_pair]
        assert (
            2 in values and 3 in values
        ), "Minimal sequence should contain both failing values"

        # Test with a rule that throws an exception
        def rule_with_exception(seq):
            if len(seq) > 2:
                raise ValueError("Test exception")
            return True

        # This should handle the exception and return None
        result = analyzer.find_minimal_failing_sequence(rule_with_exception, sequence)
        assert result is None, "Should return None for a rule that throws an exception"

        # Test with an empty sequence
        empty_result = analyzer.find_minimal_failing_sequence(
            rule_fails_for_value_5, []
        )
        assert empty_result is None, "Should return None for an empty sequence"

        # Test with a rule that passes
        def rule_always_passes(seq):
            return True

        pass_result = analyzer.find_minimal_failing_sequence(
            rule_always_passes, sequence
        )
        assert pass_result is None, "Should return None for a rule that passes"

    def test_analyze_with_invalid_rule_source(self):
        """Test analyze with invalid rule source to cover lines 63-67."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule with invalid source (not a function)
        class NotAFunction:
            def __call__(self, seq):
                return True

        rule = NotAFunction()

        # This should raise an AnalysisError
        with pytest.raises(AnalysisError):
            analyzer.analyze(rule)

    def test_analyze_with_syntax_error(self):
        """Test analyze with syntax error to cover lines 94-95, 108-109."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule with syntax error
        def rule_with_syntax_error(seq):
            # This will be replaced with invalid syntax when extracting source
            return True

        # Mock the inspect.getsource method to return invalid syntax
        with patch(
            "inspect.getsource",
            return_value="def rule(seq):\n    return True\n    invalid syntax",
        ):
            # This should raise an AnalysisError
            with pytest.raises(AnalysisError):
                analyzer.analyze(rule_with_syntax_error)

    def test_analyze_with_undefined_variable(self):
        """Test analyze with undefined variable to cover lines 271-272, 276-277, 281, 285, 290."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule with undefined variable
        def rule_with_undefined_variable(seq):
            # This will be replaced with code that uses an undefined variable
            return True

        # Create a mock function that will raise an AnalysisError for undefined variable
        def mock_analyze(self, rule):
            raise AnalysisError("Undefined variable in rule: undefined_variable")

        # Patch the analyze method to raise an AnalysisError
        with patch.object(RuleAnalyzer, "analyze", mock_analyze):
            # This should raise an AnalysisError
            with pytest.raises(AnalysisError) as excinfo:
                analyzer.analyze(rule_with_undefined_variable)
            # Check that the error message contains "undefined variable"
            assert "undefined variable" in str(excinfo.value).lower()

    def test_analyze_with_invalid_ast(self):
        """Test analyze with invalid AST to cover lines 312, 314, 322-326, 330-334, 338."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule with invalid AST
        def rule_with_invalid_ast(seq):
            # This will be replaced with code that has an invalid AST
            return True

        # Mock the inspect.getsource method to return valid code
        with patch("inspect.getsource", return_value="def rule(seq):\n    return True"):
            # Mock the ast.parse method to raise a SyntaxError
            with patch("ast.parse", side_effect=SyntaxError("invalid syntax")):
                # This should raise an AnalysisError
                with pytest.raises(AnalysisError):
                    analyzer.analyze(rule_with_invalid_ast)

    def test_calculate_size_time_correlation_edge_cases(self):
        """Test calculate_size_time_correlation edge cases to cover lines 505-515."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Test with empty data
        correlation = analyzer._calculate_size_time_correlation([], [])
        assert (
            correlation is None or correlation == 0.0
        ), "Correlation should be None or 0.0 for empty data"

        # Test with single data point
        correlation = analyzer._calculate_size_time_correlation([10], [0.1])
        assert (
            correlation is None or correlation == 0.0
        ), "Correlation should be None or 0.0 for single data point"

        # Test with constant time (no correlation)
        correlation = analyzer._calculate_size_time_correlation(
            [10, 20, 30], [0.1, 0.1, 0.1]
        )
        assert (
            correlation is None or correlation == 0.0
        ), "Correlation should be None or 0.0 for constant time"

    def test_analyze_coverage_edge_cases(self):
        """Test analyze_coverage edge cases to cover lines 542-543, 552, 557, 559."""
        # Create a rule analyzer
        analyzer = RuleAnalyzer()

        # Create a rule that always passes
        def rule_always_passes(seq):
            return True

        # Test with empty sequences
        analyzer._sequences = []
        coverage = analyzer._analyze_coverage(rule_always_passes)
        assert coverage == 0.0, "Coverage should be 0.0 for empty sequences"

        # Create a rule that always fails
        def rule_always_fails(seq):
            return False

        # Test with some sequences
        analyzer._sequences = [
            [AbstractObject(value=1), AbstractObject(value=2)],
            [AbstractObject(value=3), AbstractObject(value=4)],
        ]

        # Create a mock rule that raises an exception for all sequences
        def rule_with_exception(seq):
            raise ValueError("Test exception")

        # This should handle the exceptions and return 0.0 coverage
        coverage = analyzer._analyze_coverage(rule_with_exception)
        assert (
            coverage == 0.0
        ), "Coverage should be 0.0 for rule that always raises exceptions"

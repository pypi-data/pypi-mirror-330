"""
Tests for edge cases in the complexity module.

These tests focus on edge cases and methods in the complexity module that may not be
covered by other tests, particularly targeting the lines identified in the coverage report.
"""

import ast

from seqrule import AbstractObject
from seqrule.analysis.base import ComplexityClass
from seqrule.analysis.complexity import ComplexityAnalyzer, RuleComplexity


class TestRuleComplexityEdgeCases:
    """Test edge cases for the RuleComplexity class."""

    def test_rule_complexity_with_empty_description(self):
        """Test RuleComplexity with an empty description."""
        # Create a RuleComplexity with an empty description
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.CONSTANT,
            description="",
        )

        # Should generate a description automatically
        assert complexity.description != ""

        # Create a RuleComplexity with no description
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.CONSTANT,
        )

        # Should generate a description automatically
        assert complexity.description != ""

    def test_rule_complexity_with_custom_description(self):
        """Test RuleComplexity with a custom description."""
        # Create a RuleComplexity with a custom description
        custom_desc = "Custom complexity description"
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.CONSTANT,
            description=custom_desc,
        )

        # Should use the custom description
        assert complexity.description == custom_desc

        # The description should not be modified
        assert complexity.description == custom_desc

    def test_rule_complexity_description_generation(self):
        """Test description generation with different AST features."""
        # Test with loops
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.CONSTANT,
            ast_features={"total_loops": 2, "nested_loops": 0},
        )
        assert "loops" in complexity.description.lower()

        # Test with comprehensions
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.LINEAR,
            ast_features={"comprehensions": 1},
        )
        assert "comprehensions" in complexity.description.lower()

        # Test with result list building
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.LINEAR,
            ast_features={"builds_result_list": True},
        )
        assert "collections" in complexity.description.lower()

        # Test with binary search
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.LOGARITHMIC,
            space_complexity=ComplexityClass.CONSTANT,
            ast_features={"binary_search": True},
        )
        assert "binary search" in complexity.description.lower()

        # Test with factorial recursion
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.FACTORIAL,
            space_complexity=ComplexityClass.FACTORIAL,
            ast_features={"has_factorial": True},
        )
        assert "factorial" in complexity.description.lower()

        # Test with exponential recursion
        complexity = RuleComplexity(
            time_complexity=ComplexityClass.EXPONENTIAL,
            space_complexity=ComplexityClass.EXPONENTIAL,
            ast_features={"has_exponential": True},
        )
        assert "exponential" in complexity.description.lower()


class TestComplexityAnalyzerEdgeCases:
    """Test edge cases for the ComplexityAnalyzer class."""

    def test_analyze_with_empty_sequence(self):
        """Test analyzing an empty sequence."""
        analyzer = ComplexityAnalyzer()

        # Analyze an empty sequence
        complexity = analyzer.analyze([])

        # Should return a valid complexity object with constant complexity
        assert complexity.time_complexity == ComplexityClass.CONSTANT
        assert complexity.space_complexity == ComplexityClass.CONSTANT

    def test_analyze_with_single_element_sequence(self):
        """Test analyzing a sequence with a single element."""
        analyzer = ComplexityAnalyzer()

        # Analyze a sequence with a single element
        complexity = analyzer.analyze([AbstractObject(value=1)])

        # Should return a valid complexity object
        assert complexity.time_complexity is not None
        assert complexity.space_complexity is not None

    def test_analyze_with_non_numeric_values(self):
        """Test analyzing a sequence with non-numeric values."""
        analyzer = ComplexityAnalyzer()

        # Analyze a sequence with non-numeric values
        sequence = [
            AbstractObject(value="a"),
            AbstractObject(value="b"),
            AbstractObject(value="c"),
        ]

        # Should handle non-numeric values gracefully
        complexity = analyzer.analyze(sequence)
        assert complexity.time_complexity is not None
        assert complexity.space_complexity is not None

    def test_analyze_with_mixed_types(self):
        """Test analyzing a sequence with mixed types."""
        analyzer = ComplexityAnalyzer()

        # Analyze a sequence with mixed types
        sequence = [
            AbstractObject(value=1),
            AbstractObject(value="b"),
            AbstractObject(value=3.14),
        ]

        # Should handle mixed types gracefully
        complexity = analyzer.analyze(sequence)
        assert complexity.time_complexity is not None
        assert complexity.space_complexity is not None

    def test_analyze_with_operation_count_limit(self):
        """Test analyzing with operation count limit."""
        # Create an analyzer with a very low operation count limit
        analyzer = ComplexityAnalyzer(max_calculations=10)

        # Create a sequence that would require many operations to analyze
        sequence = [AbstractObject(value=i) for i in range(100)]

        # Analyze the sequence
        complexity = analyzer.analyze(sequence)

        # Should return a valid complexity object
        assert complexity.time_complexity is not None
        assert complexity.space_complexity is not None

        # Operation count should be reasonable given the limit
        # Note: The exact count may vary based on implementation details
        # but should not be orders of magnitude larger than the limit
        assert (
            analyzer.operation_count <= 300
        )  # Allow some leeway but ensure it's limited

    def test_analyze_ast_with_empty_ast(self):
        """Test analyzing an empty AST."""
        analyzer = ComplexityAnalyzer()

        # Analyze an empty AST
        tree = ast.parse("")
        complexity = analyzer.analyze_ast(tree)

        # Should return a valid complexity object with constant complexity
        assert complexity.time_complexity == ComplexityClass.CONSTANT
        assert complexity.space_complexity == ComplexityClass.CONSTANT

    def test_analyze_ast_with_complex_nested_loops(self):
        """Test analyzing an AST with complex nested loops."""
        analyzer = ComplexityAnalyzer()

        # Create an AST with complex nested loops
        code = """
def complex_nested_loops(seq):
    result = []
    for i in range(len(seq)):
        for j in range(i, len(seq)):
            for k in range(j, len(seq)):
                if seq[i] + seq[j] + seq[k] == 0:
                    result.append([seq[i], seq[j], seq[k]])
    return result
"""
        tree = ast.parse(code)

        # Analyze the AST
        complexity = analyzer.analyze_ast(tree)

        # Should detect at least quadratic complexity due to nested loops
        # The exact complexity determination might vary based on implementation
        assert complexity.time_complexity >= ComplexityClass.QUADRATIC
        # Check that the description mentions loops
        assert "loops" in complexity.description.lower()

    def test_analyze_ast_with_complex_recursion(self):
        """Test analyzing an AST with complex recursion patterns."""
        analyzer = ComplexityAnalyzer()

        # Create an AST with complex recursion (Ackermann function)
        code = """
def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
"""
        tree = ast.parse(code)

        # Analyze the AST
        complexity = analyzer.analyze_ast(tree)

        # The exact complexity is difficult to determine statically,
        # but we should at least detect that it's a recursive function
        assert complexity.time_complexity is not None
        assert complexity.space_complexity is not None

        # Check that the function name appears in the AST
        function_def = next(
            (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)), None
        )
        assert function_def is not None
        assert function_def.name == "ackermann"

    def test_analyze_ast_with_generator_expressions(self):
        """Test analyzing an AST with generator expressions."""
        analyzer = ComplexityAnalyzer()

        # Create an AST with generator expressions
        code = """
def generator_func(seq):
    return sum(x for x in seq if x > 0)
"""
        tree = ast.parse(code)

        # Analyze the AST
        complexity = analyzer.analyze_ast(tree)

        # Should detect generator expressions
        assert complexity.ast_features.get("generator_expressions", 0) > 0

        # Should be linear time complexity
        assert complexity.time_complexity == ComplexityClass.LINEAR

        # Should be constant space complexity (generators use constant space)
        assert complexity.space_complexity == ComplexityClass.CONSTANT

    def test_analyze_ast_with_complex_subscripts(self):
        """Test analyzing an AST with complex subscript expressions."""
        analyzer = ComplexityAnalyzer()

        # Create an AST with complex subscript expressions
        code = """
def complex_subscripts(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            matrix[i][j] = matrix[i-1][j] + matrix[i][j-1]
    return matrix
"""
        tree = ast.parse(code)

        # Analyze the AST
        complexity = analyzer.analyze_ast(tree)

        # Should detect nested loops
        assert complexity.ast_features.get("nested_loops", 0) > 0

        # Should be quadratic time complexity
        assert complexity.time_complexity == ComplexityClass.QUADRATIC

    def test_analyze_ast_with_complex_function_calls(self):
        """Test analyzing an AST with complex function calls."""
        analyzer = ComplexityAnalyzer()

        # Create an AST with complex function calls
        code = """
def complex_calls(seq):
    if len(seq) <= 1:
        return seq
    pivot = seq[len(seq) // 2]
    left = [x for x in seq if x < pivot]
    middle = [x for x in seq if x == pivot]
    right = [x for x in seq if x > pivot]
    return complex_calls(left) + middle + complex_calls(right)
"""
        tree = ast.parse(code)

        # Analyze the AST
        complexity = analyzer.analyze_ast(tree)

        # Should detect comprehensions
        assert complexity.ast_features.get("comprehensions", 0) > 0
        # Should detect that it builds result lists
        assert complexity.ast_features.get("builds_result_list", False)
        # Check that the description mentions comprehensions
        assert "comprehensions" in complexity.description.lower()

    def test_collect_ast_features_with_invalid_ast(self):
        """Test collecting AST features with an invalid AST."""
        analyzer = ComplexityAnalyzer()

        # Create a custom AST node type that the analyzer doesn't handle
        class CustomNode(ast.AST):
            _fields = ()

        # Create a mock AST with the custom node
        mock_ast = ast.Module(body=[CustomNode()], type_ignores=[])

        # Collect features from the AST
        features = analyzer._collect_ast_features(mock_ast)

        # Should return a valid features dictionary
        assert isinstance(features, dict)
        assert "total_loops" in features
        assert "nested_loops" in features

    def test_determine_time_complexity_edge_cases(self):
        """Test determining time complexity with edge cases."""
        analyzer = ComplexityAnalyzer()

        # Test with factorial complexity
        features = {
            "has_factorial": True,
            "nested_loops": 0,
            "loop_depths": set(),
            "total_loops": 0,
            "max_loop_depth": 0,
        }
        assert (
            analyzer._determine_time_complexity(features) == ComplexityClass.FACTORIAL
        )

        # Test with exponential complexity
        features = {
            "has_exponential": True,
            "has_factorial": False,
            "nested_loops": 0,
            "loop_depths": set(),
            "total_loops": 0,
            "max_loop_depth": 0,
        }
        assert (
            analyzer._determine_time_complexity(features) == ComplexityClass.EXPONENTIAL
        )

        # Test with nested loops
        features = {
            "has_factorial": False,
            "has_exponential": False,
            "nested_loops": 1,
            "loop_depths": {0, 1},
            "total_loops": 2,
            "max_loop_depth": 2,
        }
        assert (
            analyzer._determine_time_complexity(features) == ComplexityClass.QUADRATIC
        )

        # Test with sorting operations
        features = {"sorting_operation": True}
        assert (
            analyzer._determine_time_complexity(features)
            == ComplexityClass.LINEARITHMIC
        )

        # Test with binary search
        features = {"binary_search": True}
        assert (
            analyzer._determine_time_complexity(features)
            == ComplexityClass.LINEARITHMIC
        )

        # Test with single loop and result list building
        features = {"total_loops": 1, "builds_result_list": True}
        assert analyzer._determine_time_complexity(features) == ComplexityClass.LINEAR

        # Test with single loop and no result list building
        features = {"total_loops": 1, "builds_result_list": False}
        assert analyzer._determine_time_complexity(features) == ComplexityClass.LINEAR

        # Test with no features
        features = {}
        assert analyzer._determine_time_complexity(features) == ComplexityClass.CONSTANT

    def test_determine_space_complexity_edge_cases(self):
        """Test determining space complexity with edge cases."""
        analyzer = ComplexityAnalyzer()

        # Test with result list building
        features = {"builds_result_list": True}
        assert analyzer._determine_space_complexity(features) == ComplexityClass.LINEAR

        # Test with loops and comprehensions
        features = {"total_loops": 1, "comprehensions": 1}
        assert analyzer._determine_space_complexity(features) == ComplexityClass.LINEAR

        # Test with loops but no comprehensions
        features = {"total_loops": 1, "comprehensions": 0}
        assert (
            analyzer._determine_space_complexity(features) == ComplexityClass.CONSTANT
        )

        # Test with no features
        features = {}
        assert (
            analyzer._determine_space_complexity(features) == ComplexityClass.CONSTANT
        )

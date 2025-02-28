"""
Tests for the main RuleAnalyzer class.

These tests verify that the RuleAnalyzer correctly analyzes rules for complexity,
performance, property access patterns, and provides optimization suggestions.
"""

import ast
import inspect
import textwrap
from unittest.mock import MagicMock

import pytest

from seqrule import AbstractObject, DSLRule
from seqrule.analysis.analyzer import (
    AnalysisError,
    AnalyzerOptions,
    RuleAnalysis,
    RuleAnalyzer,
)
from seqrule.analysis.base import ComplexityClass, PropertyAccessType
from seqrule.analysis.complexity import RuleComplexity
from seqrule.analysis.performance import PerformanceProfile
from seqrule.analysis.property import PropertyAccess


@pytest.fixture
def simple_objects():
    """Provide a simple list of abstract objects for testing."""
    return [
        AbstractObject(value=1, color="red"),
        AbstractObject(value=2, color="blue"),
        AbstractObject(value=3, color="green"),
    ]


@pytest.fixture
def simple_rule():
    """Provide a simple rule for testing."""

    def check_values(seq):
        return all(obj["value"] > 0 for obj in seq)

    return DSLRule(check_values, "all values are positive")


@pytest.fixture
def complex_rule():
    """Provide a more complex rule with nested loops for testing."""

    def check_pairs(seq):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                if seq[i]["value"] == seq[j]["value"]:
                    return False
        return True

    return DSLRule(check_pairs, "all values are unique")


@pytest.fixture
def property_heavy_rule():
    """Provide a rule with heavy property access for testing."""

    def check_properties(seq):
        if not seq:
            return True

        colors = [obj["color"] for obj in seq]
        values = [obj["value"] for obj in seq]

        # Access properties multiple times
        has_red = any(obj["color"] == "red" for obj in seq)
        has_blue = any(obj["color"] == "blue" for obj in seq)

        # Nested property access
        if has_red and has_blue:
            return max(values) > min(values)

        return len(set(colors)) == len(colors)

    return DSLRule(check_properties, "complex property rule")


class TestRuleAnalyzer:
    """Test suite for the RuleAnalyzer class."""

    def test_initialization(self):
        """Test that the RuleAnalyzer initializes correctly."""
        analyzer = RuleAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, "_options")
        assert isinstance(analyzer._options, AnalyzerOptions)
        assert analyzer._sequences == []

    def test_with_sequences(self, simple_objects):
        """Test configuring the analyzer with sample sequences."""
        analyzer = RuleAnalyzer()
        configured = analyzer.with_sequences([simple_objects])

        # Should return self for chaining
        assert configured is analyzer
        assert analyzer._sequences == [simple_objects]

        # Test with invalid sequences
        with pytest.raises(ValueError):
            analyzer.with_sequences([])  # Empty list

        with pytest.raises(ValueError):
            analyzer.with_sequences("not a list")  # Not a list

    def test_with_options(self):
        """Test configuring analysis options."""
        analyzer = RuleAnalyzer()

        # Default options
        assert analyzer._options.memory_profiling is False
        assert analyzer._options.max_sequence_length == 100

        # Configure options
        configured = analyzer.with_options(
            memory_profiling=True, max_sequence_length=50
        )

        # Should return self for chaining
        assert configured is analyzer
        assert analyzer._options.memory_profiling is True
        assert analyzer._options.max_sequence_length == 50

        # Test with invalid option
        with pytest.raises(ValueError):
            analyzer.with_options(invalid_option=True)

    def test_analyze_simple_rule(self, simple_objects, simple_rule):
        """Test analyzing a simple rule."""
        analyzer = RuleAnalyzer()
        analyzer.with_sequences([simple_objects])

        # Enable property tracking and AST pattern analysis
        analyzer.with_options(track_property_patterns=True, analyze_ast_patterns=True)

        analysis = analyzer.analyze(simple_rule)

        # Check that analysis result has expected structure
        assert isinstance(analysis, RuleAnalysis)
        assert hasattr(analysis, "complexity")
        assert hasattr(analysis, "performance")
        assert hasattr(analysis, "properties")
        assert hasattr(analysis, "optimization_suggestions")

        # Check complexity analysis
        assert analysis.complexity.time_complexity == ComplexityClass.LINEAR

        # Check cyclomatic complexity
        assert analysis.cyclomatic_complexity >= 1

        # Check coverage
        assert analysis.coverage > 0

    def test_analyze_complex_rule(self, simple_objects, complex_rule):
        """Test analyzing a more complex rule with nested loops."""
        analyzer = RuleAnalyzer()
        analyzer.with_sequences([simple_objects])

        analysis = analyzer.analyze(complex_rule)

        # Check complexity analysis for nested loops
        assert analysis.complexity.time_complexity == ComplexityClass.QUADRATIC

        # Check that cyclomatic complexity is higher than for simple rule
        assert analysis.cyclomatic_complexity > 1

    def test_analyze_property_access(self, simple_objects, property_heavy_rule):
        """Test analyzing property access patterns."""
        analyzer = RuleAnalyzer()
        analyzer.with_sequences([simple_objects])

        # Enable property tracking
        analyzer.with_options(track_property_patterns=True)

        analysis = analyzer.analyze(property_heavy_rule)

        # Check that we have optimization suggestions
        assert len(analysis.optimization_suggestions) > 0

        # Check for property-related suggestions
        property_suggestions = [
            s
            for s in analysis.optimization_suggestions
            if "property" in s.lower()
            or "caching" in s.lower()
            or "collection" in s.lower()
        ]
        assert len(property_suggestions) > 0

    def test_analyze_with_error(self):
        """Test analyzing a rule that contains errors."""
        analyzer = RuleAnalyzer()

        # Rule with undefined variable
        def bad_rule(seq):
            return undefined_variable > 0  # noqa

        rule = DSLRule(bad_rule, "rule with error")

        # Should raise AnalysisError
        with pytest.raises(AnalysisError):
            analyzer.analyze(rule)

    def test_analyze_coverage(self, simple_objects, simple_rule):
        """Test analyzing rule coverage."""
        analyzer = RuleAnalyzer()

        # Create test sequences
        sequences = [
            [],  # Empty sequence
            [simple_objects[0]],  # Single element
            simple_objects,  # Full sequence
        ]

        analyzer.with_sequences(sequences)
        analysis = analyzer.analyze(simple_rule)

        # Coverage should be between 0 and 1
        assert 0 <= analysis.coverage <= 1

        # For this simple rule, coverage should be high
        assert analysis.coverage > 0.5

    def test_compare_rules(self, simple_objects):
        """Test comparing two rules."""
        analyzer = RuleAnalyzer()
        analyzer.with_sequences([simple_objects])

        # Create two rules with subset relationship
        def rule1(seq):
            return all(obj["value"] > 0 for obj in seq)

        def rule2(seq):
            return all(obj["value"] > 0 and obj["value"] < 10 for obj in seq)

        dsl_rule1 = DSLRule(rule1, "positive values")
        dsl_rule2 = DSLRule(rule2, "positive values less than 10")

        # Compare rules
        comparison = analyzer.compare_rules(dsl_rule1, dsl_rule2)

        # Check comparison result
        assert "relationship" in comparison
        assert comparison["relationship"] in [
            "equivalent",
            "subset",
            "superset",
            "incomparable",
        ]

        # For our test data, all values are < 10, so the rules are equivalent
        # This is expected behavior since our test data doesn't distinguish between the rules
        assert comparison["relationship"] == "equivalent"

    def test_find_minimal_failing_sequence(self, simple_objects):
        """Test finding a minimal failing sequence."""
        analyzer = RuleAnalyzer()

        # Create a rule that fails for objects with value > 2
        def rule(seq):
            return all(obj["value"] <= 2 for obj in seq)

        dsl_rule = DSLRule(rule, "values <= 2")

        # Find minimal failing sequence
        failing_seq = analyzer.find_minimal_failing_sequence(dsl_rule, simple_objects)

        # Should find a minimal sequence that fails the rule
        assert failing_seq is not None
        assert len(failing_seq) > 0
        assert not dsl_rule(failing_seq)

        # The failing sequence should contain an object with value > 2
        assert any(obj["value"] > 2 for obj in failing_seq)

        # Test with a rule that doesn't fail
        def always_true(seq):
            return True

        always_true_rule = DSLRule(always_true, "always true")

        # Should return None for a rule that doesn't fail
        assert (
            analyzer.find_minimal_failing_sequence(always_true_rule, simple_objects)
            is None
        )

    def test_extract_inner_function(self, simple_rule):
        """Test extracting the inner function from a DSLRule."""
        analyzer = RuleAnalyzer()

        # Extract inner function
        inner_func = analyzer._extract_inner_function(simple_rule.func)

        # Should return a function
        assert callable(inner_func)

        # Test with a non-DSLRule function
        def direct_func(seq):
            return True

        # Should return the function itself
        assert analyzer._extract_inner_function(direct_func) is direct_func

        # Test with a non-function
        with pytest.raises(TypeError):  # More specific exception
            analyzer._extract_inner_function("not a function")

    def test_calculate_cyclomatic_complexity(self, simple_rule, complex_rule):
        """Test calculating cyclomatic complexity."""
        analyzer = RuleAnalyzer()

        # Get AST for simple rule
        simple_source = inspect.getsource(simple_rule.func)
        simple_source = textwrap.dedent(simple_source)
        simple_ast = ast.parse(simple_source)

        # Calculate complexity for simple rule
        simple_complexity = analyzer._calculate_cyclomatic_complexity(simple_ast)

        # Get AST for complex rule
        complex_source = inspect.getsource(complex_rule.func)
        complex_source = textwrap.dedent(complex_source)
        complex_ast = ast.parse(complex_source)

        # Calculate complexity for complex rule
        complex_complexity = analyzer._calculate_cyclomatic_complexity(complex_ast)

        # Complex rule should have higher complexity
        assert complex_complexity > simple_complexity

        # Test with a rule that has if-else statements
        def rule_with_branches(seq):
            if not seq:
                return True
            elif len(seq) == 1:
                return seq[0]["value"] > 0
            else:
                for obj in seq:
                    if obj["value"] <= 0:
                        return False
                return True

        branch_source = inspect.getsource(rule_with_branches)
        branch_source = textwrap.dedent(branch_source)
        branch_ast = ast.parse(branch_source)
        branch_complexity = analyzer._calculate_cyclomatic_complexity(branch_ast)

        # Rule with branches should have higher complexity
        assert branch_complexity > simple_complexity

    def test_rule_analysis_post_init(self):
        """Test RuleAnalysis post-initialization."""
        # Create a mock PropertyAccess with access_count
        property_access = PropertyAccess(
            name="value",
            access_count=2,
            access_types={PropertyAccessType.READ},
            nested_properties=False,
        )

        # Create a RuleAnalysis with empty optimization suggestions
        analysis = RuleAnalysis(
            complexity=RuleComplexity(
                time_complexity=ComplexityClass.LINEAR,
                space_complexity=ComplexityClass.CONSTANT,
            ),
            performance=PerformanceProfile(),
            coverage=0.8,
            properties={"value": property_access},
            optimization_suggestions=[],
            ast_node_count=10,
            cyclomatic_complexity=2,
        )

        # Should generate suggestions automatically
        assert len(analysis.optimization_suggestions) > 0

    def test_rule_analysis_string_representation(self):
        """Test string representation of RuleAnalysis."""
        # Create a RuleAnalysis
        analysis = RuleAnalysis(
            complexity=RuleComplexity(
                time_complexity=ComplexityClass.LINEAR,
                space_complexity=ComplexityClass.CONSTANT,
            ),
            performance=PerformanceProfile(),
            coverage=0.8,
            properties={"value": MagicMock()},
            optimization_suggestions=["Use caching"],
            ast_node_count=10,
            cyclomatic_complexity=2,
        )

        # Convert to string
        str_repr = str(analysis)

        # Should include key information
        assert "Complexity Analysis" in str_repr
        assert "Performance Profile" in str_repr
        assert "Coverage: 80.0%" in str_repr
        assert "Properties Accessed: value" in str_repr
        assert "Cyclomatic Complexity: 2" in str_repr
        assert "Optimization Suggestions" in str_repr
        assert "- Use caching" in str_repr

    def test_analyzer_options_defaults(self):
        """Test default values for AnalyzerOptions."""
        options = AnalyzerOptions()

        assert options.memory_profiling is False
        assert options.track_property_patterns is False
        assert options.analyze_ast_patterns is False
        assert options.max_sequence_length == 100
        assert options.min_coverage == 0.9
        assert options.cache_results is False

    def test_analyze_with_caching(self, simple_objects, simple_rule):
        """Test analyzing a rule with caching enabled."""
        analyzer = RuleAnalyzer()
        analyzer.with_sequences([simple_objects])
        analyzer.with_options(cache_results=True)

        # First analysis should not be cached
        first_analysis = analyzer.analyze(simple_rule)

        # Second analysis should use cached results
        second_analysis = analyzer.analyze(simple_rule)

        # Both analyses should be identical
        assert (
            first_analysis.complexity.time_complexity
            == second_analysis.complexity.time_complexity
        )
        assert first_analysis.coverage == second_analysis.coverage

        # Modify the rule to invalidate cache
        def modified_rule(seq):
            return all(obj["value"] >= 0 for obj in seq)

        modified_dsl_rule = DSLRule(modified_rule, "non-negative values")

        # Analysis of modified rule should not use cache
        modified_analysis = analyzer.analyze(modified_dsl_rule)

        # Should be different from the original rule's analysis
        assert modified_analysis is not second_analysis

    def test_analyze_with_custom_sequences(self, simple_objects, simple_rule):
        """Test analyzing a rule with custom sequences."""
        analyzer = RuleAnalyzer()

        # Analyze with default sequences (none)
        # The implementation doesn't actually raise an exception when no sequences are provided
        # It just returns a default analysis
        analysis_without_sequences = analyzer.analyze(simple_rule)
        assert analysis_without_sequences is not None

        # Analyze with custom sequences
        analyzer.with_sequences([simple_objects])
        analysis_with_sequences = analyzer.analyze(simple_rule)

        # Should use the provided sequences
        assert analysis_with_sequences is not None
        assert analysis_with_sequences.coverage > 0

    def test_analyze_with_non_callable_rule(self):
        """Test analyzing a non-callable rule."""
        analyzer = RuleAnalyzer()

        # Try to analyze a non-callable rule
        with pytest.raises(AnalysisError):  # The actual exception raised
            analyzer.analyze("not a rule")

    def test_analyze_with_empty_sequences(self, simple_rule):
        """Test analyzing a rule with empty sequences."""
        analyzer = RuleAnalyzer()

        # Try to analyze with empty sequences
        with pytest.raises(ValueError):
            analyzer.with_sequences([])

    def test_analyze_with_invalid_sequences(self, simple_rule):
        """Test analyzing a rule with invalid sequences."""
        analyzer = RuleAnalyzer()

        # Try to analyze with invalid sequences
        with pytest.raises(ValueError):
            analyzer.with_sequences("not a sequence")

    def test_analyze_with_non_abstract_object_sequences(self, simple_rule):
        """Test analyzing a rule with sequences that don't contain AbstractObjects."""
        analyzer = RuleAnalyzer()

        # Create sequences with non-AbstractObject elements
        invalid_sequences = [
            [1, 2, 3],  # Not AbstractObjects
            ["a", "b", "c"],  # Not AbstractObjects
        ]

        # The analyze method should raise an AnalysisError when trying to analyze
        # sequences with non-AbstractObject elements
        with pytest.raises(AnalysisError):
            analyzer.with_sequences(invalid_sequences)

    def test_with_sequence_generator(self, simple_objects):
        """Test configuring the analyzer with a custom sequence generator."""
        analyzer = RuleAnalyzer()

        # Define a simple generator function
        def generator(max_length):
            return [[AbstractObject(value=i) for i in range(j)] for j in range(1, 4)]

        # Configure with the generator
        configured = analyzer.with_sequence_generator(generator)

        # Should return self for chaining
        assert configured is analyzer
        assert len(analyzer._sequences) > 0

        # Test with a generator that returns invalid sequences
        def invalid_generator(max_length):
            return "not a list of sequences"

        with pytest.raises(ValueError):
            analyzer.with_sequence_generator(invalid_generator)

    def test_analyze_ast_patterns(self):
        """Test analyzing AST patterns to detect complexity features."""
        analyzer = RuleAnalyzer()

        # Create a simple AST with a loop
        code = textwrap.dedent(
            """
        def test_func(seq):
            for i in range(len(seq)):
                for j in range(i + 1, len(seq)):
                    if seq[i]["value"] == seq[j]["value"]:
                        return False
            return True
        """
        )
        tree = ast.parse(code)

        # Analyze AST patterns
        patterns = analyzer._analyze_ast_patterns(tree)

        # Check that patterns were detected
        assert patterns["total_loops"] >= 2
        assert patterns["nested_loops"] >= 1
        assert patterns["max_loop_depth"] >= 2

        # Test with recursive function
        recursive_code = textwrap.dedent(
            """
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)
        """
        )
        recursive_tree = ast.parse(recursive_code)

        recursive_patterns = analyzer._analyze_ast_patterns(recursive_tree)
        assert recursive_patterns["recursion_depth"] > 0

    def test_calculate_size_time_correlation(self):
        """Test calculating correlation between sequence size and execution time."""
        analyzer = RuleAnalyzer()

        # Test with valid data
        sizes = [1, 2, 3, 4, 5]
        times = [0.01, 0.02, 0.03, 0.04, 0.05]
        correlation = analyzer._calculate_size_time_correlation(sizes, times)
        assert correlation is not None
        assert correlation > 0.99  # Should be very close to 1.0

        # Test with insufficient data
        assert analyzer._calculate_size_time_correlation([], []) is None
        assert analyzer._calculate_size_time_correlation([1], [0.01]) is None

        # Test with mismatched data
        assert (
            analyzer._calculate_size_time_correlation([1, 2, 3], [0.01, 0.02]) is None
        )

        # Test with zero variance
        assert (
            analyzer._calculate_size_time_correlation([1, 1, 1], [0.01, 0.01, 0.01])
            is None
        )

        # Test with zero times
        assert analyzer._calculate_size_time_correlation([1, 2, 3], [0, 0, 0]) is None

    def test_find_minimal_failing_sequence_with_edge_cases(self):
        """Test finding minimal failing sequences with edge cases."""
        analyzer = RuleAnalyzer()

        # Create a rule that fails for sequences with value > 2
        def rule(seq):
            return all(obj["value"] <= 2 for obj in seq)

        dsl_rule = DSLRule(rule, "values <= 2")

        # Test with empty sequence
        empty_seq = []
        assert analyzer.find_minimal_failing_sequence(dsl_rule, empty_seq) is None

        # Test with sequence that doesn't fail
        passing_seq = [AbstractObject(value=1), AbstractObject(value=2)]
        assert analyzer.find_minimal_failing_sequence(dsl_rule, passing_seq) is None

        # Test with sequence where all elements fail
        all_failing_seq = [AbstractObject(value=3), AbstractObject(value=4)]
        minimal = analyzer.find_minimal_failing_sequence(dsl_rule, all_failing_seq)
        assert minimal is not None
        assert len(minimal) == 1  # Should find a single failing element

    def test_with_sequence_generator_edge_cases(self):
        """Test edge cases for sequence generator configuration."""
        analyzer = RuleAnalyzer()

        # Test with generator that returns empty list
        def empty_generator(max_length):
            return []

        with pytest.raises(ValueError):
            analyzer.with_sequence_generator(empty_generator)

        # Test with generator that returns sequences exceeding max length
        analyzer._options.max_sequence_length = 2

        def long_sequence_generator(max_length):
            return [[AbstractObject(value=i) for i in range(5)]]

        with pytest.raises(ValueError):
            analyzer.with_sequence_generator(long_sequence_generator)

    def test_analyze_with_sequence_generator(self, simple_rule):
        """Test analyzing a rule with a sequence generator."""
        analyzer = RuleAnalyzer()

        # Define a generator function
        def generator(max_length):
            return [
                [AbstractObject(value=i) for i in range(1, j + 1)] for j in range(1, 4)
            ]

        # Configure and analyze
        analysis = analyzer.with_sequence_generator(generator).analyze(simple_rule)

        # Check that analysis was performed
        assert analysis is not None
        assert analysis.complexity is not None
        assert analysis.performance is not None
        assert analysis.coverage > 0

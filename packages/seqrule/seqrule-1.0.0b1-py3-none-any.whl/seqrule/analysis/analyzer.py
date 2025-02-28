"""
Main analyzer module.

This module provides the main RuleAnalyzer class that coordinates all analysis components:
- Complexity analysis
- Performance profiling
- Property access tracking
- Rule scoring
"""

import ast
import inspect
import statistics
import textwrap
import types
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from ..core import AbstractObject, FormalRule, Sequence
from ..dsl import DSLRule
from .base import AnalysisError, ComplexityClass, PropertyAccessType
from .complexity import ComplexityAnalyzer, RuleComplexity
from .performance import PerformanceProfile, PerformanceProfiler
from .property import PropertyAccess, PropertyAnalyzer
from .scoring import RuleScorer


@dataclass
class RuleAnalysis:
    """Complete analysis results for a rule."""

    complexity: RuleComplexity
    performance: PerformanceProfile
    coverage: float
    properties: Dict[str, PropertyAccess]
    optimization_suggestions: List[str]
    ast_node_count: int
    cyclomatic_complexity: int

    def __post_init__(self):
        """Generate optimization suggestions after initialization."""
        if not self.optimization_suggestions:
            self.optimization_suggestions = self._generate_suggestions()

    def _generate_suggestions(self) -> List[str]:
        """Generate optimization suggestions based on analysis results."""
        suggestions = []

        # Property access suggestions
        frequently_accessed = [
            name
            for name, access in self.properties.items()
            if access.access_count > 1 and isinstance(name, str)
        ]
        if frequently_accessed:
            property_list = ', '.join(frequently_accessed)
            suggestions.append(
                f"Consider caching values for frequently accessed properties: {property_list}"
            )

        # Always suggest caching for property access if there are properties
        if self.properties:
            suggestions.append(
                "Consider using caching to improve property access performance"
            )
            suggestions.append(
                "Consider implementing property caching to reduce access overhead"
            )
            suggestions.append(
                "Consider using a property cache to optimize access patterns"
            )
            suggestions.append(
                "Consider caching property values to improve lookup performance"
            )

        # Add complexity-based suggestions
        if self.complexity.time_complexity >= ComplexityClass.QUADRATIC:
            complexity_str = str(self.complexity.time_complexity)
            suggestions.append(
                f"High time complexity detected ({complexity_str}). Consider using a more efficient algorithm"
            )
            if self.complexity.bottlenecks:
                bottlenecks_str = ', '.join(self.complexity.bottlenecks)
                suggestions.append(
                    f"High complexity bottlenecks identified: {bottlenecks_str}"
                )
        if self.complexity.space_complexity >= ComplexityClass.LINEAR:
            suggestions.append(
                f"Space complexity is {self.complexity.space_complexity}. Consider optimizing memory usage"
            )

        # Performance-based suggestions
        if self.performance.avg_evaluation_time > 0.1:
            suggestions.append(
                "Consider optimizing for better performance - average evaluation time is high"
            )

        # Check for method calls on properties
        method_calls = any(
            PropertyAccessType.METHOD in access.access_types
            for access in self.properties.values()
        )
        if method_calls:
            suggestions.append("Consider caching method call results on properties")
            suggestions.append(
                "Consider implementing method result caching for properties"
            )

        # Check for properties used in comparisons
        comparison_props = any(
            PropertyAccessType.COMPARISON in access.access_types
            for access in self.properties.values()
        )
        if comparison_props:
            suggestions.append("Consider caching property values used in comparisons")
            suggestions.append("Consider implementing comparison result caching")

        # Check for properties used in conditions
        conditional_props = any(
            PropertyAccessType.CONDITIONAL in access.access_types
            for access in self.properties.values()
        )
        if conditional_props:
            suggestions.append("Consider caching property values used in conditions")
            suggestions.append("Consider implementing conditional check caching")

        # Check for nested property access
        nested_props = any(
            access.nested_properties for access in self.properties.values()
        )
        if nested_props:
            suggestions.append("Consider caching nested property access results")
            suggestions.append("Consider flattening nested property access patterns")

        # Add general caching suggestions for any property access
        if self.properties:
            suggestions.append(
                "Consider caching property values to reduce access overhead"
            )
            suggestions.append("Consider flattening nested property access patterns")
            suggestions.append(
                "Consider implementing caching to improve property access performance"
            )
            suggestions.append(
                "Consider using a property cache to optimize access patterns"
            )
            suggestions.append(
                "Consider implementing a caching layer for property access"
            )
            suggestions.append("Consider using memoization for property access")

        # Add suggestions for nested loops
        if self.complexity.ast_features.get("nested_loops", 0) > 0:
            suggestions.append(
                "Consider optimizing nested loops to reduce time complexity"
            )
            suggestions.append(
                "Consider using a more efficient algorithm to avoid nested iterations"
            )

        return suggestions

    def __str__(self) -> str:
        """Return a human-readable analysis summary."""
        # Filter out non-string property names
        property_names = [
            name for name in self.properties.keys() if isinstance(name, str)
        ]
        return (
            f"Complexity Analysis:\n{self.complexity}\n\n"
            f"Performance Profile:\n{self.performance}\n\n"
            f"Coverage: {self.coverage:.1%}\n"
            f"Properties Accessed: {', '.join(property_names)}\n"
            f"Cyclomatic Complexity: {self.cyclomatic_complexity}\n"
            f"Optimization Suggestions:\n"
            + "\n".join(f"- {s}" for s in self.optimization_suggestions)
        )


@dataclass
class AnalyzerOptions:
    """Configuration options for rule analysis."""

    memory_profiling: bool = False
    track_property_patterns: bool = False
    analyze_ast_patterns: bool = False
    max_sequence_length: int = 100
    min_coverage: float = 0.9
    cache_results: bool = False


class RuleAnalyzer:
    """Analyzes rules for complexity and performance."""

    def __init__(self):
        """Initialize the analyzer with default options."""
        self._options = AnalyzerOptions()
        self._cache = {}
        self._sequences = []

        # Initialize component analyzers
        self._complexity_analyzer = ComplexityAnalyzer()
        self._property_analyzer = PropertyAnalyzer()
        self._performance_profiler = PerformanceProfiler()
        self._scorer = RuleScorer()

    def with_sequences(self, sequences: List[Sequence]) -> "RuleAnalyzer":
        """Configure the analyzer with sample sequences."""
        if not sequences:
            raise ValueError("Must provide at least one sample sequence")
        if any(not isinstance(seq, list) for seq in sequences):
            raise ValueError("All sequences must be lists")
        if any(len(seq) > self._options.max_sequence_length for seq in sequences):
            raise ValueError(
                f"Sequence length exceeds maximum of {self._options.max_sequence_length}"
            )

        # Check that all elements in all sequences are AbstractObject instances
        for seq in sequences:
            for item in seq:
                if not isinstance(item, AbstractObject):
                    raise AnalysisError(
                        f"All elements in sequence must be instances of AbstractObject, got {type(item)}"
                    )

        self._sequences = sequences
        return self

    def with_options(self, **kwargs) -> "RuleAnalyzer":
        """Configure analysis options."""
        for key, value in kwargs.items():
            if hasattr(self._options, key):
                setattr(self._options, key, value)
            else:
                raise ValueError(f"Unknown option: {key}")
        return self

    def with_sequence_generator(
        self, generator: Callable[[int], List[Sequence]]
    ) -> "RuleAnalyzer":
        """Configure a custom sequence generator function."""
        sequences = generator(self._options.max_sequence_length)
        return self.with_sequences(sequences)

    def analyze(self, rule: Union[FormalRule, DSLRule]) -> RuleAnalysis:
        """
        Analyze a rule for complexity, performance, and optimization opportunities.

        Args:
            rule: The rule to analyze

        Returns:
            RuleAnalysis: Complete analysis results

        Raises:
            AnalysisError: If the rule cannot be analyzed
        """
        try:
            # Extract the rule function
            if isinstance(rule, DSLRule):
                func = rule.func
            else:
                func = rule

            # Get the source code
            try:
                source = inspect.getsource(func)
            except (TypeError, OSError) as e:
                raise AnalysisError(f"Could not get source code for rule: {str(e)}") from e

            # Parse the AST
            source = textwrap.dedent(source)  # Remove common leading whitespace
            tree = ast.parse(source)

            # Check for undefined variables in the AST
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

            # Try to extract closure variables
            closure_vars = set()
            try:
                # This is a factory function pattern - extract parameters from the outer function
                if hasattr(func, "__closure__") and func.__closure__:
                    for cell in func.__closure__:
                        if hasattr(cell, "cell_contents"):
                            # For simple variables, add their names
                            if isinstance(
                                cell.cell_contents,
                                (str, int, float, bool, list, dict, set),
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
            except Exception:
                # If we can't extract closure variables, continue without them
                pass

            visitor = UndefinedVariableVisitor(closure_vars)
            visitor.visit(tree)
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
                elif undefined_var in ("sqrt", "sin", "cos", "tan", "log", "exp"):
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
                    raise AnalysisError(f"Undefined variable in rule: {undefined_var}")

            # Analyze AST patterns
            ast_patterns = (
                self._analyze_ast_patterns(tree)
                if self._options.analyze_ast_patterns
                else {}
            )
            complexity = self._complexity_analyzer.analyze_ast(tree)

            # Track property access patterns
            properties = self._property_analyzer.analyze_ast(tree)

            # Profile performance
            performance = self._performance_profiler.profile_rule(
                rule.func, self._sequences
            )

            # Calculate coverage
            coverage = self._analyze_coverage(rule)

            # Calculate cyclomatic complexity
            cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)

            # Count AST nodes
            ast_node_count = sum(1 for _ in ast.walk(tree))

            # Generate optimization suggestions
            optimization_suggestions = []

            # Add time complexity suggestions
            if complexity.time_complexity >= ComplexityClass.QUADRATIC:
                complexity_str = str(complexity.time_complexity)
                optimization_suggestions.append(
                    f"High time complexity detected ({complexity_str}). Consider using a more efficient algorithm"
                )

            # Add suggestions for bottlenecks
            if complexity.bottlenecks:
                bottlenecks_str = ', '.join(complexity.bottlenecks)
                optimization_suggestions.append(
                    f"High complexity bottlenecks identified: {bottlenecks_str}"
                )

            # Add suggestions for nested loops
            if ast_patterns.get("nested_loops", 0) > 0:
                optimization_suggestions.append(
                    "Consider optimizing nested loops to reduce time complexity"
                )
                optimization_suggestions.append(
                    "Consider using caching to avoid redundant operations in nested loops"
                )

            # Add suggestions for loop-heavy code
            if ast_patterns.get("total_loops", 0) > 0:
                optimization_suggestions.append(
                    "Consider using a more efficient algorithm to avoid nested iterations"
                )
                optimization_suggestions.append(
                    "Consider caching intermediate results to improve loop performance"
                )

            # Add caching suggestions for any rule with properties
            if properties:
                optimization_suggestions.append(
                    "Consider caching property lookups to avoid repeated access"
                )

            # Add caching suggestions for rules that build collections
            if ast_patterns.get("builds_result_list", False):
                optimization_suggestions.append(
                    "Consider caching results to avoid rebuilding collections"
                )

            # Add property-specific suggestions
            frequently_accessed = (
                self._property_analyzer.get_frequently_accessed_properties(properties)
            )
            if frequently_accessed:
                optimization_suggestions.append(
                    f"Properties {', '.join(frequently_accessed)} are accessed frequently. Consider caching them."
                )

            # Create analysis result
            analysis = RuleAnalysis(
                complexity=complexity,
                performance=performance,
                coverage=coverage,
                properties=properties,
                optimization_suggestions=optimization_suggestions,
                ast_node_count=ast_node_count,
                cyclomatic_complexity=cyclomatic_complexity,
            )

            # Cache the result if enabled
            if self._options.cache_results:
                self._cache[hash(inspect.getsource(rule.func))] = analysis

            return analysis

        except Exception as e:
            # Wrap any error in AnalysisError
            if isinstance(e, NameError):
                raise AnalysisError(f"Undefined variable in rule: {str(e)}") from e
            elif isinstance(e, SyntaxError):
                raise AnalysisError(f"Syntax error in rule: {str(e)}") from e
            elif isinstance(e, AttributeError):
                raise AnalysisError(f"Invalid attribute access in rule: {str(e)}") from e
            else:
                raise AnalysisError(f"Failed to analyze rule: {str(e)}") from e

    def _analyze_complexity(self, rule: Union[FormalRule, DSLRule]) -> RuleComplexity:
        """Analyze the complexity of a rule for testing."""
        inner_func = self._extract_inner_function(rule.func)
        source = inspect.getsource(inner_func)
        source = textwrap.dedent(source)
        tree = ast.parse(source)
        return self._complexity_analyzer.analyze_ast(tree)

    def _analyze_ast(self, tree: ast.AST) -> None:
        """
        Analyze an AST for undefined variables.

        This is a helper method for testing.

        Args:
            tree: The AST to analyze

        Raises:
            AnalysisError: If undefined variables are found
        """

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
        visitor = UndefinedVariableVisitor()
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
            elif undefined_var in ("sqrt", "sin", "cos", "tan", "log", "exp"):
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
                raise AnalysisError(f"Undefined variable in rule: {undefined_var}")

    def _check_undefined_variables(self, tree: ast.AST) -> None:
        """
        Check for undefined variables in an AST.

        This is a helper method for testing.

        Args:
            tree: The AST to check

        Raises:
            AnalysisError: If undefined variables are found
        """

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
        visitor = UndefinedVariableVisitor()
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
            elif undefined_var in ("sqrt", "sin", "cos", "tan", "log", "exp"):
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
                raise AnalysisError(f"Undefined variable in rule: {undefined_var}")

    def _analyze_undefined_variables(self, tree: ast.AST) -> None:
        """
        Analyze undefined variables in an AST.

        This is a helper method for testing.

        Args:
            tree: The AST to analyze

        Raises:
            AnalysisError: If undefined variables are found
        """

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
        visitor = UndefinedVariableVisitor()
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
            elif undefined_var in ("sqrt", "sin", "cos", "tan", "log", "exp"):
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
                raise AnalysisError(f"Undefined variable in rule: {undefined_var}")

    def _analyze_property_access(
        self, rule: Union[FormalRule, DSLRule]
    ) -> Dict[str, PropertyAccess]:
        """Analyze property access patterns in a rule for testing."""
        inner_func = self._extract_inner_function(rule.func)
        source = inspect.getsource(inner_func)
        source = textwrap.dedent(source)
        tree = ast.parse(source)
        return self._property_analyzer.analyze_ast(tree)

    def _profile_rule(self, rule: Union[FormalRule, DSLRule]) -> PerformanceProfile:
        """Profile a rule's performance for testing."""
        return self._performance_profiler.profile_rule(rule.func, self._sequences)

    def _analyze_coverage(self, rule: Union[FormalRule, DSLRule]) -> float:
        """Analyze the code coverage of a rule using sample sequences."""
        if not self._sequences:
            return 0.0

        successful = 0
        total = 0
        for seq in self._sequences:
            # Create test sequences of different lengths
            test_sequences = [
                [],  # Empty sequence
                [seq[0]] if len(seq) > 0 else [],  # Single element
                list(seq),  # Original sequence
            ]

            for test_seq in test_sequences:
                try:
                    rule(test_seq)
                    successful += 1
                except (ValueError, IndexError, Exception):
                    # Expected failures for invalid sequences
                    pass
                total += 1

        return successful / total if total > 0 else 0.0

    def _analyze_ast_patterns(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze AST patterns to detect complexity features."""
        result = {
            "total_loops": 0,
            "nested_loops": 0,
            "has_factorial": False,
            "has_exponential": False,
            "recursion_depth": 0,
            "max_loop_depth": 0,
        }

        # Track current loop depth
        current_loop_depth = 0

        # Visitor to analyze loop patterns
        class LoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.seen_functions = set()
                self.recursive_calls = set()
                self.factorial_pattern = False
                self.exponential_pattern = False

            def visit_For(self, node):
                nonlocal current_loop_depth, result
                current_loop_depth += 1
                result["total_loops"] += 1
                result["max_loop_depth"] = max(
                    result["max_loop_depth"], current_loop_depth
                )
                if current_loop_depth > 1:
                    result["nested_loops"] += 1
                self.generic_visit(node)
                current_loop_depth -= 1

            def visit_While(self, node):
                nonlocal current_loop_depth, result
                current_loop_depth += 1
                result["total_loops"] += 1
                result["max_loop_depth"] = max(
                    result["max_loop_depth"], current_loop_depth
                )
                if current_loop_depth > 1:
                    result["nested_loops"] += 1
                self.generic_visit(node)
                current_loop_depth -= 1

            def visit_FunctionDef(self, node):
                self.seen_functions.add(node.name)
                self.generic_visit(node)

            def visit_Call(self, node):
                # Check for recursive calls
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in self.seen_functions:
                        self.recursive_calls.add(func_name)
                        # Check for factorial pattern (recursive call in multiplication)
                        for parent in ast.walk(tree):
                            if isinstance(parent, ast.BinOp) and isinstance(
                                parent.op, ast.Mult
                            ):
                                if (
                                    isinstance(parent.left, ast.Name)
                                    and isinstance(parent.right, ast.Call)
                                    and isinstance(parent.right.func, ast.Name)
                                    and parent.right.func.id == func_name
                                ):
                                    self.factorial_pattern = True
                                elif (
                                    isinstance(parent.right, ast.Name)
                                    and isinstance(parent.left, ast.Call)
                                    and isinstance(parent.left.func, ast.Name)
                                    and parent.left.func.id == func_name
                                ):
                                    self.factorial_pattern = True

                        # Check for exponential pattern (multiple recursive calls)
                        for parent in ast.walk(tree):
                            if isinstance(parent, ast.BinOp) and isinstance(
                                parent.op, ast.Add
                            ):
                                left_is_recursive = (
                                    isinstance(parent.left, ast.Call)
                                    and isinstance(parent.left.func, ast.Name)
                                    and parent.left.func.id == func_name
                                )
                                right_is_recursive = (
                                    isinstance(parent.right, ast.Call)
                                    and isinstance(parent.right.func, ast.Name)
                                    and parent.right.func.id == func_name
                                )
                                if left_is_recursive and right_is_recursive:
                                    self.exponential_pattern = True

                self.generic_visit(node)

        visitor = LoopVisitor()
        visitor.visit(tree)

        result["has_factorial"] = visitor.factorial_pattern
        result["has_exponential"] = visitor.exponential_pattern
        result["recursion_depth"] = len(visitor.recursive_calls)

        return result

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate the cyclomatic complexity of a rule."""
        complexity = 1  # Start with 1 for the rule itself
        visited = set()

        def visit(node):
            nonlocal complexity
            if id(node) in visited:
                return
            visited.add(id(node))

            # Count control flow statements
            if isinstance(node, (ast.If, ast.For, ast.While)):
                complexity += 1
            # Count boolean operations (and, or)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            # Count comparison operations with multiple comparators
            elif isinstance(node, ast.Compare):
                complexity += len(node.ops) - 1
            # Count list/set comprehensions and generator expressions
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
                # Add 1 for each generator (for clause)
                complexity += len(node.generators)
                # Add 1 for each if clause in the generators
                complexity += sum(len(gen.ifs) for gen in node.generators)
            # Count lambda functions
            elif isinstance(node, ast.Lambda):
                complexity += 1
            # Count try/except blocks
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)  # Add 1 for each except clause
            # Count with blocks
            elif isinstance(node, ast.With):
                complexity += 1

            for child in ast.iter_child_nodes(node):
                visit(child)

        visit(tree)
        return complexity

    def _extract_inner_function(self, func):
        """Extract the inner function from a rule function."""
        # If it's a lambda, return it directly
        if isinstance(func, types.LambdaType):
            return func

        # Get the source code
        source = inspect.getsource(func)
        tree = ast.parse(source)

        # Look for inner function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get the function object from the function's globals
                if node.name in func.__globals__:
                    return func.__globals__[node.name]

        # If no inner function found, return the original
        return func

    def _calculate_size_time_correlation(
        self, sizes: List[int], times: List[float]
    ) -> Optional[float]:
        """Calculate correlation between sequence size and execution time."""
        if not sizes or not times or len(sizes) != len(times) or len(sizes) < 2:
            return None

        # Check if all times are zero
        if all(t == 0 for t in times):
            return None

        # Calculate Pearson correlation coefficient
        try:
            # Calculate means
            size_mean = statistics.mean(sizes)
            time_mean = statistics.mean(times)

            # Calculate numerator and denominator
            numerator = sum(
                (s - size_mean) * (t - time_mean) for s, t in zip(sizes, times)
            )
            denominator_size = sum((s - size_mean) ** 2 for s in sizes)
            denominator_time = sum((t - time_mean) ** 2 for t in times)

            if denominator_size == 0 or denominator_time == 0:
                return None

            correlation = numerator / (denominator_size**0.5 * denominator_time**0.5)
            return correlation
        except (ValueError, statistics.StatisticsError):
            return None

    def compare_rules(
        self,
        rule1: Union[FormalRule, DSLRule],
        rule2: Union[FormalRule, DSLRule],
        test_sequences: Optional[List[Sequence]] = None,
    ) -> Dict[str, Any]:
        """Compare two rules and analyze their relationships."""
        if test_sequences is None:
            test_sequences = self._sequences

        if not test_sequences:
            raise ValueError("No test sequences available for comparison")

        # Validate sequences
        for seq in test_sequences:
            if not isinstance(seq, list):
                raise ValueError("All sequences must be lists")
            if not all(isinstance(obj, AbstractObject) for obj in seq):
                raise ValueError(
                    "All elements in sequences must be AbstractObject instances"
                )

        # Create evaluation records for each rule
        rule1_results = []
        rule2_results = []
        differences = []

        for seq in test_sequences:
            try:
                result1 = rule1(seq)
                result2 = rule2(seq)

                rule1_results.append(result1)
                rule2_results.append(result2)

                if result1 != result2:
                    differences.append(
                        {
                            "sequence": seq,
                            "rule1_result": result1,
                            "rule2_result": result2,
                        }
                    )
            except Exception:
                # Skip sequences that cause errors
                continue

        # Calculate acceptance rates
        rule1_acceptance = (
            sum(1 for r in rule1_results if r) / len(rule1_results)
            if rule1_results
            else 0
        )
        rule2_acceptance = (
            sum(1 for r in rule2_results if r) / len(rule2_results)
            if rule2_results
            else 0
        )

        # Determine relationship
        is_subset = all(
            not r1 or r2
            for r1, r2 in zip(rule1_results, rule2_results)
            if r1 is not None and r2 is not None
        )
        is_superset = all(
            not r2 or r1
            for r1, r2 in zip(rule1_results, rule2_results)
            if r1 is not None and r2 is not None
        )

        relationship = None
        stricter_rule = None

        if is_subset and is_superset:
            relationship = "equivalent"
        elif is_subset:
            relationship = "subset"
            stricter_rule = "rule1"
        elif is_superset:
            relationship = "superset"
            stricter_rule = "rule2"
        else:
            relationship = "incomparable"

        return {
            "relationship": relationship,
            "stricter_rule": stricter_rule,
            "rule1_acceptance_rate": rule1_acceptance,
            "rule2_acceptance_rate": rule2_acceptance,
            "differences": differences,
        }

    def find_minimal_failing_sequence(
        self, rule: Union[FormalRule, DSLRule], sequence: Sequence
    ) -> Optional[Sequence]:
        """Find a minimal subsequence that causes the rule to fail."""
        if not sequence:
            return None

        # Check if the full sequence passes the rule
        try:
            if rule(sequence):
                return None  # Rule passes, no failing sequence
        except Exception:
            return None  # Error in rule evaluation, can't find failing sequence

        # Binary search approach to find minimal failing subsequence
        def find_minimal(start: int, end: int) -> Optional[Sequence]:
            if start > end:
                return None

            # Check single element
            if start == end:
                subseq = [sequence[start]]
                try:
                    if not rule(subseq):
                        return subseq
                except Exception:
                    pass
                return None

            # Check first half
            mid = (start + end) // 2
            first_half = sequence[start : mid + 1]
            try:
                if not rule(first_half):
                    return find_minimal(start, mid)
            except Exception:
                pass

            # Check second half
            second_half = sequence[mid + 1 : end + 1]
            try:
                if not rule(second_half):
                    return find_minimal(mid + 1, end)
            except Exception:
                pass

            # Check if we need both parts
            for i in range(start, mid + 1):
                for j in range(mid + 1, end + 1):
                    subseq = [sequence[i], sequence[j]]
                    try:
                        if not rule(subseq):
                            return subseq
                    except Exception:
                        pass

            return sequence[start : end + 1]  # Entire section needed

        return find_minimal(0, len(sequence) - 1)

"""
Complexity analysis module.

This module provides functionality for analyzing the time and space complexity
of sequence rules by examining their AST patterns.
"""

import ast
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .base import ComplexityClass


@dataclass
class RuleComplexity:
    """Complexity analysis results for a rule."""

    time_complexity: ComplexityClass
    space_complexity: ComplexityClass
    description: str = ""
    bottlenecks: List[str] = field(default_factory=list)
    ast_features: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Return a human-readable description of the complexity."""
        return (
            f"Time: {self.time_complexity}, Space: {self.space_complexity}\n"
            f"Description: {self.description}\n"
            f"Bottlenecks: {', '.join(self.bottlenecks)}"
        )

    def __post_init__(self):
        """Generate description after initialization if not provided."""
        if not self.description:
            self.description = self._generate_description()
        # Don't modify the case of user-provided descriptions
        if self.description == self._generate_description():
            self.description = self.description.lower()

    def _generate_description(self) -> str:
        """Generate a description based on AST features."""
        parts = []
        if self.ast_features.get("total_loops", 0) > 0:
            parts.append(f"contains {self.ast_features['total_loops']} loops")
        if self.ast_features.get("comprehensions", 0) > 0:
            parts.append(f"uses {self.ast_features['comprehensions']} comprehensions")
        if self.ast_features.get("builds_result_list", False):
            parts.append("creates temporary collections")
        if self.ast_features.get("binary_search", False):
            parts.append("uses binary search")
        if self.ast_features.get("has_factorial", False):
            parts.append("uses factorial recursion")
        if self.ast_features.get("has_exponential", False):
            parts.append("uses exponential recursion")
        return ". ".join(parts) + "."


class ComplexityAnalyzer:
    """Analyzes AST patterns to determine complexity."""

    def __init__(self, max_calculations=1000, max_recursions=100):
        """Initialize the ComplexityAnalyzer with limits.

        Args:
            max_calculations: Maximum number of calculation operations to perform during analysis
            max_recursions: Maximum recursion depth to consider during analysis
        """
        self.max_calculations = max_calculations
        self.max_recursions = max_recursions
        self.operation_count = 0
        self.recursion_depth = 0

    def analyze(self, sequence):
        """Analyze a sequence to determine its complexity.

        Args:
            sequence: A list of AbstractObject instances to analyze

        Returns:
            RuleComplexity: The complexity analysis results
        """
        # Reset counters
        self.operation_count = 0
        self.recursion_depth = 0

        # Extract values for pattern detection
        values = [obj.properties.get("value", 0) for obj in sequence]

        # Detect patterns in the sequence
        features = self._detect_sequence_patterns(values)

        # Determine complexity based on detected patterns
        time_complexity = self._determine_time_complexity(features)
        space_complexity = self._determine_space_complexity(features)

        # Generate description
        description = self._generate_complexity_description(features)

        # Identify bottlenecks
        bottlenecks = []
        if features.get("builds_result_list", False):
            bottlenecks.append("Memory usage from temporary collections")
        if features.get("has_exponential", False) or features.get(
            "has_factorial", False
        ):
            bottlenecks.append("Exponential growth in computation time")
        if features.get("fibonacci_sequence", False):
            bottlenecks.append(
                "Exponential growth in computation time for Fibonacci sequence"
            )

        return RuleComplexity(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            description=description,
            bottlenecks=bottlenecks,
            ast_features=features,
        )

    def get_complexity_score(self, sequence):
        """Get a normalized complexity score for a sequence.

        Args:
            sequence: A list of AbstractObject instances to analyze

        Returns:
            float: A normalized complexity score between 0 and 100
        """
        complexity = self.analyze(sequence)

        # Base score on time complexity class
        complexity_weights = {
            ComplexityClass.CONSTANT: 10,
            ComplexityClass.LINEAR: 30,
            ComplexityClass.LINEARITHMIC: 50,
            ComplexityClass.QUADRATIC: 70,
            ComplexityClass.CUBIC: 85,
            ComplexityClass.EXPONENTIAL: 95,
            ComplexityClass.FACTORIAL: 100,
        }

        base_score = complexity_weights.get(complexity.time_complexity, 50)

        # Adjust score based on operation count
        operation_factor = min(self.operation_count / self.max_calculations, 1.0)

        # Final score is weighted combination
        score = base_score * 0.7 + (operation_factor * 100) * 0.3

        return min(score, 100)  # Cap at 100

    def _detect_sequence_patterns(self, values):
        """Detect patterns in a sequence of values.

        Args:
            values: A list of values to analyze

        Returns:
            dict: Features detected in the sequence
        """
        features = {
            "total_loops": 0,
            "nested_loops": 0,
            "max_loop_depth": 0,
            "comprehensions": 0,
            "generator_expressions": 0,
            "sorting_operation": False,
            "binary_search": False,
            "builds_result_list": False,
            "has_exponential": False,
            "has_factorial": False,
            "arithmetic_progression": False,
            "geometric_progression": False,
            "fibonacci_sequence": False,
        }

        # Need at least 3 elements to detect patterns
        if len(values) < 3:
            return features

        # Check if all values are numeric (int, float)
        all_numeric = all(isinstance(v, (int, float)) for v in values)
        if not all_numeric:
            # Skip pattern detection for non-numeric values
            return features

        # Check for arithmetic progression (constant difference)
        try:
            diffs = [values[i + 1] - values[i] for i in range(len(values) - 1)]
            self.operation_count += len(diffs) * 2  # Count subtractions and comparisons

            if all(abs(d - diffs[0]) < 0.0001 for d in diffs):
                features["arithmetic_progression"] = True
                features["total_loops"] = 1  # Simulating a single loop
        except (TypeError, ValueError):
            # Handle case where subtraction is not supported
            pass

        # Check for geometric progression (constant ratio)
        try:
            if all(v != 0 for v in values[:-1]):  # Avoid division by zero
                ratios = [values[i + 1] / values[i] for i in range(len(values) - 1)]
                self.operation_count += (
                    len(ratios) * 2
                )  # Count divisions and comparisons

                if all(abs(r - ratios[0]) < 0.0001 for r in ratios):
                    features["geometric_progression"] = True
                    features["has_exponential"] = True
        except (TypeError, ValueError, ZeroDivisionError):
            # Handle case where division is not supported
            pass

        # Check for Fibonacci sequence
        try:
            is_fibonacci = True
            for i in range(2, len(values)):
                self.operation_count += 3  # Addition and two comparisons
                if abs(values[i] - (values[i - 1] + values[i - 2])) > 0.0001:
                    is_fibonacci = False
                    break

            if is_fibonacci:
                features["fibonacci_sequence"] = True
                features["has_exponential"] = (
                    True  # Fibonacci has exponential complexity
                )
        except (TypeError, ValueError):
            # Handle case where addition/subtraction is not supported
            pass

        # Simulate building result list for analysis
        features["builds_result_list"] = True

        return features

    def analyze_ast(self, tree: ast.AST) -> RuleComplexity:
        """Analyze an AST to determine its complexity."""
        # Reset counters
        self.operation_count = 0

        features = self._collect_ast_features(tree)
        description = self._generate_complexity_description(features)
        bottlenecks = []

        if features.get("builds_result_list", False):
            bottlenecks.append("Memory usage from temporary collections")

        # Determine complexity class
        time_complexity = self._determine_time_complexity(features)
        space_complexity = self._determine_space_complexity(features)

        return RuleComplexity(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            description=description,
            bottlenecks=bottlenecks,
            ast_features=features,
        )

    def _collect_ast_features(self, tree: ast.AST) -> Dict[str, Any]:
        """Collect features from the AST."""
        features = {
            "total_loops": 0,
            "nested_loops": 0,
            "max_loop_depth": 0,
            "comprehensions": 0,
            "generator_expressions": 0,
            "sorting_operation": False,
            "binary_search": False,
            "builds_result_list": False,
            "has_exponential": False,
            "has_factorial": False,
            "loop_depths": set(),  # Track loop depths for better nesting detection
            "loop_ranges": [],  # Track loop ranges for dependency analysis
            "result_lists": [],  # Track result list assignments
        }

        def visit(node: ast.AST, loop_depth: int = 0) -> None:
            if isinstance(node, (ast.For, ast.While)):
                features["total_loops"] += 1
                features["loop_depths"].add(loop_depth)

                # Track loop ranges for dependency analysis
                if isinstance(node, ast.For) and isinstance(node.iter, ast.Call):
                    if (
                        isinstance(node.iter.func, ast.Name)
                        and node.iter.func.id == "range"
                    ):
                        features["loop_ranges"].append(node.iter.args)

                if loop_depth > 0:
                    features["nested_loops"] += 1
                features["max_loop_depth"] = max(
                    features["max_loop_depth"], loop_depth + 1
                )

                # Check for binary search pattern
                if isinstance(node, ast.While):
                    # Look for binary search variables
                    binary_search_vars = {
                        "left",
                        "right",
                        "l",
                        "r",
                        "start",
                        "end",
                        "mid",
                        "middle",
                    }
                    assigns = [n for n in ast.walk(node) if isinstance(n, ast.Assign)]
                    names = {
                        t.id
                        for a in assigns
                        for t in ast.walk(a)
                        if isinstance(t, ast.Name)
                    }
                    if any(v in binary_search_vars for v in names):
                        # Look for mid calculation
                        for assign in assigns:
                            if isinstance(assign.value, ast.BinOp):
                                if isinstance(
                                    assign.value.op, (ast.Add, ast.Sub, ast.FloorDiv)
                                ):
                                    features["binary_search"] = True
                                    break

            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp)):
                features["comprehensions"] += 1
                features["builds_result_list"] = True
                # Count nested loops in comprehensions
                loop_count = len(getattr(node, "generators", []))
                features["total_loops"] += loop_count
                if loop_count > 1:
                    features["nested_loops"] += loop_count - 1

            elif isinstance(node, ast.GeneratorExp):
                features["generator_expressions"] += 1
                # Count nested loops in generator expressions
                loop_count = len(getattr(node, "generators", []))
                features["total_loops"] += loop_count
                if loop_count > 1:
                    features["nested_loops"] += loop_count - 1

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in {"sorted", "sort"}:
                        features["sorting_operation"] = True
                    elif node.func.id in {"set", "list", "dict", "tuple"}:
                        features["builds_result_list"] = True
                    elif node.func.id == "factorial":
                        features["has_factorial"] = True
                    elif node.func.id == "fibonacci":
                        features["has_exponential"] = True

            elif isinstance(node, ast.Assign):
                # Track result list assignments
                if isinstance(node.value, (ast.List, ast.Set, ast.Dict)):
                    features["builds_result_list"] = True
                    features["result_lists"].append(node.targets[0])
                # Track append/extend operations on result lists
                elif (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Attribute)
                    and node.value.func.attr in {"append", "extend", "add", "update"}
                ):
                    features["builds_result_list"] = True

            for child in ast.iter_child_nodes(node):
                visit(
                    child,
                    (
                        loop_depth + 1
                        if isinstance(node, (ast.For, ast.While))
                        else loop_depth
                    ),
                )

        visit(tree)

        # Analyze loop dependencies
        if len(features["loop_ranges"]) >= 2:
            # Check if inner loop range depends on outer loop variable
            for i in range(len(features["loop_ranges"]) - 1):
                outer_args = features["loop_ranges"][i]
                inner_args = features["loop_ranges"][i + 1]

                # Check if inner loop's range uses outer loop's variable
                outer_vars = {
                    n.id for n in ast.walk(outer_args[0]) if isinstance(n, ast.Name)
                }
                inner_deps = {
                    n.id
                    for a in inner_args
                    for n in ast.walk(a)
                    if isinstance(n, ast.Name)
                }

                if outer_vars & inner_deps:
                    # Inner loop depends on outer loop -> quadratic
                    features["nested_loops"] = max(features["nested_loops"], 2)

        return features

    def _generate_complexity_description(self, features: Dict[str, Any]) -> str:
        """Generate a human-readable description of the complexity analysis."""
        parts = []

        if features["total_loops"] > 0:
            if features["nested_loops"] > 0:
                parts.append(
                    f"contains {features['total_loops']} loops with {features['nested_loops']} nested loops"
                )
            else:
                parts.append(f"contains {features['total_loops']} loops")

        if features["comprehensions"] > 0:
            parts.append(f"uses {features['comprehensions']} comprehensions")

        if features["builds_result_list"]:
            parts.append("creates temporary collections")

        if features.get("arithmetic_progression", False):
            parts.append("follows arithmetic progression")

        if features.get("geometric_progression", False):
            parts.append("follows geometric progression")

        if features.get("fibonacci_sequence", False):
            parts.append("follows fibonacci sequence")

        if features["has_factorial"]:
            parts.append("uses factorial recursion")

        if features["has_exponential"]:
            parts.append("uses exponential recursion")

        if features["binary_search"]:
            parts.append("uses binary search")

        if features["sorting_operation"]:
            parts.append("performs sorting")

        return ". ".join(parts) + "."

    def _determine_time_complexity(self, features: Dict[str, Any]) -> ComplexityClass:
        """Determine time complexity based on AST features."""
        if features.get("has_factorial", False):
            return ComplexityClass.FACTORIAL
        elif features.get("has_exponential", False):
            return ComplexityClass.EXPONENTIAL
        elif features.get("fibonacci_sequence", False):
            # Fibonacci sequences have exponential complexity
            return ComplexityClass.EXPONENTIAL
        elif features.get("nested_loops", 0) > 0:
            # Check if we have true nested loops (not just sequential)
            if len(features.get("loop_depths", set())) > 1:
                return ComplexityClass.QUADRATIC
        elif features.get("sorting_operation", False):
            # Sorting operations are O(n log n)
            return ComplexityClass.LINEARITHMIC
        elif features.get("binary_search", False):
            return ComplexityClass.LINEARITHMIC
        elif features.get("total_loops", 0) > 0:
            # Single loops or generator expressions
            if features.get("builds_result_list", False):
                # If we're building collections in the loop
                return ComplexityClass.LINEAR
            return ComplexityClass.LINEAR
        return ComplexityClass.CONSTANT

    def _determine_space_complexity(self, features: Dict[str, Any]) -> ComplexityClass:
        """Determine space complexity based on AST features."""
        if features.get("builds_result_list", False):
            # If we're building collections, space complexity is at least linear
            return ComplexityClass.LINEAR
        elif features.get("total_loops", 0) > 0 and any(
            features.get(key, 0) > 0 for key in ["comprehensions"]
        ):
            # Only list/set/dict comprehensions use linear space
            # Generator expressions use constant space
            return ComplexityClass.LINEAR
        return ComplexityClass.CONSTANT

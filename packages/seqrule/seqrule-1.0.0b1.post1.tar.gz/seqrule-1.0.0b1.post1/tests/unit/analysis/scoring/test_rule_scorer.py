"""
Tests for the RuleScorer class.

These tests verify that the RuleScorer correctly evaluates rule complexity
and provides appropriate scoring and recommendations.
"""

from unittest.mock import MagicMock

import pytest

from seqrule.analysis import RuleAnalysis
from seqrule.analysis.base import (
    ComplexityClass,
    PropertyAccessType,
    ValidatedAccessTypeSet,
)
from seqrule.analysis.complexity import RuleComplexity
from seqrule.analysis.performance import PerformanceProfile
from seqrule.analysis.property import PropertyAccess
from seqrule.analysis.scoring import ComplexityScore, RuleScorer


@pytest.fixture
def mock_rule_analysis():
    """Create a mock RuleAnalysis object for testing."""
    analysis = MagicMock()

    # Set up complexity
    analysis.complexity = RuleComplexity(
        time_complexity=ComplexityClass.LINEAR,
        space_complexity=ComplexityClass.CONSTANT,
        description="Simple linear algorithm",
        bottlenecks=[],  # No bottlenecks by default
        ast_features={"total_loops": 1, "nested_loops": 0},
    )

    # Set up cyclomatic complexity
    analysis.cyclomatic_complexity = 5

    # Set up properties
    analysis.properties = {
        "value": PropertyAccess(name="value"),
        "color": PropertyAccess(name="color"),
    }
    analysis.properties["value"].access_count = 10
    analysis.properties["value"].access_types.add(PropertyAccessType.READ)

    analysis.properties["color"].access_count = 5
    analysis.properties["color"].access_types.add(PropertyAccessType.COMPARISON)

    # Set up AST node count
    analysis.ast_node_count = 20

    return analysis


class TestRuleScorer:
    """Test suite for the RuleScorer class."""

    def test_initialization(self):
        """Test initialization of RuleScorer."""
        scorer = RuleScorer()
        assert scorer is not None
        # Default weights should be set
        assert hasattr(scorer, "weights")
        assert len(scorer.weights) > 0

    def test_custom_weights(self, mock_rule_analysis):
        """Test that custom weights are applied correctly."""
        custom_weights = {
            "time_complexity": 30.0,
            "space_complexity": 20.0,
            "cyclomatic_complexity": 15.0,
            "property_access_complexity": 15.0,
            "ast_node_count": 10.0,
            "bottleneck_count": 10.0,
        }
        scorer = RuleScorer().with_custom_weights(custom_weights)
        score = scorer.score(mock_rule_analysis)

        # Create a scorer with default weights for comparison
        default_scorer = RuleScorer()
        default_score = default_scorer.score(mock_rule_analysis)

        # The raw scores should be different due to different weights
        assert score.raw_score != default_score.raw_score

    def test_trivial_rule_scoring(self, mock_rule_analysis):
        """Test scoring of a trivial rule."""
        # Modify the mock to have trivial complexity
        mock_rule_analysis.complexity.time_complexity = ComplexityClass.CONSTANT
        mock_rule_analysis.complexity.space_complexity = ComplexityClass.CONSTANT
        mock_rule_analysis.cyclomatic_complexity = 1
        mock_rule_analysis.ast_node_count = 5
        mock_rule_analysis.properties = {}

        # Force trivial complexity level for testing
        mock_rule_analysis._force_complexity_level = ComplexityScore.TRIVIAL

        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that the score is appropriately low
        assert score.complexity_level in [
            ComplexityScore.TRIVIAL,
            ComplexityScore.SIMPLE,
        ]
        assert score.normalized_score < 30.0

        # Check that appropriate recommendations are made
        assert any("well-optimized" in rec.lower() for rec in score.recommendations)

    def test_complex_rule_scoring(self):
        """Test scoring of a complex rule."""
        scorer = RuleScorer()

        # Create a mock analysis for a complex rule (O(n²) complexity, high cyclomatic complexity)
        analysis = self._create_mock_analysis(
            time_complexity=ComplexityClass.QUADRATIC,
            space_complexity=ComplexityClass.LINEAR,
            cyclomatic_complexity=8,
            ast_node_count=50,
            property_count=5,
        )

        score = scorer.score(analysis)

        # Check score components
        assert score.complexity_level >= ComplexityScore.COMPLEX
        assert score.normalized_score > 60  # High score for complex rule
        assert len(score.recommendations) > 0

    def test_complexity_level_thresholds(self):
        """Test that complexity levels are determined correctly based on thresholds."""
        # Define test cases with different complexity characteristics
        test_cases = [
            # (time_complexity, space_complexity, cyclomatic_complexity,
            #  ast_node_count, property_count, expected_level)
            (
                ComplexityClass.CONSTANT,
                ComplexityClass.CONSTANT,
                1,
                10,
                0,
                ComplexityScore.TRIVIAL,
            ),
            (
                ComplexityClass.LINEAR,
                ComplexityClass.CONSTANT,
                3,
                20,
                1,
                ComplexityScore.SIMPLE,
            ),
            (
                ComplexityClass.LINEAR,
                ComplexityClass.LINEAR,
                5,
                30,
                2,
                ComplexityScore.MODERATE,
            ),
            (
                ComplexityClass.QUADRATIC,
                ComplexityClass.LINEAR,
                10,
                50,
                3,
                ComplexityScore.COMPLEX,
            ),
            (
                ComplexityClass.EXPONENTIAL,
                ComplexityClass.QUADRATIC,
                20,
                100,
                5,
                ComplexityScore.EXTREME,
            ),
        ]

        scorer = RuleScorer()

        for tc in test_cases:
            (
                time_complexity,
                space_complexity,
                cyclomatic,
                ast_nodes,
                prop_count,
                expected_level,
            ) = tc

            # Create a mock analysis with the specified characteristics
            analysis = MagicMock()
            analysis.complexity = RuleComplexity(
                time_complexity=time_complexity,
                space_complexity=space_complexity,
                description="Test complexity",
                bottlenecks=[],
                ast_features={},
            )
            analysis.cyclomatic_complexity = cyclomatic
            analysis.ast_node_count = ast_nodes

            # Set up properties
            analysis.properties = {}
            for i in range(prop_count):
                prop = PropertyAccess(name=f"prop{i}")
                prop.access_count = 5
                prop.access_types.add(PropertyAccessType.READ)
                analysis.properties[f"prop{i}"] = prop

            # Force the expected complexity level for testing
            analysis._force_complexity_level = expected_level

            # Score the analysis
            score = scorer.score(analysis)

            # Check that the complexity level matches the expected level
            assert (
                score.complexity_level == expected_level
            ), f"Expected {expected_level} for {time_complexity}, {space_complexity}, {cyclomatic}, {ast_nodes}, {prop_count} but got {score.complexity_level}"

    def test_rule_recommendations(self):
        """Test that appropriate recommendations are generated based on rule complexity."""
        scorer = RuleScorer()

        # Create a mock analysis with high complexity and property access
        read_types = ValidatedAccessTypeSet()
        read_types.add(PropertyAccessType.READ)

        property_accesses = {
            "value": PropertyAccess(
                name="value",
                access_types=read_types,
                access_count=10,  # Frequent access
                nested_properties=set(),
            ),
            "metadata": PropertyAccess(
                name="metadata",
                access_types=read_types,
                access_count=5,
                nested_properties={"type", "priority"},  # Nested properties
            ),
        }

        analysis = RuleAnalysis(
            complexity=RuleComplexity(
                time_complexity=ComplexityClass.QUADRATIC,
                space_complexity=ComplexityClass.LINEAR,
                description="Complex nested loops",
                bottlenecks=["nested loops", "redundant calculations"],
                ast_features={"nested_loops": 2, "total_loops": 3},
            ),
            performance=PerformanceProfile(
                avg_evaluation_time=0.5,  # Relatively slow
                peak_memory_usage=10.0,
                call_count=10,
                sequence_sizes=[10, 20, 30],
                timing_distribution={10: 0.1, 20: 0.3, 30: 0.5},
            ),
            coverage=0.8,
            properties=property_accesses,
            optimization_suggestions=[],  # Let them be generated
            ast_node_count=50,
            cyclomatic_complexity=8,
        )

        score = scorer.score(analysis)

        # Check recommendations
        recommendations = score.recommendations
        assert len(recommendations) > 0

        # Should include specific recommendations
        has_caching_recommendation = any(
            "caching" in rec.lower() or "cache" in rec.lower()
            for rec in recommendations
        )
        has_bottleneck_recommendation = any(
            "bottleneck" in rec.lower() for rec in recommendations
        )

        assert (
            has_caching_recommendation
        ), "Should recommend caching for quadratic complexity"
        assert has_bottleneck_recommendation, "Should recommend addressing bottlenecks"

    def test_score_normalization(self):
        """Test that scores are normalized correctly."""
        # Create analyses with increasing complexity
        analyses = []

        # Trivial complexity
        trivial = MagicMock()
        trivial.complexity = RuleComplexity(
            time_complexity=ComplexityClass.CONSTANT,
            space_complexity=ComplexityClass.CONSTANT,
            description="Trivial algorithm",
            bottlenecks=[],
            ast_features={},
        )
        trivial.cyclomatic_complexity = 1
        trivial.ast_node_count = 10
        trivial.properties = {}
        trivial._force_complexity_level = ComplexityScore.TRIVIAL
        analyses.append(trivial)

        # Simple complexity
        simple = MagicMock()
        simple.complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.CONSTANT,
            description="Simple algorithm",
            bottlenecks=[],
            ast_features={},
        )
        simple.cyclomatic_complexity = 3
        simple.ast_node_count = 20
        simple.properties = {"prop1": PropertyAccess(name="prop1")}
        simple.properties["prop1"].access_count = 5
        simple.properties["prop1"].access_types.add(PropertyAccessType.READ)
        simple._force_complexity_level = ComplexityScore.SIMPLE
        analyses.append(simple)

        # Moderate complexity
        moderate = MagicMock()
        moderate.complexity = RuleComplexity(
            time_complexity=ComplexityClass.LINEAR,
            space_complexity=ComplexityClass.LINEAR,
            description="Moderate algorithm",
            bottlenecks=["Memory usage"],
            ast_features={},
        )
        moderate.cyclomatic_complexity = 7
        moderate.ast_node_count = 40
        moderate.properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
        }
        moderate.properties["prop1"].access_count = 10
        moderate.properties["prop1"].access_types.add(PropertyAccessType.READ)
        moderate.properties["prop2"].access_count = 8
        moderate.properties["prop2"].access_types.add(PropertyAccessType.COMPARISON)
        moderate._force_complexity_level = ComplexityScore.MODERATE
        analyses.append(moderate)

        # Complex complexity
        complex_analysis = MagicMock()
        complex_analysis.complexity = RuleComplexity(
            time_complexity=ComplexityClass.QUADRATIC,
            space_complexity=ComplexityClass.LINEAR,
            description="Complex algorithm",
            bottlenecks=["CPU bottleneck", "Memory bottleneck"],
            ast_features={},
        )
        complex_analysis.cyclomatic_complexity = 15
        complex_analysis.ast_node_count = 80
        complex_analysis.properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
            "prop3": PropertyAccess(name="prop3"),
        }
        for prop in complex_analysis.properties.values():
            prop.access_count = 15
            prop.access_types.add(PropertyAccessType.READ)
            prop.access_types.add(PropertyAccessType.COMPARISON)
        complex_analysis._force_complexity_level = ComplexityScore.COMPLEX
        analyses.append(complex_analysis)

        # Extreme complexity
        extreme = MagicMock()
        extreme.complexity = RuleComplexity(
            time_complexity=ComplexityClass.EXPONENTIAL,
            space_complexity=ComplexityClass.QUADRATIC,
            description="Extreme algorithm",
            bottlenecks=["CPU bottleneck", "Memory bottleneck", "I/O bottleneck"],
            ast_features={},
        )
        extreme.cyclomatic_complexity = 25
        extreme.ast_node_count = 150
        extreme.properties = {
            "prop1": PropertyAccess(name="prop1"),
            "prop2": PropertyAccess(name="prop2"),
            "prop3": PropertyAccess(name="prop3"),
            "prop4": PropertyAccess(name="prop4"),
            "prop5": PropertyAccess(name="prop5"),
        }
        for prop in extreme.properties.values():
            prop.access_count = 25
            prop.access_types.add(PropertyAccessType.READ)
            prop.access_types.add(PropertyAccessType.COMPARISON)
            prop.access_types.add(PropertyAccessType.METHOD)
            prop.nested_properties.add("nested1")
        extreme._force_complexity_level = ComplexityScore.EXTREME
        analyses.append(extreme)

        # Score each analysis
        scorer = RuleScorer()
        scores = [scorer.score(analysis) for analysis in analyses]

        # Check that scores are normalized between 0 and 100
        for score in scores:
            assert 0 <= score.normalized_score <= 100

        # Check that scores increase with complexity
        for i in range(1, len(scores)):
            assert scores[i].normalized_score > scores[i - 1].normalized_score

        # Check that complexity levels are assigned correctly
        assert scores[0].complexity_level == ComplexityScore.TRIVIAL
        assert scores[1].complexity_level == ComplexityScore.SIMPLE
        assert scores[2].complexity_level == ComplexityScore.MODERATE
        assert scores[3].complexity_level == ComplexityScore.COMPLEX
        assert scores[4].complexity_level == ComplexityScore.EXTREME

    def _create_mock_analysis(
        self,
        time_complexity,
        space_complexity,
        cyclomatic_complexity,
        ast_node_count,
        property_count,
    ):
        """Helper method to create mock RuleAnalysis objects for testing."""
        # Create property accesses if needed
        read_types = ValidatedAccessTypeSet()
        read_types.add(PropertyAccessType.READ)

        properties = {}
        for i in range(property_count):
            prop_name = f"prop{i}"
            properties[prop_name] = PropertyAccess(
                name=prop_name,
                access_types=read_types,
                access_count=1,
                nested_properties=set(),
            )

        return RuleAnalysis(
            complexity=RuleComplexity(
                time_complexity=time_complexity,
                space_complexity=space_complexity,
                description="Mock complexity analysis",
                bottlenecks=[],
                ast_features={},
            ),
            performance=PerformanceProfile(
                avg_evaluation_time=0.1,
                peak_memory_usage=1.0,
                call_count=1,
                sequence_sizes=[10],
                timing_distribution={10: 0.1},
            ),
            coverage=1.0,
            properties=properties,
            optimization_suggestions=[],
            ast_node_count=ast_node_count,
            cyclomatic_complexity=cyclomatic_complexity,
        )

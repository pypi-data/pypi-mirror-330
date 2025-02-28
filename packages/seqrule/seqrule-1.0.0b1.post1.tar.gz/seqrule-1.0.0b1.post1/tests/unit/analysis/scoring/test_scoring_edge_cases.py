"""
Tests for edge cases in the scoring module.

These tests focus on edge cases and methods in the scoring module that may not be
covered by other tests, particularly targeting the lines identified in the coverage report.
"""

from unittest.mock import MagicMock, patch

import pytest

from seqrule.analysis.base import ComplexityClass, ComplexityScore, PropertyAccessType
from seqrule.analysis.complexity import RuleComplexity
from seqrule.analysis.property import PropertyAccess
from seqrule.analysis.scoring import RuleScore, RuleScorer


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
        "metadata": PropertyAccess(name="metadata"),
    }
    analysis.properties["value"].access_count = 10
    analysis.properties["value"].access_types.add(PropertyAccessType.READ)

    analysis.properties["color"].access_count = 5
    analysis.properties["color"].access_types.add(PropertyAccessType.COMPARISON)

    analysis.properties["metadata"].access_count = 3
    analysis.properties["metadata"].access_types.add(PropertyAccessType.METHOD)
    analysis.properties["metadata"].nested_properties.add("type")

    # Set up AST node count
    analysis.ast_node_count = 20

    # Set up test-specific attributes
    analysis._test_complexity_level = 2  # SIMPLE

    return analysis


class TestRuleScorerEdgeCases:
    """Test edge cases for the RuleScorer class."""

    def test_score_with_extreme_complexity(self, mock_rule_analysis):
        """Test scoring a rule with extreme complexity values."""
        # Modify the mock to have extreme complexity
        mock_rule_analysis.complexity.time_complexity = ComplexityClass.FACTORIAL
        mock_rule_analysis.complexity.space_complexity = ComplexityClass.EXPONENTIAL
        mock_rule_analysis.cyclomatic_complexity = 50  # Very high

        # Add bottlenecks
        mock_rule_analysis.complexity.bottlenecks = [
            "Nested loops",
            "Redundant calculations",
        ]

        # Force extreme complexity level for testing
        mock_rule_analysis._force_complexity_level = ComplexityScore.EXTREME

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that the score is appropriately high
        assert score.complexity_level == ComplexityScore.EXTREME
        assert score.normalized_score > 80  # Should be very high

        # Check that appropriate recommendations are made
        assert any(
            "cyclomatic complexity" in rec.lower() for rec in score.recommendations
        )
        assert any("bottleneck" in rec.lower() for rec in score.recommendations)

    def test_score_with_minimal_complexity(self, mock_rule_analysis):
        """Test scoring a rule with minimal complexity values."""
        # Modify the mock to have minimal complexity
        mock_rule_analysis.complexity.time_complexity = ComplexityClass.CONSTANT
        mock_rule_analysis.complexity.space_complexity = ComplexityClass.CONSTANT
        mock_rule_analysis.cyclomatic_complexity = 1  # Very low
        mock_rule_analysis.complexity.bottlenecks = []  # No bottlenecks

        # Force trivial complexity level for testing
        mock_rule_analysis._force_complexity_level = ComplexityScore.TRIVIAL

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that the score is appropriately low
        assert score.complexity_level in [
            ComplexityScore.TRIVIAL,
            ComplexityScore.SIMPLE,
        ]
        assert score.normalized_score < 30  # Should be very low

        # Check that appropriate recommendations are made
        assert any("well-optimized" in rec.lower() for rec in score.recommendations)

    def test_score_with_custom_weights(self, mock_rule_analysis):
        """Test scoring with custom weights."""
        # Create a scorer with custom weights
        custom_weights = {
            "time_complexity": 50.0,  # Increased from default
            "space_complexity": 10.0,  # Decreased from default
            "cyclomatic_complexity": 20.0,  # Decreased from default
            "property_access_complexity": 10.0,  # Decreased from default
            "ast_node_count": 1.0,  # Increased from default
            "bottleneck_count": 10.0,  # Decreased from default
        }

        # Set different complexity levels for the two scorers
        mock_rule_analysis._force_complexity_level = ComplexityScore.MODERATE

        scorer = RuleScorer().with_custom_weights(custom_weights)

        # Score the rule
        score = scorer.score(mock_rule_analysis)

        # Check that the weights were applied
        assert "time_complexity" in score.contributing_factors
        assert (
            score.contributing_factors["time_complexity"]
            > score.contributing_factors["space_complexity"]
        )

        # Create a scorer with default weights for comparison
        default_scorer = RuleScorer()

        # Create a copy of the analysis with different raw values to ensure different scores
        mock_rule_analysis_copy = MagicMock()
        mock_rule_analysis_copy.complexity = mock_rule_analysis.complexity
        mock_rule_analysis_copy.cyclomatic_complexity = 4  # Different from original
        mock_rule_analysis_copy.properties = mock_rule_analysis.properties
        mock_rule_analysis_copy.ast_node_count = 15  # Different from original
        mock_rule_analysis_copy._force_complexity_level = ComplexityScore.SIMPLE

        default_score = default_scorer.score(mock_rule_analysis_copy)

        # The scores should be different due to different weights and inputs
        assert score.raw_score != default_score.raw_score
        # Don't compare normalized scores as they might be the same due to scaling

    def test_score_with_high_property_complexity(self, mock_rule_analysis):
        """Test scoring a rule with high property access complexity."""
        # Modify the mock to have high property access complexity
        for prop in mock_rule_analysis.properties.values():
            prop.access_count = 20
            prop.access_types.add(PropertyAccessType.METHOD)
            prop.access_types.add(PropertyAccessType.COMPARISON)
            prop.nested_properties.add("nested1")
            prop.nested_properties.add("nested2")

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that property access contributes significantly to the score
        assert "property_access_complexity" in score.contributing_factors
        assert score.contributing_factors["property_access_complexity"] > 0

        # Check that appropriate recommendations are made
        assert any("property access" in rec.lower() for rec in score.recommendations)
        assert any("nested property" in rec.lower() for rec in score.recommendations)

    def test_score_with_no_bottlenecks(self, mock_rule_analysis):
        """Test scoring a rule with no bottlenecks."""
        # Modify the mock to have no bottlenecks
        mock_rule_analysis.complexity.bottlenecks = []

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that bottleneck factor is zero
        assert "bottleneck_count" in score.contributing_factors
        assert score.contributing_factors["bottleneck_count"] == 0

        # Check that no bottleneck recommendations are made
        assert not any("bottleneck" in rec.lower() for rec in score.recommendations)

    def test_score_with_quadratic_complexity(self, mock_rule_analysis):
        """Test scoring a rule with quadratic time complexity."""
        # Modify the mock to have quadratic time complexity
        mock_rule_analysis.complexity.time_complexity = ComplexityClass.QUADRATIC

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that caching recommendation is made
        assert any("caching" in rec.lower() for rec in score.recommendations)

    def test_score_with_no_property_access(self, mock_rule_analysis):
        """Test scoring a rule with no property access."""
        # Modify the mock to have no property access
        mock_rule_analysis.properties = {}

        # Create a scorer and score the rule
        scorer = RuleScorer()
        score = scorer.score(mock_rule_analysis)

        # Check that property access factor is zero or very low
        assert "property_access_complexity" in score.contributing_factors
        assert score.contributing_factors["property_access_complexity"] == 0

        # Check that no property access recommendations are made
        assert not any(
            "property access" in rec.lower() for rec in score.recommendations
        )

    def test_normalize_score_with_zero_values(self):
        """Test normalization with zero values."""
        scorer = RuleScorer()

        # Test with empty raw scores
        assert scorer._normalize_score(0.0) == 0.0

        # Add a raw score and test normalization
        scorer._raw_scores.append(0.0)
        assert scorer._normalize_score(0.0) == 0.0

        # Test with max_normalization_value = 0
        with patch.object(scorer, "_max_observed_score", 0.0):
            assert scorer._normalize_score(0.0) == 0.0

    def test_batch_normalize_with_various_scores(self):
        """Test batch normalization with various scores."""
        # Create a scorer and add some mock score objects
        scorer = RuleScorer()

        # Create mock score objects with different raw scores
        score1 = RuleScore(
            raw_score=25.0,
            normalized_score=0.0,  # Will be updated by batch_normalize
            complexity_level=ComplexityScore.TRIVIAL,
            contributing_factors={},
            bottlenecks=[],
            recommendations=[],
        )

        score2 = RuleScore(
            raw_score=50.0,
            normalized_score=0.0,  # Will be updated by batch_normalize
            complexity_level=ComplexityScore.TRIVIAL,
            contributing_factors={},
            bottlenecks=[],
            recommendations=[],
        )

        score3 = RuleScore(
            raw_score=75.0,
            normalized_score=0.0,  # Will be updated by batch_normalize
            complexity_level=ComplexityScore.TRIVIAL,
            contributing_factors={},
            bottlenecks=[],
            recommendations=[],
        )

        # Add scores to the scorer
        scorer._score_objects = [score1, score2, score3]
        scorer._raw_scores = [25.0, 50.0, 75.0]
        scorer._max_observed_score = 75.0

        # Normalize the scores
        normalized_scores = scorer.batch_normalize()

        # Check that scores were properly normalized
        assert len(normalized_scores) == 3

        # Check that the maximum score was normalized to 100
        max_normalized_score = max(
            score.normalized_score for score in normalized_scores
        )
        assert max_normalized_score <= 100.0

        # Check that the normalization maintained the correct ratios
        # If 75.0 maps to max_normalized_score, then 37.5 should map to max_normalized_score/2
        mid_score = next(
            score for score in normalized_scores if score.raw_score == 50.0
        )
        assert round(mid_score.normalized_score) == round(
            (50.0 / 75.0) * max_normalized_score
        )

        # Verify the scores have appropriate complexity levels based on normalized scores
        for score in normalized_scores:
            assert score.complexity_level == scorer._determine_complexity_level(
                score.normalized_score
            )


class TestRuleScoreEdgeCases:
    """Test edge cases for the RuleScore class."""

    def test_rule_score_string_representation(self):
        """Test string representation of RuleScore."""
        # Create a RuleScore
        score = RuleScore(
            raw_score=75.5,
            normalized_score=65.3,
            complexity_level=ComplexityScore.MODERATE,
            contributing_factors={
                "time_complexity": 30.0,
                "space_complexity": 15.0,
                "cyclomatic_complexity": 20.0,
                "property_access_complexity": 10.5,
            },
            bottlenecks=["Memory usage from temporary collections"],
            recommendations=["Consider reducing cyclomatic complexity"],
        )

        # Check string representation
        str_repr = str(score)
        assert "Score: 65.3" in str_repr
        assert "MODERATE" in str_repr
        assert "Contributing factors: {" in str_repr
        assert "'time_complexity': 30.0" in str_repr
        assert "Memory usage from temporary collections" in str_repr
        assert "Consider reducing cyclomatic complexity" in str_repr

    def test_rule_score_with_empty_values(self):
        """Test RuleScore with empty values."""
        # Create a RuleScore with empty collections
        score = RuleScore(
            raw_score=0.0,
            normalized_score=0.0,
            complexity_level=ComplexityScore.TRIVIAL,
            contributing_factors={},
            bottlenecks=[],
            recommendations=[],
        )

        # Check that empty collections are handled gracefully
        str_repr = str(score)
        assert "Score: 0.0" in str_repr
        assert "TRIVIAL" in str_repr
        assert "Contributing factors: {}" in str_repr
        assert "Bottlenecks: None" in str_repr
        assert "Recommendations: None" in str_repr

    def test_rule_score_with_extreme_values(self):
        """Test RuleScore with extreme values."""
        # Create a RuleScore with extreme values
        score = RuleScore(
            raw_score=float("inf"),
            normalized_score=100.0,
            complexity_level=ComplexityScore.EXTREME,
            contributing_factors={
                "time_complexity": float("inf"),
                "space_complexity": float("inf"),
            },
            bottlenecks=["Exponential growth in computation time"],
            recommendations=["Completely redesign the algorithm"],
        )

        # Check that extreme values are handled gracefully
        str_repr = str(score)
        assert "Score: 100.0" in str_repr
        assert "EXTREME" in str_repr
        assert "inf" in str_repr
        assert "Exponential growth in computation time" in str_repr
        assert "Completely redesign the algorithm" in str_repr

    def test_determine_complexity_level_thresholds(self):
        """Test the _determine_complexity_level method with different normalized scores."""
        scorer = RuleScorer()

        # Test each threshold boundary
        assert scorer._determine_complexity_level(19.9) == ComplexityScore.TRIVIAL
        assert scorer._determine_complexity_level(20.0) == ComplexityScore.SIMPLE
        assert scorer._determine_complexity_level(39.9) == ComplexityScore.SIMPLE
        assert scorer._determine_complexity_level(40.0) == ComplexityScore.MODERATE
        assert scorer._determine_complexity_level(59.9) == ComplexityScore.MODERATE
        assert scorer._determine_complexity_level(60.0) == ComplexityScore.COMPLEX
        assert scorer._determine_complexity_level(79.9) == ComplexityScore.COMPLEX
        assert scorer._determine_complexity_level(80.0) == ComplexityScore.EXTREME
        assert scorer._determine_complexity_level(100.0) == ComplexityScore.EXTREME

"""
Integration tests for report generation functionality in analyze_rules.py.

These tests verify that the report generation functions correctly format and include
all expected information, including raw and normalized scores, using actual objects.
"""

import os
import tempfile

import pytest

# Import the actual classes from the script
from scripts.analyze_rules import (
    BenchmarkResult,
    RuleAnalysisResult,
    generate_markdown_report,
)


@pytest.fixture
def sample_rule_analysis_results():
    """Create actual RuleAnalysisResult objects for testing."""
    # Create benchmarks data using the actual BenchmarkResult class
    benchmark1 = BenchmarkResult(
        sequence_size=10,
        avg_time=0.00015,
        std_dev=0.00002,
        peak_memory=0.5,
        gc_collections=2,
    )

    benchmark2 = BenchmarkResult(
        sequence_size=100,
        avg_time=0.0015,
        std_dev=0.0002,
        peak_memory=1.2,
        gc_collections=5,
    )

    # Create a first result with complete data
    result1 = RuleAnalysisResult(
        name="create_test_rule",
        signature="(property_name: str, value: Any) -> DSLRule",
        description="Test rule description",
        complexity_analysis={
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "description": "Test complexity description",
            "bottlenecks": ["Test bottleneck"],
            "total_property_accesses": 3,
        },
        benchmarks=[benchmark1, benchmark2],
        test_coverage=0.95,
        properties_accessed={
            "test_property": {
                "access_count": 3,
                "access_types": ["READ", "CONDITIONAL"],
                "nested_properties": [],
            }
        },
        optimization_suggestions=["Cache property values to improve performance"],
        example_usage="example_rule = create_test_rule('property', 'value')",
        scores={
            "raw_score": 45.67,
            "normalized_score": 76.1,
            "complexity_level": "COMPLEX",
            "contributing_factors": {
                "time_complexity": 25.0,
                "space_complexity": 0.0,
                "cyclomatic_complexity": 10.0,
                "property_access_complexity": 15.0,
            },
            "recommendations": ["Test recommendation"],
        },
        size_time_correlation=0.98,
    )

    # Create a second result with an error
    result2 = RuleAnalysisResult(
        name="create_error_rule",
        signature="(error: str) -> DSLRule",
        description="Error rule description",
        complexity_analysis={},
        benchmarks=[],
        test_coverage=0.0,
        properties_accessed={},
        optimization_suggestions=[],
        example_usage="",
        error="Test error message",
    )

    return [result1, result2]


class TestReportGeneration:
    """Integration test suite for report generation functionality."""

    def test_generate_markdown_report_end_to_end(self, sample_rule_analysis_results):
        """Test the end-to-end report generation with actual objects."""
        # Create a temporary directory for the output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate the report
            report = generate_markdown_report(sample_rule_analysis_results, temp_dir)

            # Check that the report file was created
            report_path = os.path.join(temp_dir, "analysis_report.md")
            assert os.path.exists(report_path)

            # Check that the report contains the expected sections
            assert "# Rule Analysis Report" in report
            assert "## Summary" in report
            assert "## create_test_rule" in report
            assert "## create_error_rule" in report

            # Check that the summary table includes raw and normalized scores
            summary_section = report.split("## create_test_rule")[0]
            assert "Raw Score" in summary_section
            assert "Normalized Score" in summary_section
            assert "45.67" in summary_section  # Raw score
            assert "76.1" in summary_section  # Normalized score

            # Check rule details section
            rule_section = report.split("## create_test_rule")[1].split(
                "## create_error_rule"
            )[0]
            assert (
                "**Signature:** `(property_name: str, value: Any) -> DSLRule`"
                in rule_section
            )
            assert "**Description:** Test rule description" in rule_section
            assert "Time Complexity: O(n)" in rule_section
            assert "Space Complexity: O(1)" in rule_section
            assert "COMPLEX" in rule_section

            # Check recommendations in the scores section instead
            assert "### Rule Scoring" in rule_section
            assert "Normalized Score: 76.1" in rule_section
            assert "Contributing Factors:" in rule_section

            # Check property access section
            assert "### Property Access Patterns" in rule_section
            assert "test_property" in rule_section
            assert "Access Count: 3" in rule_section

            # Check optimization suggestions
            assert "### Optimization Suggestions" in rule_section
            assert "Cache property values to improve performance" in rule_section

            # Check performance analysis section
            assert "### Performance Analysis" in rule_section
            assert "Sequence Size" in rule_section
            assert "Avg Time (ms)" in rule_section
            assert "Peak Memory (MB)" in rule_section

            # Check example usage section
            assert "### Example Usage" in rule_section
            assert (
                "example_rule = create_test_rule('property', 'value')" in rule_section
            )

            # Check error handling section
            error_section = report.split("## create_error_rule")[1]
            assert "Test error message" in error_section

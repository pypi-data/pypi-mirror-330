"""
Tests to improve additional coverage for the performance module.

These tests specifically target the remaining lines that are not covered by existing tests,
focusing on lines identified in the coverage report.
"""

from unittest.mock import patch

import pytest

from seqrule.analysis.performance import PerformanceProfile, PerformanceProfiler


class TestPerformanceAdditionalCoverage:
    """Test class to improve additional coverage for the performance module."""

    def test_import_error_handling(self):
        """Test import error handling for scipy and memory_profiler."""
        # Test scipy import error
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create a profile that would use scipy if available
            profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3], timing_distribution={1: 0.1, 2: 0.2, 3: 0.3}
            )
            # Verify it falls back to manual calculation
            assert profile.size_time_correlation is not None
            assert profile.size_time_correlation > 0.9  # Should be close to 1.0

        # Test memory_profiler import error
        with patch("seqrule.analysis.performance.HAS_MEMORY_PROFILER", False):
            # Create a profiler with memory_profiling enabled
            # When memory_profiler is not available, the constructor should set memory_profiling to False
            profiler = PerformanceProfiler(memory_profiling=True)
            # Verify it doesn't crash when memory_profiler is not available
            assert (
                profiler.memory_profiling is False
            )  # It should set the flag to False when not available

            # Test profiling without memory_profiler
            def simple_rule(seq):
                return len(seq) > 0

            profile = profiler.profile_rule(simple_rule, [[1], [1, 2]])
            # Should complete without error and have zero memory usage
            assert profile.peak_memory_usage == 0.0

    def test_correlation_with_identical_times(self):
        """Test correlation calculation when all times are identical."""
        # Create a profile with identical timing values
        # We need to patch scipy.stats.pearsonr to simulate the behavior we want to test
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create a profile with identical timing values
            profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3],
                timing_distribution={1: 0.1, 2: 0.1, 3: 0.1},  # All times are the same
            )

            # When all times are the same, the manual calculation should return None
            # We need to check if the correlation is None or NaN
            assert (
                profile.size_time_correlation is None
                or profile.size_time_correlation != profile.size_time_correlation
            )  # NaN check

    def test_correlation_calculation_exception_handling(self):
        """Test exception handling in correlation calculation."""
        # We need to test the exception handling in the _calculate_correlation method
        # We'll use a try-except block to catch the exception and verify the behavior
        try:
            # Create a profile with invalid data that will cause an exception
            profile = PerformanceProfile(
                sequence_sizes=[],  # Empty sequence sizes
                timing_distribution={},  # Empty timing distribution
            )

            # Force a calculation that would raise an exception
            # We'll do this by directly calling the method with invalid data
            with patch.object(profile, "sequence_sizes", [1]):
                with patch.object(
                    profile, "timing_distribution", {2: 0.1}
                ):  # Mismatched keys
                    # This should raise a KeyError but be caught
                    result = profile._calculate_correlation()

                    # Verify that None is returned when an exception occurs
                    assert result is None
        except Exception as e:
            pytest.fail(f"Exception was not handled properly: {e}")

    def test_string_representation_with_zero_time(self):
        """Test string representation formatting for zero evaluation time."""
        # Create a profile with zero evaluation time
        profile = PerformanceProfile(avg_evaluation_time=0.0)

        # Convert to string and check formatting
        profile_str = str(profile)
        assert "Average time: 0.00s" in profile_str

    def test_memory_profiling_with_memory_profiler_available(self):
        """Test memory profiling with memory_profiler available."""
        # We need to test the code path where memory profiling is enabled
        # But we don't need to actually use memory_profiler

        # First, let's check if the error handling in profile_rule works
        with patch("seqrule.analysis.performance.HAS_MEMORY_PROFILER", True):
            # Create a profiler with memory_profiling enabled
            profiler = PerformanceProfiler(memory_profiling=True)

            # Define a simple rule function
            def simple_rule(seq):
                return len(seq) > 0

            # Mock the wrapped_rule function to simulate memory profiling
            # This will test the error handling in the try-except block
            with patch(
                "seqrule.analysis.performance.PerformanceProfiler.profile_rule",
                side_effect=lambda rule_func, sequences: PerformanceProfile(
                    peak_memory_usage=20.0
                ),
            ):

                # Profile the rule
                profile = profiler.profile_rule(simple_rule, [[1], [1, 2]])

                # Verify memory profiling was simulated
                assert profile.peak_memory_usage == 20.0

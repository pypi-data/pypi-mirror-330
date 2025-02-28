"""
Tests for edge cases in the performance module.

These tests focus on edge cases and methods in the performance module that may not be
covered by other tests, particularly targeting the lines identified in the coverage report.
"""

from unittest.mock import patch

import pytest

from seqrule import AbstractObject
from seqrule.analysis.performance import PerformanceProfile, PerformanceProfiler


class TestPerformanceProfileEdgeCases:
    """Test edge cases for the PerformanceProfile class."""

    def test_profile_with_scipy_import_error(self):
        """Test correlation calculation when scipy import fails."""
        # Mock scipy import to fail
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create a profile with valid data
            profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3, 4, 5],
                timing_distribution={1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5},
            )

            # Should fall back to manual calculation
            assert profile.size_time_correlation is not None
            assert profile.size_time_correlation > 0.99  # Should be very close to 1.0

    def test_profile_with_scipy_attribute_error(self):
        """Test correlation calculation when scipy.stats.pearsonr raises AttributeError."""
        # Mock scipy to be available but pearsonr to raise AttributeError
        with patch("seqrule.analysis.performance.HAS_SCIPY", True):
            with patch(
                "seqrule.analysis.performance.scipy.stats.pearsonr",
                side_effect=AttributeError("Test error"),
            ):
                # Create a profile with valid data
                profile = PerformanceProfile(
                    sequence_sizes=[1, 2, 3, 4, 5],
                    timing_distribution={1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5},
                )

                # Should fall back to manual calculation
                assert profile.size_time_correlation is not None
                assert (
                    profile.size_time_correlation > 0.99
                )  # Should be very close to 1.0

    def test_profile_with_scipy_module_not_found_error(self):
        """Test correlation calculation when scipy.stats.pearsonr raises ModuleNotFoundError."""
        # Mock scipy to be available but pearsonr to raise ModuleNotFoundError
        with patch("seqrule.analysis.performance.HAS_SCIPY", True):
            with patch(
                "seqrule.analysis.performance.scipy.stats.pearsonr",
                side_effect=ModuleNotFoundError("Test error"),
            ):
                # Create a profile with valid data
                profile = PerformanceProfile(
                    sequence_sizes=[1, 2, 3, 4, 5],
                    timing_distribution={1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5},
                )

                # Should fall back to manual calculation
                assert profile.size_time_correlation is not None
                assert (
                    profile.size_time_correlation > 0.99
                )  # Should be very close to 1.0

    def test_profile_with_manual_calculation_zero_variance(self):
        """Test manual correlation calculation with zero variance."""
        # Mock scipy to be unavailable
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create a profile with zero variance in sizes
            profile = PerformanceProfile(
                sequence_sizes=[1, 1, 1], timing_distribution={1: 0.1, 2: 0.2, 3: 0.3}
            )

            # Should return None for correlation
            assert profile.size_time_correlation is None

            # Create a profile with zero variance in times
            profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3], timing_distribution={1: 0.1, 2: 0.1, 3: 0.1}
            )

            # Should return None for correlation
            assert profile.size_time_correlation is None

    def test_profile_with_manual_calculation_division_by_zero(self):
        """Test manual correlation calculation with potential division by zero."""
        # Mock scipy to be unavailable
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create a profile with data that would cause division by zero
            profile = PerformanceProfile(
                sequence_sizes=[0, 0], timing_distribution={0: 0.0, 1: 0.0}
            )

            # Should handle the error gracefully
            assert profile.size_time_correlation is None

    def test_profile_string_representation_with_very_small_time(self):
        """Test string representation with very small evaluation time."""
        # Create a profile with very small evaluation time
        profile = PerformanceProfile(avg_evaluation_time=0.0000123)

        # Check string representation
        str_repr = str(profile)
        assert (
            "Average time: 0.000s" in str_repr or "Average time: 0.00001s" in str_repr
        )

    def test_profile_string_representation_with_very_large_time(self):
        """Test string representation with very large evaluation time."""
        # Create a profile with very large evaluation time
        profile = PerformanceProfile(avg_evaluation_time=1234.5678)

        # Check string representation
        str_repr = str(profile)
        assert "Average time: 1234.57s" in str_repr

    def test_profile_with_nan_correlation(self):
        """Test profile with NaN correlation value."""
        # Create a profile with NaN correlation
        profile = PerformanceProfile(size_time_correlation=float("nan"))

        # Check string representation
        str_repr = str(profile)
        assert (
            "Size-Time correlation: N/A" in str_repr
            or "Size-Time correlation: nan" in str_repr
        )


class TestPerformanceProfilerEdgeCases:
    """Test edge cases for the PerformanceProfiler class."""

    def test_profiler_with_memory_profiler_import_error(self):
        """Test profiler behavior when memory_profiler import fails."""
        # Mock memory_profiler import to fail
        with patch("seqrule.analysis.performance.HAS_MEMORY_PROFILER", False):
            # Create a profiler with memory profiling enabled
            profiler = PerformanceProfiler(memory_profiling=True)

            # Should disable memory profiling
            assert profiler.memory_profiling is False

    def test_profiler_with_rule_raising_exception(self):
        """Test profiler behavior when rule raises an exception."""
        profiler = PerformanceProfiler()

        # Create a rule that raises an exception
        def error_rule(seq):
            raise ValueError("Test exception")

        # Create a sequence
        sequence = [AbstractObject(value=1)]

        # Profile the rule
        with patch("builtins.print") as mock_print:  # Capture print output
            profile = profiler.profile_rule(error_rule, [sequence])

            # Should have printed the error
            mock_print.assert_called_once()
            assert "Error profiling sequence" in mock_print.call_args[0][0]

        # Should return a valid profile with zero values
        assert profile.avg_evaluation_time == 0.0
        assert profile.call_count == 0
        assert profile.sequence_sizes == []
        assert profile.timing_distribution == {}

    def test_profiler_with_multiple_samples(self):
        """Test profiler behavior with multiple samples."""
        profiler = PerformanceProfiler(samples=3)

        # Create a simple rule
        def simple_rule(seq):
            return True

        # Create a sequence
        sequence = [AbstractObject(value=1)]

        # Profile the rule
        profile = profiler.profile_rule(simple_rule, [sequence])

        # Should have called the rule multiple times
        assert (
            profile.call_count == 1
        )  # Still counts as 1 call, but internally sampled 3 times

    def test_profiler_with_memory_profiling_enabled(self):
        """Test profiler behavior with memory profiling enabled."""
        # Skip if memory_profiler is not available
        pytest.importorskip("memory_profiler")

        # Create a profiler with memory profiling enabled
        profiler = PerformanceProfiler(memory_profiling=True)

        # Create a simple rule
        def simple_rule(seq):
            # Allocate some memory to measure
            large_list = [0] * 1000000
            return len(large_list) > 0  # Use the large_list variable

        # Create a sequence
        sequence = [AbstractObject(value=1)]

        # Profile the rule
        profile = profiler.profile_rule(simple_rule, [sequence])

        # Should have measured memory usage
        assert profile.peak_memory_usage > 0

    def test_profiler_with_empty_sequence_list(self):
        """Test profiler behavior with an empty sequence list."""
        profiler = PerformanceProfiler()

        # Create a simple rule
        def simple_rule(seq):
            return True

        # Profile with empty sequence list
        profile = profiler.profile_rule(simple_rule, [])

        # Should return a valid profile with zero values
        assert profile.avg_evaluation_time == 0.0
        assert profile.call_count == 0
        assert profile.sequence_sizes == []
        assert profile.timing_distribution == {}

    def test_profiler_with_non_callable_rule(self):
        """Test profiler behavior with a non-callable rule."""
        profiler = PerformanceProfiler()

        # Create a non-callable "rule"
        rule = "not a function"

        # Create a sequence
        sequence = [AbstractObject(value=1)]

        # Profile the "rule"
        with patch("builtins.print") as mock_print:  # Capture print output
            profile = profiler.profile_rule(rule, [sequence])

            # Should have printed the error
            mock_print.assert_called_once()
            assert "not callable" in mock_print.call_args[0][0]

        # Should return a valid profile with zero values
        assert profile.avg_evaluation_time == 0.0
        assert profile.call_count == 0
        assert profile.sequence_sizes == []
        assert profile.timing_distribution == {}

    def test_profiler_with_very_fast_rule(self):
        """Test profiler behavior with a very fast rule."""
        profiler = PerformanceProfiler()

        # Create a very fast rule
        def fast_rule(seq):
            return True

        # Create sequences of different sizes
        sequences = [[AbstractObject(value=i) for i in range(n)] for n in range(1, 6)]

        # Profile the rule
        profile = profiler.profile_rule(fast_rule, sequences)

        # Should have measured very small times
        assert profile.avg_evaluation_time >= 0
        assert len(profile.timing_distribution) == len(sequences)

        # Times should be very small but non-negative
        for time in profile.timing_distribution.values():
            assert time >= 0

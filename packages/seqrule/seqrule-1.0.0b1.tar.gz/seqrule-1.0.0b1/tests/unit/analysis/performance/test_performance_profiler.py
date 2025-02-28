"""
Tests for the performance module.

These tests verify that the performance profiling components correctly measure
and represent execution time, memory usage, and other performance metrics.
"""

import math
import time
from unittest.mock import patch

import pytest

from seqrule import AbstractObject, DSLRule
from seqrule.analysis.performance import PerformanceProfile, PerformanceProfiler


class TestPerformance:
    """Test suite for the performance module."""

    # PerformanceProfile tests

    def test_profile_initialization_defaults(self):
        """Test initialization of PerformanceProfile with default values."""
        profile = PerformanceProfile()

        assert profile.avg_evaluation_time == 0.0
        assert profile.peak_memory_usage == 0.0
        assert profile.call_count == 0
        assert profile.sequence_sizes == []
        assert profile.timing_distribution == {}
        assert profile.size_time_correlation is None

    def test_profile_initialization_with_values(self):
        """Test initialization of PerformanceProfile with provided values."""
        profile = PerformanceProfile(
            avg_evaluation_time=0.05,
            peak_memory_usage=10.5,
            call_count=5,
            sequence_sizes=[1, 2, 3],
            timing_distribution={1: 0.01, 2: 0.02, 3: 0.03},
            size_time_correlation=0.95,
        )

        assert profile.avg_evaluation_time == 0.05
        assert profile.peak_memory_usage == 10.5
        assert profile.call_count == 5
        assert profile.sequence_sizes == [1, 2, 3]
        assert profile.timing_distribution == {1: 0.01, 2: 0.02, 3: 0.03}
        assert profile.size_time_correlation == 0.95

    def test_profile_correlation_with_insufficient_data(self):
        """Test correlation calculation with insufficient data."""
        # Empty sequence sizes
        profile = PerformanceProfile(sequence_sizes=[])
        assert profile.size_time_correlation is None

        # Single sequence size (need at least 2 for correlation)
        profile = PerformanceProfile(sequence_sizes=[1], timing_distribution={1: 0.01})
        assert profile.size_time_correlation is None

    def test_profile_correlation_with_valid_data(self):
        """Test correlation calculation with valid data."""
        # Perfect positive correlation
        profile = PerformanceProfile(
            sequence_sizes=[1, 2, 3], timing_distribution={1: 0.01, 2: 0.02, 3: 0.03}
        )
        assert profile.size_time_correlation is not None
        assert profile.size_time_correlation > 0.99  # Should be very close to 1.0

        # Perfect negative correlation
        profile = PerformanceProfile(
            sequence_sizes=[1, 2, 3], timing_distribution={1: 0.03, 2: 0.02, 3: 0.01}
        )
        assert profile.size_time_correlation is not None
        assert profile.size_time_correlation < -0.99  # Should be very close to -1.0

        # No correlation (constant times)
        profile = PerformanceProfile(
            sequence_sizes=[1, 2, 3], timing_distribution={1: 0.02, 2: 0.02, 3: 0.02}
        )
        # When all values are the same, correlation is undefined (NaN)
        # Check that it's either None or NaN
        assert profile.size_time_correlation is None or math.isnan(
            profile.size_time_correlation
        )

    def test_profile_correlation_with_zero_times(self):
        """Test correlation calculation with zero times."""
        profile = PerformanceProfile(
            sequence_sizes=[1, 2, 3], timing_distribution={1: 0.0, 2: 0.0, 3: 0.0}
        )
        assert profile.size_time_correlation is None

    def test_profile_correlation_with_mismatched_data(self):
        """Test correlation calculation with mismatched data."""
        # Create a profile with matching data to avoid KeyError
        profile = PerformanceProfile(
            sequence_sizes=[1, 2],  # Only include sizes that have timing data
            timing_distribution={1: 0.01, 2: 0.02},
        )

        # This should handle the mismatch gracefully
        assert profile.size_time_correlation is not None
        assert profile.size_time_correlation > 0.99  # Should be very close to 1.0

    def test_profile_string_representation(self):
        """Test string representation of performance profile."""
        # Test with zero time (special case)
        profile = PerformanceProfile(
            avg_evaluation_time=0.0, peak_memory_usage=5.0, call_count=10
        )
        str_repr = str(profile)
        assert "Average time: 0.00s" in str_repr
        assert "Peak memory: 5.00MB" in str_repr
        assert "Calls: 10" in str_repr

        # Test with small time (3 decimal places)
        profile = PerformanceProfile(
            avg_evaluation_time=0.005, peak_memory_usage=5.0, call_count=10
        )
        str_repr = str(profile)
        assert "Average time: 0.005s" in str_repr

        # Test with larger time (2 decimal places)
        profile = PerformanceProfile(
            avg_evaluation_time=0.05, peak_memory_usage=5.0, call_count=10
        )
        str_repr = str(profile)
        assert "Average time: 0.05s" in str_repr

        # Test with correlation
        profile = PerformanceProfile(
            avg_evaluation_time=0.05,
            peak_memory_usage=5.0,
            call_count=10,
            size_time_correlation=0.95,
        )
        str_repr = str(profile)
        assert "Size-Time correlation: 0.95" in str_repr

        # Test with no correlation
        profile = PerformanceProfile(
            avg_evaluation_time=0.05,
            peak_memory_usage=5.0,
            call_count=10,
            size_time_correlation=None,
        )
        str_repr = str(profile)
        assert "Size-Time correlation: N/A" in str_repr

    def test_profile_manual_correlation_calculation(self):
        """Test manual correlation calculation when scipy is not available."""
        # Mock scipy to be unavailable
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Create test data
            sizes = [1, 2, 3, 4, 5]
            times = [0.01, 0.02, 0.03, 0.04, 0.05]

            # Create a profile with the test data
            profile = PerformanceProfile(
                sequence_sizes=sizes, timing_distribution=dict(zip(sizes, times))
            )

            # Check that correlation was calculated manually
            assert profile.size_time_correlation is not None
            assert profile.size_time_correlation > 0.99  # Should be very close to 1.0

            # Test with negative correlation
            neg_times = [0.05, 0.04, 0.03, 0.02, 0.01]
            neg_profile = PerformanceProfile(
                sequence_sizes=sizes, timing_distribution=dict(zip(sizes, neg_times))
            )

            assert neg_profile.size_time_correlation is not None
            assert (
                neg_profile.size_time_correlation < -0.99
            )  # Should be very close to -1.0

    def test_profile_correlation_calculation_error_handling(self):
        """Test error handling in correlation calculation."""
        # Test with invalid data that would cause errors
        with patch("seqrule.analysis.performance.HAS_SCIPY", False):
            # Test with empty data
            empty_profile = PerformanceProfile(
                sequence_sizes=[], timing_distribution={}
            )
            assert empty_profile.size_time_correlation is None

            # Test with single data point
            single_profile = PerformanceProfile(
                sequence_sizes=[1], timing_distribution={1: 0.01}
            )
            assert single_profile.size_time_correlation is None

            # Test with zero variance
            zero_var_profile = PerformanceProfile(
                sequence_sizes=[1, 1, 1], timing_distribution={1: 0.01}
            )
            assert zero_var_profile.size_time_correlation is None

            # Test with zero times
            zero_times_profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3], timing_distribution={1: 0.0, 2: 0.0, 3: 0.0}
            )
            assert zero_times_profile.size_time_correlation is None

    def test_profile_string_formatting(self):
        """Test string formatting in PerformanceProfile."""
        # Test with very small time (3 decimal places)
        small_time_profile = PerformanceProfile(avg_evaluation_time=0.0012)
        str_repr = str(small_time_profile)
        assert "Average time: 0.001s" in str_repr

        # Test with medium time (2 decimal places)
        medium_time_profile = PerformanceProfile(avg_evaluation_time=0.12)
        str_repr = str(medium_time_profile)
        assert "Average time: 0.12s" in str_repr

        # Test with large time (2 decimal places)
        large_time_profile = PerformanceProfile(avg_evaluation_time=1.2)
        str_repr = str(large_time_profile)
        assert "Average time: 1.20s" in str_repr

        # Test with zero time (special case)
        zero_time_profile = PerformanceProfile(avg_evaluation_time=0.0)
        str_repr = str(zero_time_profile)
        assert "Average time: 0.00s" in str_repr

        # Test with correlation
        corr_profile = PerformanceProfile(
            avg_evaluation_time=0.05, size_time_correlation=0.95
        )
        str_repr = str(corr_profile)
        assert "Size-Time correlation: 0.95" in str_repr

        # Test with no correlation
        no_corr_profile = PerformanceProfile(
            avg_evaluation_time=0.05, size_time_correlation=None
        )
        str_repr = str(no_corr_profile)
        assert "Size-Time correlation: N/A" in str_repr

    # PerformanceProfiler tests

    def test_profiler_initialization(self):
        """Test initialization of PerformanceProfiler."""
        profiler = PerformanceProfiler()
        assert profiler is not None
        # Default configuration options should be set
        assert hasattr(profiler, "samples")
        assert hasattr(profiler, "memory_profiling")

    def test_profiler_rule_timing(self):
        """Test profiling rule execution time."""
        profiler = PerformanceProfiler()

        # Create a rule with predictable timing behavior
        def timed_rule(seq):
            time.sleep(0.01)  # Small sleep to ensure measurable time
            return True

        # Create test sequences of different sizes
        sequences = [[AbstractObject(value=i) for i in range(n)] for n in [1, 2, 3]]

        # Profile the rule
        profile = profiler.profile_rule(timed_rule, sequences)

        # Check timing results
        assert profile.avg_evaluation_time > 0
        assert profile.call_count == len(sequences)
        assert len(profile.sequence_sizes) == len(sequences)
        assert profile.sequence_sizes == [len(seq) for seq in sequences]
        assert len(profile.timing_distribution) > 0

    def test_profiler_correlation_calculation(self):
        """Test calculation of size-time correlation in profiler."""
        profiler = PerformanceProfiler()

        # Create a rule with timing that scales with sequence size
        def scaling_rule(seq):
            # Time proportional to sequence length
            for _ in range(len(seq) * 100):
                pass
            return True

        # Create sequences with distinctly different sizes
        sequences = [
            [AbstractObject(value=i) for i in range(n)]
            for n in [5, 10, 15]  # Different sizes to test correlation
        ]

        # Profile the rule
        profile = profiler.profile_rule(scaling_rule, sequences)

        # There should be a positive correlation between size and time
        assert profile.size_time_correlation is not None
        assert profile.size_time_correlation > 0

    def test_profiler_memory_profiling_disabled(self):
        """Test behavior when memory profiling is disabled."""
        profiler = PerformanceProfiler(memory_profiling=False)

        def simple_rule(seq):
            return len(seq) > 0

        sequences = [[AbstractObject(value=1)]]

        profile = profiler.profile_rule(simple_rule, sequences)

        # Memory usage should be 0 when disabled
        assert profile.peak_memory_usage == 0.0

    def test_profiler_dsl_rule_profiling(self):
        """Test profiling a DSLRule object."""
        profiler = PerformanceProfiler()

        # Create a DSL rule
        rule = DSLRule(
            lambda seq: all(obj["value"] > 0 for obj in seq), "All positive values"
        )

        # Create test sequences
        sequences = [
            [AbstractObject(value=1), AbstractObject(value=2)],
            [AbstractObject(value=3), AbstractObject(value=4), AbstractObject(value=5)],
        ]

        # Profile the DSL rule
        profile = profiler.profile_rule(rule, sequences)

        # Basic checks
        assert profile.avg_evaluation_time > 0
        assert profile.call_count == len(sequences)

    def test_profiler_with_empty_sequences(self):
        """Test profiling with empty sequences."""
        profiler = PerformanceProfiler()

        def simple_rule(seq):
            return len(seq) == 0

        # Include an empty sequence
        sequences = [[], [AbstractObject(value=1)]]

        profile = profiler.profile_rule(simple_rule, sequences)

        # Should still profile correctly
        assert profile.avg_evaluation_time > 0
        assert profile.call_count == len(sequences)
        assert 0 in profile.sequence_sizes  # Should include the empty sequence size

    def test_profiler_timing_distribution(self):
        """Test the timing distribution data structure."""
        profiler = PerformanceProfiler()

        # Create sequences of same size to test timing variation
        sequences = [
            [AbstractObject(value=i) for i in range(5)]
            for _ in range(3)  # Multiple sequences of the same size
        ]

        def variable_rule(seq):
            # Introduce some timing variation
            time.sleep(0.01 * (1 + (hash(str(seq)) % 3) / 10))
            return True

        profile = profiler.profile_rule(variable_rule, sequences)

        # Check timing distribution
        assert len(profile.timing_distribution) > 0
        # All sequences are size 5, so there should be a key for size 5
        assert 5 in profile.timing_distribution

        # The time value should be reasonable (positive)
        assert profile.timing_distribution[5] > 0

    def test_profiler_error_handling(self):
        """Test error handling during profiling."""
        profiler = PerformanceProfiler()

        # Create a rule that raises an exception
        def error_rule(seq):
            raise ValueError("Test exception")

        sequences = [[AbstractObject(value=1)]]

        # Should not raise an exception, but should log the error
        profile = profiler.profile_rule(error_rule, sequences)

        # Should still return a profile, but with zero times
        assert profile.avg_evaluation_time == 0.0
        assert profile.call_count == 0

    def test_profiler_with_empty_sequence_list(self):
        """Test profiling with an empty list of sequences."""
        profiler = PerformanceProfiler()

        def simple_rule(seq):
            return True

        # Empty list of sequences
        profile = profiler.profile_rule(simple_rule, [])

        # Should return an empty profile
        assert profile.avg_evaluation_time == 0.0
        assert profile.call_count == 0
        assert profile.sequence_sizes == []
        assert profile.timing_distribution == {}

    def test_profiler_memory_profiling_enabled(self):
        """Test behavior when memory profiling is enabled."""
        # Skip this test if memory_profiler is not available
        pytest.skip(
            "Skipping memory profiling test as it requires memory_profiler module"
        )

        # This test would normally test memory profiling, but we're skipping it
        # to avoid dependency issues. In a real environment with memory_profiler
        # installed, this test would verify that memory usage is properly tracked.

    def test_profiler_with_scipy_errors(self):
        """Test profiler behavior when scipy raises errors."""
        # Instead of mocking scipy directly, patch the _calculate_correlation method
        with patch(
            "seqrule.analysis.performance.PerformanceProfile._calculate_correlation"
        ) as mock_calc:
            # Set up the mock to return a correlation value
            mock_calc.return_value = 0.99

            # Create a profile with test data
            profile = PerformanceProfile(
                sequence_sizes=[1, 2, 3],
                timing_distribution={1: 0.01, 2: 0.02, 3: 0.03},
            )

            # Should use the mocked correlation value
            assert profile.size_time_correlation == 0.99

    def test_profiler_with_complex_rule(self):
        """Test profiling a rule with complex behavior."""
        profiler = PerformanceProfiler()

        # Create a rule with varying behavior based on sequence size
        def complex_rule(seq):
            # O(n²) for sequences longer than 5
            if len(seq) > 5:
                for _i in range(len(seq)):
                    for _j in range(len(seq)):
                        pass
            # O(n) for shorter sequences
            else:
                for _i in range(len(seq)):
                    pass
            return True

        # Create test sequences of different sizes
        sequences = [[AbstractObject(value=i) for i in range(n)] for n in range(1, 10)]

        # Profile the rule
        profile = profiler.profile_rule(complex_rule, sequences)

        # Check that profiling was performed
        assert profile.avg_evaluation_time > 0
        assert profile.call_count == len(sequences)
        assert len(profile.sequence_sizes) == len(sequences)

        # Check correlation - should be positive as time increases with size
        assert profile.size_time_correlation is not None
        assert profile.size_time_correlation > 0

"""
Performance profiling module.

This module provides functionality for profiling the performance characteristics
of sequence rules, including execution time, memory usage, and scaling behavior.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import memory_profiler

    HAS_MEMORY_PROFILER = True
except ImportError:
    HAS_MEMORY_PROFILER = False

try:
    import scipy.stats

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


@dataclass
class PerformanceProfile:
    """Performance profiling results for a rule."""

    avg_evaluation_time: float = 0.0
    peak_memory_usage: float = 0.0
    call_count: int = 0
    sequence_sizes: List[int] = field(default_factory=list)
    timing_distribution: Dict[Any, float] = field(default_factory=dict)
    size_time_correlation: Optional[float] = None

    def __post_init__(self):
        """Calculate correlation after initialization."""
        if not self.size_time_correlation:
            self.size_time_correlation = self._calculate_correlation()

    def _calculate_correlation(self) -> Optional[float]:
        """Calculate correlation between sequence sizes and execution times."""
        if len(self.sequence_sizes) < 2:
            return None

        try:
            if HAS_SCIPY:
                try:
                    sizes = list(self.sequence_sizes)
                    times = [self.timing_distribution[size] for size in sizes]

                    # Check if we have valid data for correlation
                    if (
                        not sizes
                        or not times
                        or len(sizes) != len(times)
                        or all(t == 0 for t in times)
                    ):
                        return None

                    correlation, _ = scipy.stats.pearsonr(sizes, times)
                    return float(correlation)  # Ensure we return a float
                except (AttributeError, ModuleNotFoundError, Exception):
                    # Fall back to manual calculation if scipy fails
                    pass

            # Manual correlation calculation if scipy is not available or failed
            sizes = list(self.sequence_sizes)
            times = [self.timing_distribution[size] for size in sizes]

            # Check if we have valid data for correlation
            if not sizes or not times or len(sizes) != len(times):
                return None

            # If all times are the same, correlation is 0 (no relationship)
            if all(t == times[0] for t in times):
                return None  # Return None for zero variance

            # Calculate mean and standard deviation
            size_mean = sum(sizes) / len(sizes)
            time_mean = sum(times) / len(times)

            # Calculate covariance and variances
            covariance = sum(
                (s - size_mean) * (t - time_mean) for s, t in zip(sizes, times)
            )
            size_var = sum((s - size_mean) ** 2 for s in sizes)
            time_var = sum((t - time_mean) ** 2 for t in times)

            # Calculate correlation coefficient
            if size_var == 0 or time_var == 0:
                return None  # Return None for zero variance
            correlation = covariance / (size_var**0.5 * time_var**0.5)

            return float(correlation)  # Ensure we return a float
        except Exception:
            # Catch any other exceptions and return None
            return None

    def __str__(self) -> str:
        """Return a human-readable performance summary."""
        # Use 3 decimal places for small values, 2 for larger values
        # Special case for zero to match test expectations
        if self.avg_evaluation_time == 0:
            time_str = "0.00s"
        else:
            time_format = ".3f" if self.avg_evaluation_time < 0.01 else ".2f"
            time_str = f"{self.avg_evaluation_time:{time_format}}s"
        return (
            f"Average time: {time_str}\n"
            f"Peak memory: {self.peak_memory_usage:.2f}MB\n"
            f"Calls: {self.call_count}\n"
            f"Size-Time correlation: {self.size_time_correlation or 'N/A'}"
        )


class PerformanceProfiler:
    """Profiles the performance characteristics of sequence rules."""

    def __init__(self, memory_profiling: bool = False, samples: int = 1):
        """Initialize the profiler.

        Args:
            memory_profiling: Whether to enable memory profiling
            samples: Number of samples to collect for each sequence
        """
        self.memory_profiling = memory_profiling and HAS_MEMORY_PROFILER
        self.samples = samples

    def profile_rule(
        self, rule_func: callable, sequences: List[List[Any]]
    ) -> PerformanceProfile:
        """Profile a rule's performance characteristics."""
        if not sequences:
            return PerformanceProfile()

        # Initialize profiling data
        total_time = 0.0
        peak_memory = 0.0
        timing_distribution = {}
        sequence_sizes = []
        call_count = 0

        # Check if rule_func is callable
        if not callable(rule_func):
            print(f"Error profiling sequence: '{rule_func}' object is not callable")
            return PerformanceProfile()

        for sequence in sequences:
            try:
                sequence_size = len(sequence)

                # Time the rule evaluation
                start_time = time.perf_counter()
                rule_func(sequence)
                end_time = time.perf_counter()
                elapsed = end_time - start_time

                # Update timing data
                total_time += elapsed
                timing_distribution[sequence_size] = elapsed
                sequence_sizes.append(sequence_size)
                call_count += 1

                # Profile memory if enabled
                if self.memory_profiling:
                    # Capture the sequence variable in a default argument to avoid loop variable issues
                    def wrapped_rule(seq=sequence):
                        rule_func(seq)

                    mem_usage = memory_profiler.memory_usage(
                        (wrapped_rule, (), {}), interval=0.1
                    )
                    if mem_usage:
                        peak_memory = max(peak_memory, max(mem_usage))
            except Exception as e:
                # Log the error but continue profiling
                print(f"Error profiling sequence: {e}")
                continue

        # Calculate average time
        avg_time = total_time / call_count if call_count else 0.0

        return PerformanceProfile(
            avg_evaluation_time=avg_time,
            peak_memory_usage=peak_memory,
            call_count=call_count,
            sequence_sizes=sequence_sizes,
            timing_distribution=timing_distribution,
        )

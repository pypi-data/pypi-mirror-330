"""
Analysis module for sequence rules.

This module provides tools for analyzing sequence rules, including:
- Complexity analysis
- Performance profiling
- AST pattern detection
- Property access tracking
"""

from .analyzer import AnalyzerOptions, RuleAnalysis, RuleAnalyzer
from .base import (
    AnalysisError,
    ComplexityClass,
    ComplexityScore,
    PropertyAccess,
    PropertyAccessType,
    ValidatedAccessTypeSet,
)
from .complexity import ComplexityAnalyzer, RuleComplexity
from .performance import (
    HAS_MEMORY_PROFILER,
    HAS_SCIPY,
    PerformanceProfile,
    PerformanceProfiler,
)
from .property import PropertyAnalyzer, PropertyVisitor
from .scoring import RuleScore, RuleScorer

__all__ = [
    # Base types
    "ComplexityClass",
    "PropertyAccessType",
    "PropertyAccess",
    "ValidatedAccessTypeSet",
    "ComplexityScore",
    "AnalysisError",
    # Complexity analysis
    "RuleComplexity",
    "ComplexityAnalyzer",
    # Performance profiling
    "PerformanceProfile",
    "PerformanceProfiler",
    "HAS_MEMORY_PROFILER",
    "HAS_SCIPY",
    # Property access tracking
    "PropertyVisitor",
    "PropertyAnalyzer",
    # Rule scoring
    "RuleScore",
    "RuleScorer",
    # Main analyzer
    "RuleAnalysis",
    "RuleAnalyzer",
    "AnalyzerOptions",
]

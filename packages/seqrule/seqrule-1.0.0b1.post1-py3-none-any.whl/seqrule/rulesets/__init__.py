"""
Domain-specific implementations of sequence rules.

This package contains implementations of sequence rules for various domains:

- general: General-purpose rules applicable across domains
- dna: Rules for DNA sequence analysis (GC content, motifs, etc.)
- eleusis: Rules for the Eleusis card game
- music: Rules for musical sequence analysis
- pipeline: Rules for software release pipeline validation
- tea: Rules for tea processing validation

Each domain module provides factory functions for creating domain-specific rules.
"""

# Import all domain modules
from . import dna, eleusis, general, music, pipeline, tea
from .dna import (
    create_gc_content_rule,
    create_motif_rule,
)

# Add commonly used factory functions for convenience
from .general import (
    create_alternation_rule,
    create_balanced_rule,
    create_property_match_rule,
    create_property_trend_rule,
    create_unique_property_rule,
)

__all__ = [
    # Domain modules
    "general",
    "dna",
    "eleusis",
    "music",
    "pipeline",
    "tea",
    # Common general rules
    "create_property_trend_rule",
    "create_property_match_rule",
    "create_balanced_rule",
    "create_unique_property_rule",
    "create_alternation_rule",
    # Common DNA rules
    "create_gc_content_rule",
    "create_motif_rule",
]

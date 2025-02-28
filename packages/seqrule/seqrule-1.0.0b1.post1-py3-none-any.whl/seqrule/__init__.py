"""
seqrule - A library for defining and validating sequence rules
"""

__version__ = "1.0.0"

# Core abstractions
# Analysis capabilities
from .analysis import (
    ComplexityClass,
    PropertyAccessType,
    RuleAnalyzer,
    RuleScorer,
)
from .core import (
    AbstractObject,
    DictAccessProxy,
    FormalRule,
    FormalRuleProtocol,
    Sequence,
    check_sequence,
)

# DSL module
from .dsl import DSLRule, and_atomic, if_then_rule, range_rule

# Rule combinators (aliases for better readability)
from .dsl import DSLRule as And  # DSLRule.__and__ provides AND functionality
from .dsl import DSLRule as Not  # DSLRule.__invert__ provides NOT functionality
from .dsl import DSLRule as Or  # DSLRule.__or__ provides OR functionality

# Generation utilities
from .generators import (
    ConstrainedGenerator,
    Constraint,
    ConstraintFunction,
    Domain,
    FilterRule,
    LazyGenerator,
    PropertyPattern,
    generate_counter_examples,
    generate_lazy,
    generate_sequences,
)

# Commonly used factory functions from rulesets
from .rulesets import (
    create_alternation_rule,
    create_balanced_rule,
    create_gc_content_rule,
    create_motif_rule,
    create_property_match_rule,
    create_property_trend_rule,
    create_unique_property_rule,
)

# Common type definitions
from .types import (
    ComplexityOrder,
    PredicateFunction,
    Properties,
    PropertyKey,
    PropertyValue,
    RuleRelationship,
    TransformFunction,
)

__all__ = [
    # Core abstractions
    "AbstractObject",
    "Sequence",
    "FormalRule",
    "FormalRuleProtocol",
    "check_sequence",
    "DictAccessProxy",
    # DSL and rule definitions
    "DSLRule",
    "if_then_rule",
    "range_rule",
    "and_atomic",
    # Rule combinators
    "And",
    "Or",
    "Not",
    # Generation utilities
    "generate_sequences",
    "generate_counter_examples",
    "generate_lazy",
    "LazyGenerator",
    "ConstrainedGenerator",
    "Constraint",
    "PropertyPattern",
    "Domain",
    "FilterRule",
    "ConstraintFunction",
    # Common types
    "RuleRelationship",
    "ComplexityOrder",
    "PropertyKey",
    "PropertyValue",
    "Properties",
    "PredicateFunction",
    "TransformFunction",
    # Commonly used factory functions
    "create_property_trend_rule",
    "create_property_match_rule",
    "create_balanced_rule",
    "create_unique_property_rule",
    "create_alternation_rule",
    "create_gc_content_rule",
    "create_motif_rule",
    # Analysis capabilities
    "RuleAnalyzer",
    "RuleScorer",
    "ComplexityClass",
    "PropertyAccessType",
]

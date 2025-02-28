# API Reference

## Core Module

Core abstractions and base classes for the SeqRule library.

```python
from seqrule.core import AbstractObject, FormalRule, Sequence
```

[Full Core Module Documentation](api/core.md)

## DSL Module

Domain-specific language for creating and composing rules.

```python
from seqrule.dsl import DSLRule, check_sequence
```

[Full DSL Module Documentation](api/dsl.md)

## Analysis Module

Tools for analyzing and profiling rules.

```python
from seqrule.analysis import RuleAnalyzer
```

Key features:
- Complexity analysis (time/space)
- Performance profiling
- Memory usage analysis
- Property access tracking
- Optimization suggestions

Example usage:
```python
analyzer = RuleAnalyzer().with_sequences(sample_sequences)
analysis = analyzer.analyze(my_rule)
print(f"Time complexity: {analysis.complexity.time_complexity}")
```

[Full Analysis Module Documentation](api/analysis.md)

## Domain Modules

Specialized rule generators for different domains.

### DNA Module
```python
from seqrule.rulesets.dna import create_gc_content_rule
```

[Full DNA Module Documentation](api/dna.md)

### Tea Module
```python
from seqrule.rulesets.tea import create_temperature_rule
```

[Full Tea Module Documentation](api/tea.md)

### Music Module
```python
from seqrule.rulesets.music import create_rhythm_rule
```

[Full Music Module Documentation](api/music.md)

### Pipeline Module
```python
from seqrule.rulesets.pipeline import create_dependency_rule
```

[Full Pipeline Module Documentation](api/pipeline.md)

## Utility Functions

Helper functions and common operations.

```python
from seqrule.generators import generate_sequences, generate_lazy, LazyGenerator, ConstrainedGenerator
```

### Sequence Generation

```python
def generate_sequences(domain, max_length=10, filter_rule=None):
    """
    Generate sequences from a domain of objects.
    
    Args:
        domain: List of objects to generate sequences from
        max_length: Maximum length of generated sequences
        filter_rule: Optional rule to filter generated sequences
        
    Returns:
        List of valid sequences
    """

def generate_lazy(domain, max_length=10, filter_rule=None):
    """
    Create a lazy sequence generator.
    
    Args:
        domain: List of objects to generate sequences from
        max_length: Maximum length of generated sequences
        filter_rule: Optional rule to filter generated sequences
        
    Returns:
        LazyGenerator instance
    """

class LazyGenerator:
    """
    Generator that lazily produces sequences.
    
    This generator only creates sequences when they are requested, making
    it more memory efficient for large domains or long sequences.
    
    Methods:
        __call__(): Generate the next sequence
        __iter__(): Return an iterator that generates sequences
    """

class ConstrainedGenerator:
    """
    Generator that produces sequences satisfying constraints and patterns.
    
    Methods:
        add_constraint(constraint): Add a constraint function
        add_pattern(pattern): Add a property pattern
        predict_next(sequence): Predict possible next items
        generate(max_length): Generate valid sequences
    """

[Full Utilities Documentation](api/utils.md)

## General Ruleset

### Property Rules

```python
def create_property_trend_rule(property_name, trend_type, tolerance=0):
    """
    Create a rule that checks if property values follow a trend.
    
    Args:
        property_name (str): Name of the property to check.
        trend_type (str): One of: "ascending", "descending", "constant".
        tolerance (float, optional): Allowed deviation from trend.
        
    Returns:
        Rule: A rule checking the specified trend.
    """

def create_unique_property_rule(property_name):
    """
    Create a rule requiring unique property values.
    
    Args:
        property_name (str): Name of the property to check.
        
    Returns:
        Rule: A rule checking for uniqueness.
    """

def create_dependency_rule(property_name, dependent_property, mapping):
    """
    Create a rule requiring property values to match according to a mapping.
    
    Args:
        property_name (str): Name of the primary property.
        dependent_property (str): Name of the dependent property.
        mapping (dict): Mapping from primary to dependent values.
        
    Returns:
        Rule: A rule checking the dependency.
    """

def create_balanced_rule(property_name, tolerance=0):
    """
    Create a rule requiring balanced occurrence of property values.
    
    Args:
        property_name (str): Name of the property to check.
        tolerance (float, optional): Allowed deviation from perfect balance.
        
    Returns:
        Rule: A rule checking for balance.
    """
```

## Error Handling

All functions may raise:
- `ValueError`: For invalid arguments
- `TypeError`: For arguments of wrong type
- `KeyError`: For missing required properties (in some cases)

Rules handle missing or invalid properties by skipping them rather than raising errors, unless explicitly configured otherwise. 
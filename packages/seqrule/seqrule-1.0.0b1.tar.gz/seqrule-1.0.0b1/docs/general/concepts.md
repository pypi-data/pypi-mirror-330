# Core Concepts

## Abstract Objects

The foundation of SeqRule is the `AbstractObject` class, which represents any item in a sequence. An abstract object is essentially a container for properties, allowing you to model any domain-specific entity:

```python
from seqrule import AbstractObject

# DNA nucleotide
nucleotide = AbstractObject(base="A", position=1)

# Musical note
note = AbstractObject(pitch="C4", duration=0.25, velocity=64)

# Tea processing step
step = AbstractObject(type="oxidation", duration=2.5)
```

Properties can be accessed using dictionary-style notation or attribute notation:
```python
note["pitch"]  # "C4"
note.pitch     # "C4"
```

## Rules

Rules in SeqRule are functions that take a sequence of abstract objects and return a boolean indicating whether the sequence satisfies the rule. Rules can be created in several ways:

### 1. Direct Function Definition

```python
def ascending_values(sequence):
    """Values must strictly increase."""
    return all(seq[i].value < seq[i+1].value 
              for i in range(len(seq)-1))

rule = DSLRule(ascending_values)
```

### 2. Built-in Rule Factories

```python
from seqrule.rulesets.general import create_property_trend_rule

# Create a rule requiring ascending pitch values
ascending_pitch = create_property_trend_rule(
    "pitch", 
    trend_type="ascending"
)
```

### 3. Domain-Specific Rules

```python
from seqrule.rulesets.dna import create_gc_content_rule

# Create a rule requiring 40-60% GC content
gc_rule = create_gc_content_rule(
    min_percent=40,
    max_percent=60
)
```

## Rule Composition

Rules can be combined using logical operators to create more complex rules:

```python
from seqrule import And, Or, Not

# Combine multiple rules
complex_rule = And(
    ascending_pitch,
    Or(
        create_property_trend_rule("velocity", "constant"),
        create_property_trend_rule("velocity", "ascending")
    )
)
```

## Sequence Validation

To validate a sequence against a rule:

```python
from seqrule import check_sequence

sequence = [
    AbstractObject(pitch="C4", velocity=64),
    AbstractObject(pitch="E4", velocity=72),
    AbstractObject(pitch="G4", velocity=80),
]

is_valid = check_sequence(sequence, complex_rule)
```

## Error Handling

SeqRule provides robust error handling for invalid properties and missing values:

```python
# Missing properties are skipped
obj = AbstractObject(pitch="C4")  # no velocity
rule = create_property_trend_rule("velocity", "ascending")
check_sequence([obj], rule)  # True (no values to compare)

# Invalid values are skipped
obj = AbstractObject(pitch="invalid")
rule = create_property_trend_rule("pitch", "ascending")
check_sequence([obj], rule)  # True (no valid values to compare)
```

## Domain-Specific Language (DSL)

The DSL module provides a higher-level interface for creating and combining rules:

```python
from seqrule.dsl import DSLRule, if_then_rule, range_rule, and_atomic

# Create a rule using the DSL
rule = DSLRule(ascending_values, "values must be ascending")

# Combine rules using operators
from seqrule import And, Or, Not
combined_rule = And(
    DSLRule(ascending_values, "ascending"),
    Or(
        DSLRule(even_values, "even"),
        DSLRule(positive_values, "positive")
    )
)

# Create rules with common patterns
sequence_rule = if_then_rule(
    lambda obj: obj.color == "red",  # condition
    lambda obj: obj.value > 5        # consequence
)

range_check = range_rule(
    start=2,
    length=3,
    condition=lambda obj: obj.value % 2 == 0  # even values
)
```

## Performance Considerations

1. Rules are evaluated lazily where possible
2. Property access is optimized for repeated access
3. Complex rules use short-circuit evaluation
4. Large sequences use efficient iteration
5. LazyGenerator provides memory-efficient sequence generation
6. ConstrainedGenerator enables pattern-based sequence generation

## Best Practices

1. Use built-in rule factories when possible
2. Compose complex rules from simple ones
3. Handle missing/invalid values appropriately
4. Write clear, descriptive rule names
5. Test rules with edge cases 
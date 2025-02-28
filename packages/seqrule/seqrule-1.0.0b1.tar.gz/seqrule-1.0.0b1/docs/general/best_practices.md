# Best Practices

## Rule Design

### 1. Use Built-in Rule Factories

Whenever possible, use the built-in rule factories instead of writing custom rules. They are:
- Well-tested
- Optimized for performance
- Handle edge cases correctly
- Maintain consistent behavior

```python
# Good
rule = create_property_trend_rule("value", "ascending")

# Less Good
def custom_ascending(seq):
    return all(seq[i].value < seq[i+1].value 
              for i in range(len(seq)-1))
rule = DSLRule(custom_ascending)
```

### 2. Compose Complex Rules

Break down complex rules into simpler components and compose them:

```python
# Good
pitch_rule = create_property_trend_rule("pitch", "ascending")
velocity_rule = create_property_trend_rule("velocity", "constant")
complex_rule = And(pitch_rule, velocity_rule)

# Less Good
def complex_check(seq):
    ascending = all(seq[i].pitch < seq[i+1].pitch 
                   for i in range(len(seq)-1))
    constant = all(seq[i].velocity == seq[i+1].velocity 
                  for i in range(len(seq)-1))
    return ascending and constant
```

### 3. Handle Missing and Invalid Values

Design rules to gracefully handle:
- Missing properties
- Invalid property values
- Empty sequences
- Single-element sequences

```python
# Good
def robust_rule(seq):
    valid_values = [obj.value for obj in seq 
                   if hasattr(obj, "value") and 
                   isinstance(obj.value, (int, float))]
    if len(valid_values) <= 1:
        return True
    return all(valid_values[i] < valid_values[i+1] 
              for i in range(len(valid_values)-1))

# Less Good
def fragile_rule(seq):
    return all(seq[i].value < seq[i+1].value 
              for i in range(len(seq)-1))
```

### 4. Use Clear Names and Documentation

Make rules self-documenting:

```python
# Good
def create_pitch_sequence_rule(scale, root):
    """
    Create a rule that checks if pitches form a valid sequence in the scale.
    
    Args:
        scale (str): The scale name (e.g., "major", "minor")
        root (str): The root note of the scale
        
    Returns:
        Rule: A rule that validates pitch sequences
    """
    
# Less Good
def check_notes(s, r):
    """Check if notes are valid."""
```

## Performance Optimization

### 1. Lazy Evaluation

Design rules to stop evaluation as soon as possible:

```python
# Good
def efficient_rule(seq):
    for i in range(len(seq)-1):
        if seq[i].value >= seq[i+1].value:
            return False
    return True

# Less Good
def inefficient_rule(seq):
    return all(seq[i].value < seq[i+1].value 
              for i in range(len(seq)-1))
```

### 2. Cache Property Access

Cache frequently accessed properties:

```python
# Good
def efficient_rule(seq):
    values = [obj.value for obj in seq]
    return all(values[i] < values[i+1] 
              for i in range(len(values)-1))

# Less Good
def inefficient_rule(seq):
    return all(seq[i].value < seq[i+1].value 
              for i in range(len(seq)-1))
```

### 3. Use Appropriate Data Structures

Choose efficient data structures for your use case:

```python
# Good (O(1) lookup)
def efficient_unique_check(seq):
    seen = set()
    for obj in seq:
        if obj.value in seen:
            return False
        seen.add(obj.value)
    return True

# Less Good (O(n) lookup)
def inefficient_unique_check(seq):
    values = [obj.value for obj in seq]
    return len(values) == len(set(values))
```

## Testing Strategies

### 1. Test Edge Cases

Always test:
- Empty sequences
- Single-element sequences
- Missing properties
- Invalid property values
- Boundary conditions

```python
def test_ascending_rule():
    rule = create_property_trend_rule("value", "ascending")
    
    # Empty sequence
    assert rule([])
    
    # Single element
    assert rule([AbstractObject(value=1)])
    
    # Missing properties
    assert rule([AbstractObject(other=1)])
    
    # Invalid values
    assert rule([AbstractObject(value="invalid")])
    
    # Boundary conditions
    assert rule([
        AbstractObject(value=float("-inf")),
        AbstractObject(value=float("inf"))
    ])
```

### 2. Use Property-Based Testing

Test with generated data:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_unique_rule(values):
    seq = [AbstractObject(value=v) for v in values]
    rule = create_unique_property_rule("value")
    assert rule(seq) == (len(values) == len(set(values)))
```

### 3. Test Rule Composition

Test composed rules both individually and together:

```python
def test_complex_rule():
    pitch_rule = create_property_trend_rule("pitch", "ascending")
    velocity_rule = create_property_trend_rule("velocity", "constant")
    complex_rule = And(pitch_rule, velocity_rule)
    
    # Test individual rules
    assert pitch_rule([...])
    assert velocity_rule([...])
    
    # Test composition
    assert complex_rule([...])
    assert not complex_rule([...])
```

## Error Handling

### 1. Use Appropriate Error Types

```python
def create_custom_rule(threshold):
    if not isinstance(threshold, (int, float)):
        raise TypeError("threshold must be numeric")
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
```

### 2. Provide Helpful Error Messages

```python
def validate_sequence(seq, rule):
    try:
        return rule(seq)
    except Exception as e:
        raise ValueError(
            f"Failed to validate sequence: {str(e)}\n"
            f"Sequence: {seq}\n"
            f"Rule: {rule}"
        ) from e
```

### 3. Log Validation Details

```python
import logging

def apply_rule(seq, rule):
    logging.debug(f"Applying {rule} to sequence of length {len(seq)}")
    try:
        result = rule(seq)
        logging.info(f"Rule {rule} {'passed' if result else 'failed'}")
        return result
    except Exception:
        logging.exception(f"Error applying rule {rule}")
        raise
``` 
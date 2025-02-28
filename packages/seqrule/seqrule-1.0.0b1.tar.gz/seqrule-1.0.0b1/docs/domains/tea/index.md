# Tea Processing

The tea module provides specialized rules and objects for validating tea processing sequences. It supports various types of tea processing including:
- White tea
- Green tea
- Oolong tea
- Black tea
- Pu-erh tea

## Basic Usage

```python
from seqrule import AbstractObject
from seqrule.rulesets.tea import (
    TeaType,
    create_oxidation_rule,
    create_temperature_rule,
    create_processing_sequence_rule
)

# Create a processing sequence
sequence = [
    AbstractObject(type="plucking", duration=0.5),
    AbstractObject(type="withering", duration=12),
    AbstractObject(type="oxidation", duration=2),
    AbstractObject(type="drying", duration=1, temperature=90),
]

# Check oxidation requirements
black_tea = create_oxidation_rule(TeaType.BLACK)
is_valid = black_tea(sequence)  # True

# Check temperature constraints
drying_temp = create_temperature_rule(TeaType.BLACK, "drying")
temp_ok = drying_temp(sequence)  # True
```

## Tea Types

```python
class TeaType:
    """Enumeration of tea types with their processing requirements."""
    WHITE = "white"   # Minimal processing
    GREEN = "green"   # No oxidation
    OOLONG = "oolong"  # Partial oxidation
    BLACK = "black"   # Full oxidation
    PUERH = "puerh"   # Post-fermentation
```

## Processing Rules

### Oxidation Control

```python
def create_oxidation_rule(tea_type):
    """
    Create a rule checking correct oxidation for a tea type.
    
    Args:
        tea_type (TeaType): The type of tea being processed
        
    Returns:
        Rule: A rule checking oxidation requirements
        
    Example:
        >>> green_tea = create_oxidation_rule(TeaType.GREEN)
        >>> green_tea(sequence)  # True if no oxidation
    """
```

### Temperature Control

```python
def create_temperature_rule(tea_type, step_type):
    """
    Create a rule checking temperature requirements.
    
    Args:
        tea_type (TeaType): The type of tea being processed
        step_type (str): The processing step to check
        
    Returns:
        Rule: A rule checking temperature requirements
        
    Example:
        >>> firing_temp = create_temperature_rule(
        ...     TeaType.GREEN, 
        ...     "firing"
        ... )
        >>> firing_temp(sequence)  # True if temp correct
    """
```

### Processing Sequence

```python
def create_processing_sequence_rule(
    tea_type,
    allow_optional=True
):
    """
    Create a rule checking the entire processing sequence.
    
    Args:
        tea_type (TeaType): The type of tea being processed
        allow_optional (bool): Allow optional steps
        
    Returns:
        Rule: A rule checking sequence validity
        
    Example:
        >>> sequence_rule = create_processing_sequence_rule(
        ...     TeaType.OOLONG
        ... )
        >>> sequence_rule(sequence)  # True if valid sequence
    """
```

## Processing Steps

Each tea type requires specific processing steps:

### White Tea
1. Plucking (required)
2. Withering (required)
3. Drying (required)

### Green Tea
1. Plucking (required)
2. Fixing/Firing (required)
3. Rolling (optional)
4. Drying (required)

### Oolong Tea
1. Plucking (required)
2. Withering (required)
3. Bruising (required)
4. Oxidation (required, partial)
5. Fixing (required)
6. Rolling (required)
7. Drying (required)

### Black Tea
1. Plucking (required)
2. Withering (required)
3. Rolling (required)
4. Oxidation (required, full)
5. Drying (required)

### Pu-erh Tea
1. Plucking (required)
2. Fixing (required)
3. Rolling (required)
4. Drying (required)
5. Fermentation (required)
6. Aging (optional)

## Advanced Features

### Step Duration Control

```python
def create_duration_rule(step_type, min_hours, max_hours):
    """
    Create a rule checking step duration.
    
    Args:
        step_type (str): The processing step
        min_hours (float): Minimum duration
        max_hours (float): Maximum duration
        
    Returns:
        Rule: A rule checking duration requirements
        
    Example:
        >>> withering = create_duration_rule(
        ...     "withering", 
        ...     12, 
        ...     24
        ... )
        >>> withering(sequence)  # True if duration correct
    """
```

### Complex Rules

Combine multiple rules for comprehensive validation:

```python
from seqrule import And, Or, Not

# Create a complete black tea rule
black_tea_rule = And(
    create_processing_sequence_rule(TeaType.BLACK),
    create_oxidation_rule(TeaType.BLACK),
    create_temperature_rule(TeaType.BLACK, "drying"),
    create_duration_rule("withering", 12, 24),
    create_duration_rule("oxidation", 2, 4)
)

# Create a flexible oolong rule
oolong_rule = And(
    create_processing_sequence_rule(TeaType.OOLONG),
    Or(
        create_duration_rule("oxidation", 1, 2),
        create_duration_rule("oxidation", 4, 6)
    )
)
```

## Best Practices

### 1. Step Validation

Always validate processing steps:
```python
def validate_step(step):
    """Check if step has required properties."""
    required = {"type", "duration"}
    return all(
        hasattr(step, prop)
        for prop in required
    )
```

### 2. Temperature Handling

Use consistent temperature units (Celsius):
```python
def normalize_temperature(step):
    """Convert temperature to Celsius if needed."""
    if hasattr(step, "temperature_f"):
        step.temperature = (step.temperature_f - 32) * 5/9
    return step
```

### 3. Duration Formatting

Use consistent time units (hours):
```python
def normalize_duration(step):
    """Convert duration to hours."""
    if hasattr(step, "duration_minutes"):
        step.duration = step.duration_minutes / 60
    return step
```

### 4. Error Handling

Handle missing or invalid steps gracefully:
```python
def get_step_duration(step):
    """Get step duration safely."""
    if not hasattr(step, "duration"):
        return 0
    try:
        return float(step.duration)
    except (ValueError, TypeError):
        return 0
```

## Performance Tips

1. Cache computed properties:
```python
class ProcessingSequence:
    def __init__(self, sequence):
        self._sequence = sequence
        self._total_duration = None
        
    @property
    def total_duration(self):
        if self._total_duration is None:
            self._total_duration = sum(
                get_step_duration(step)
                for step in self._sequence
            )
        return self._total_duration
```

2. Use efficient lookups:
```python
def find_step(sequence, step_type):
    """Find a step efficiently."""
    step_dict = {
        step.type: step
        for step in sequence
        if hasattr(step, "type")
    }
    return step_dict.get(step_type)
```

3. Implement early returns:
```python
def check_sequence(sequence, required_steps):
    """Check sequence validity with early returns."""
    if not sequence:
        return False
    
    seen_steps = set()
    for step in sequence:
        if not hasattr(step, "type"):
            return False
        seen_steps.add(step.type)
        
    return all(
        step in seen_steps
        for step in required_steps
    )
``` 
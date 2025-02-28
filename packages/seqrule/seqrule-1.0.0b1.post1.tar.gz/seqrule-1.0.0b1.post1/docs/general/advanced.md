# Advanced Topics

## Custom Rule Creation

### Creating Rule Factories

Rule factories are functions that create specialized rules based on parameters:

```python
def create_value_range_rule(min_value=None, max_value=None):
    """
    Create a rule that checks if values fall within a range.
    
    Args:
        min_value (float, optional): Minimum allowed value
        max_value (float, optional): Maximum allowed value
        
    Returns:
        Rule: A rule checking value ranges
    """
    def check_range(seq):
        for obj in seq:
            if not hasattr(obj, "value"):
                continue
            if not isinstance(obj.value, (int, float)):
                continue
            if min_value is not None and obj.value < min_value:
                return False
            if max_value is not None and obj.value > max_value:
                return False
        return True
        
    name = f"value_range({min_value}, {max_value})"
    return DSLRule(check_range, name=name)
```

### Stateful Rules

Rules can maintain state across sequence elements:

```python
class StatefulRule(Rule):
    def __init__(self):
        super().__init__()
        self.state = {}
        
    def reset(self):
        """Reset the rule's state."""
        self.state.clear()
        
    def __call__(self, sequence):
        self.reset()
        return self.check_sequence(sequence)
        
    def check_sequence(self, sequence):
        """Override this method to implement the rule."""
        raise NotImplementedError

class MovingAverageRule(StatefulRule):
    def __init__(self, window_size, max_deviation):
        super().__init__()
        self.window_size = window_size
        self.max_deviation = max_deviation
        
    def check_sequence(self, sequence):
        values = []
        for obj in sequence:
            if not hasattr(obj, "value"):
                continue
            if not isinstance(obj.value, (int, float)):
                continue
                
            values.append(obj.value)
            if len(values) > self.window_size:
                values.pop(0)
                
            if len(values) == self.window_size:
                avg = sum(values) / len(values)
                if abs(values[-1] - avg) > self.max_deviation:
                    return False
                    
        return True
```

## Rule Composition

### Custom Composite Rules

Create specialized composite rules for complex logic:

```python
class Majority(CompositeRule):
    """Rule that passes if more than half of sub-rules pass."""
    
    def __call__(self, sequence):
        results = [rule(sequence) for rule in self.rules]
        return sum(results) > len(results) / 2

class AtLeastN(CompositeRule):
    """Rule that passes if at least N sub-rules pass."""
    
    def __init__(self, n, *rules, name=None):
        super().__init__(*rules, name=name)
        self.n = n
        
    def __call__(self, sequence):
        results = [rule(sequence) for rule in self.rules]
        return sum(results) >= self.n
```

### Rule Decorators

Use decorators to modify rule behavior:

```python
def skip_empty(rule):
    """Decorator that makes a rule pass for empty sequences."""
    def wrapper(sequence):
        if not sequence:
            return True
        return rule(sequence)
    return wrapper

def require_minimum_length(min_length):
    """Decorator that requires a minimum sequence length."""
    def decorator(rule):
        def wrapper(sequence):
            if len(sequence) < min_length:
                return False
            return rule(sequence)
        return wrapper
    return decorator

@skip_empty
@require_minimum_length(3)
def complex_rule(sequence):
    # Rule implementation
    pass
```

## Domain Extension

### Creating Domain-Specific Objects

Extend AbstractObject for specialized domains:

```python
class Note(AbstractObject):
    """Musical note with specialized methods."""
    
    def __init__(self, pitch, duration, velocity=64):
        super().__init__(
            pitch=pitch,
            duration=duration,
            velocity=velocity
        )
        
    @property
    def frequency(self):
        """Convert pitch to frequency in Hz."""
        # Implementation
        pass
        
    def transpose(self, semitones):
        """Return a new note transposed by semitones."""
        # Implementation
        pass

class DNABase(AbstractObject):
    """DNA base with biological properties."""
    
    def __init__(self, base, position):
        super().__init__(
            base=base.upper(),
            position=position
        )
        
    @property
    def complement(self):
        """Get the complementary base."""
        complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return complements[self.base]
```

### Domain-Specific Rule Sets

Create specialized rule sets for domains:

```python
class MusicRuleSet:
    """Collection of music-specific rules."""
    
    @staticmethod
    def create_chord_rule(chord_type):
        """Create a rule checking for valid chord structures."""
        # Implementation
        pass
        
    @staticmethod
    def create_voice_leading_rule(max_leap=12):
        """Create a rule checking voice leading constraints."""
        # Implementation
        pass
        
    @staticmethod
    def create_harmony_rule(key):
        """Create a rule checking harmonic progression."""
        # Implementation
        pass

class DNARuleSet:
    """Collection of DNA-specific rules."""
    
    @staticmethod
    def create_restriction_site_rule(site):
        """Create a rule checking for restriction sites."""
        # Implementation
        pass
        
    @staticmethod
    def create_primer_rule(length=20, gc_content=(40, 60)):
        """Create a rule for valid primer sequences."""
        # Implementation
        pass
```

## Meta-Rules

### Rule Generators

Create rules that generate other rules:

```python
def create_meta_rule(property_names, rule_type):
    """
    Create rules for multiple properties.
    
    Args:
        property_names (list[str]): Properties to check
        rule_type (str): Type of rule to create
        
    Returns:
        CompositeRule: Combined rules for all properties
    """
    rules = []
    for prop in property_names:
        if rule_type == "trend":
            rules.append(
                create_property_trend_rule(prop, "ascending")
            )
        elif rule_type == "unique":
            rules.append(
                create_unique_property_rule(prop)
            )
    return And(*rules)

# Usage
numeric_properties = ["value", "count", "index"]
all_ascending = create_meta_rule(
    numeric_properties, 
    "trend"
)
```

### Rule Analysis

Analyze rule behavior and relationships:

```python
class RuleAnalyzer:
    """Analyze relationships between rules."""
    
    @staticmethod
    def are_equivalent(rule1, rule2, test_sequences):
        """Check if two rules are equivalent."""
        return all(
            rule1(seq) == rule2(seq)
            for seq in test_sequences
        )
        
    @staticmethod
    def is_stricter(rule1, rule2, test_sequences):
        """Check if rule1 is stricter than rule2."""
        return all(
            rule1(seq) <= rule2(seq)
            for seq in test_sequences
        )
        
    @staticmethod
    def find_minimal_failing(rule, sequence):
        """Find minimal subsequence that fails the rule."""
        n = len(sequence)
        for length in range(1, n + 1):
            for start in range(n - length + 1):
                subseq = sequence[start:start + length]
                if not rule(subseq):
                    return subseq
        return None
``` 
# Rule Analysis Guide

This guide covers SeqRule's analysis capabilities, designed to help researchers understand and optimize their rule implementations.

## Overview

The analysis module provides tools for:
- Algorithmic complexity analysis
- Performance benchmarking
- Memory usage profiling
- Property access patterns
- Optimization detection

## Basic Analysis

### Single Rule Analysis

```python
from seqrule.analysis import RuleAnalyzer

# Create analyzer with sample sequences
analyzer = RuleAnalyzer().with_sequences(sample_sequences)

# Analyze a rule
analysis = analyzer.analyze(my_rule)

# Access results
print(f"Time Complexity: {analysis.complexity.time_complexity}")
print(f"Space Complexity: {analysis.complexity.space_complexity}")
print(f"Cyclomatic Complexity: {analysis.cyclomatic_complexity}")
```

### Batch Analysis

```python
# Analyze multiple rules
rules = [rule1, rule2, rule3]
analyses = [analyzer.analyze(rule) for rule in rules]

# Compare complexities
for rule, analysis in zip(rules, analyses):
    print(f"{rule.name}: {analysis.complexity.time_complexity}")
```

## Performance Profiling

### Memory Usage

```python
# Enable memory profiling
analyzer = (RuleAnalyzer()
           .with_sequences(sequences)
           .with_options(memory_profiling=True))

analysis = analyzer.analyze(rule)
print(f"Peak Memory Usage: {analysis.performance.peak_memory_usage} MB")
```

### Time Performance

```python
# Get detailed timing information
profile = analysis.performance
print(f"Average Time: {profile.avg_evaluation_time} seconds")
print(f"Size-Time Correlation: {profile.size_time_correlation}")

# The correlation coefficient (using scipy.stats.pearsonr) indicates:
# - Positive values: Time increases with sequence size
# - Values near 1: Strong linear relationship
# - Values near 0: No clear relationship
# - Negative values: Time decreases with sequence size (rare)
```

## Property Analysis

Track how rules access object properties:

```python
# Get property access patterns
for prop_name, access in analysis.properties.items():
    print(f"\nProperty: {prop_name}")
    print(f"Access Count: {access.access_count}")
    print(f"Access Types: {access.access_types}")
    print(f"Nested Properties: {access.nested_properties}")

# Example of tracked access types:
# - PropertyAccessType.READ: Direct property reads
# - PropertyAccessType.METHOD: Method calls (e.g., .get())
# - PropertyAccessType.CONDITIONAL: Used in if statements
# - PropertyAccessType.COMPARISON: Used in comparisons
# - PropertyAccessType.NESTED: Nested property access
```

### Nested Property Analysis

The analyzer now tracks nested property relationships and different types of access patterns:

```python
def complex_property_rule(seq):
    if not seq:
        return True
    first = seq[0]
    if "nested" in first.properties:
        nested = first["nested"]
        if "deep" in nested:
            return nested["deep"] > first["value"]
    return True

analysis = analyzer.analyze(DSLRule(complex_property_rule))
# Shows nested relationship between 'nested' and 'deep' properties
print(analysis.properties["nested"].nested_properties)  # {'deep'}
print(analysis.properties["nested"].access_types)  # {PropertyAccessType.NESTED, PropertyAccessType.CONDITIONAL}
```

### Bottleneck Detection

The complexity analyzer can now identify performance bottlenecks in your rules:

```python
analysis = analyzer.analyze(my_rule)
print("Bottlenecks:")
for bottleneck in analysis.complexity.bottlenecks:
    print(f"- {bottleneck}")

# Example bottlenecks:
# - "Nested loop at line 45"
# - "Inefficient collection building at line 23"
# - "Repeated property access without caching"
```

## Optimization Suggestions

```python
# Get optimization suggestions
for suggestion in analysis.optimization_suggestions:
    print(f"- {suggestion}")
```

## Rule Comparison

Compare rules for equivalence and relationships:

```python
comparison = analyzer.compare_rules(rule1, rule2)
print(f"Relationship: {comparison['relationship']}")
print(f"Stricter Rule: {comparison['stricter_rule']}")
```

## Research Applications

### Complexity Analysis

The analyzer detects:
- Time complexity classes (O(1) to O(n!))
- Space complexity patterns
- Nested loops and recursion
- Temporary collection creation
- Property access patterns

### Performance Analysis

Benchmark rules with:
- Various sequence sizes
- Different property distributions
- Edge cases and stress tests
- Memory usage patterns
- GC impact analysis

### Optimization Research

Study optimization opportunities:
- Property caching strategies
- Algorithm improvements
- Memory usage patterns
- Rule composition effects
- Performance bottlenecks

## Best Practices

1. **Sample Sequences**
   - Use diverse sequence sizes
   - Include edge cases
   - Represent real-world data
   - Cover different property distributions

2. **Performance Analysis**
   - Profile with realistic data sizes
   - Consider memory constraints
   - Measure GC impact
   - Track size-time correlation

3. **Optimization**
   - Address O(n²) or higher complexity
   - Minimize temporary collections
   - Cache frequently accessed properties
   - Use generators for large sequences

4. **Comparison**
   - Compare alternative implementations
   - Measure trade-offs
   - Document performance characteristics
   - Consider space-time trade-offs

## Advanced Topics

### Custom Analysis

Extend the analyzer for specific needs:

```python
class CustomAnalyzer(RuleAnalyzer):
    def analyze(self, rule):
        # Add custom analysis logic
        base_analysis = super().analyze(rule)
        # Add custom metrics
        return base_analysis
```

### Batch Processing

Analyze multiple rules efficiently:

```python
def analyze_ruleset(rules, sequences):
    analyzer = RuleAnalyzer().with_sequences(sequences)
    with ThreadPoolExecutor() as executor:
        analyses = list(executor.map(analyzer.analyze, rules))
    return analyses
```

### Visualization

Create performance visualizations:

```python
def plot_performance(analyses):
    import matplotlib.pyplot as plt
    
    sizes = [len(seq) for seq in sequences]
    times = [a.performance.avg_evaluation_time for a in analyses]
    
    plt.plot(sizes, times)
    plt.xlabel('Sequence Size')
    plt.ylabel('Average Time (s)')
    plt.title('Rule Performance Scaling')
    plt.show()
```

## Common Patterns

### Time Complexity Patterns

- O(1): Direct property access
- O(n): Single pass through sequence
- O(n²): Nested loops or comparisons
- O(n log n): Sorting operations

### Space Complexity Patterns

- O(1): No temporary storage
- O(n): List comprehensions
- O(n²): Nested collections
- O(log n): Divide and conquer

### Optimization Patterns

- Replace nested loops with maps/sets
- Use generators for large sequences
- Cache computed values
- Minimize object creation

## Future Directions

Planned enhancements:
- Machine learning-based optimization suggestions
- Interactive visualization dashboard
- Distributed performance testing
- Custom metric plugins
- Automated regression detection 
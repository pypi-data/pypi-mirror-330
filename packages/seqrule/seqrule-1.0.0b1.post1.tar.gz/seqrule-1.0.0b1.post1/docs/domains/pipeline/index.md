# Pipeline Validation

The pipeline module provides specialized rules and objects for validating software release pipelines. It supports various aspects of pipeline validation including:
- Stage ordering
- Dependency checks
- Resource requirements
- Timing constraints
- Error handling

## Basic Usage

```python
from seqrule import AbstractObject
from seqrule.rulesets.pipeline import (
    create_stage_order_rule,
    create_dependency_rule,
    create_resource_rule
)

# Create a pipeline sequence
sequence = [
    AbstractObject(stage="build", duration=5, resources=["cpu"]),
    AbstractObject(stage="test", duration=10, resources=["cpu", "memory"]),
    AbstractObject(stage="deploy", duration=15, resources=["network"]),
]

# Check stage ordering
stage_rule = create_stage_order_rule([
    "build",
    "test",
    "deploy"
])
is_valid = stage_rule(sequence)  # True

# Check resource requirements
resource_rule = create_resource_rule(
    required=["cpu", "memory"]
)
has_resources = resource_rule(sequence)  # True
```

## Pipeline Rules

### Stage Ordering

```python
def create_stage_order_rule(required_stages):
    """
    Create a rule enforcing stage order.
    
    Args:
        required_stages (list[str]): Ordered list of required stages
        
    Returns:
        Rule: A rule checking stage order
        
    Example:
        >>> stages = ["build", "test", "deploy"]
        >>> order_rule = create_stage_order_rule(stages)
        >>> order_rule(sequence)  # True if stages in order
    """
```

### Dependencies

```python
def create_dependency_rule(dependencies):
    """
    Create a rule checking stage dependencies.
    
    Args:
        dependencies (dict): Map of stage to required stages
        
    Returns:
        Rule: A rule checking dependencies
        
    Example:
        >>> deps = {"deploy": ["build", "test"]}
        >>> dep_rule = create_dependency_rule(deps)
        >>> dep_rule(sequence)  # True if deps satisfied
    """
```

### Resources

```python
def create_resource_rule(
    required=None,
    forbidden=None
):
    """
    Create a rule checking resource requirements.
    
    Args:
        required (list[str]): Required resources
        forbidden (list[str]): Forbidden resources
        
    Returns:
        Rule: A rule checking resources
        
    Example:
        >>> res_rule = create_resource_rule(
        ...     required=["cpu"],
        ...     forbidden=["gpu"]
        ... )
        >>> res_rule(sequence)  # True if resources valid
    """
```

## Advanced Features

### Timing Constraints

```python
def create_timing_rule(
    max_duration=None,
    stage_limits=None
):
    """
    Create a rule checking timing constraints.
    
    Args:
        max_duration (int): Maximum total duration
        stage_limits (dict): Per-stage duration limits
        
    Returns:
        Rule: A rule checking timing constraints
        
    Example:
        >>> timing = create_timing_rule(
        ...     max_duration=60,
        ...     stage_limits={"build": 10}
        ... )
        >>> timing(sequence)  # True if timing valid
    """
```

### Error Handling

```python
def create_error_rule(
    required_handlers=None,
    max_retries=3
):
    """
    Create a rule checking error handling.
    
    Args:
        required_handlers (list[str]): Required error handlers
        max_retries (int): Maximum retry attempts
        
    Returns:
        Rule: A rule checking error handling
        
    Example:
        >>> error_rule = create_error_rule(
        ...     required_handlers=["timeout", "network"]
        ... )
        >>> error_rule(sequence)  # True if handlers present
    """
```

### Complex Rules

Combine multiple rules for comprehensive validation:

```python
from seqrule import And, Or, Not

# Create a complete pipeline rule
pipeline_rule = And(
    create_stage_order_rule(["build", "test", "deploy"]),
    create_resource_rule(required=["cpu"]),
    create_timing_rule(max_duration=60),
    Not(create_resource_rule(forbidden=["gpu"]))
)

# Create a flexible deployment rule
deploy_rule = And(
    create_stage_order_rule(["build", "test"]),
    Or(
        create_stage_order_rule(["deploy-staging"]),
        create_stage_order_rule(["deploy-prod"])
    )
)
```

## Best Practices

### 1. Stage Validation

Always validate pipeline stages:
```python
def validate_stage(stage):
    """Check if stage has required properties."""
    required = {"stage", "duration"}
    return all(
        hasattr(stage, prop)
        for prop in required
    )
```

### 2. Resource Handling

Track resource usage carefully:
```python
def check_resources(stage):
    """Check resource availability."""
    if not hasattr(stage, "resources"):
        return True
        
    available = get_available_resources()
    return all(
        resource in available
        for resource in stage.resources
    )
```

### 3. Error Recovery

Plan for failures:
```python
def create_recovery_plan(stage):
    """Create error recovery plan."""
    return {
        "retry_count": 0,
        "max_retries": 3,
        "backoff": 1.5,
        "handlers": {
            "timeout": lambda: retry_with_timeout(stage),
            "network": lambda: retry_with_network(stage)
        }
    }
```

### 4. Timing Management

Handle timing constraints:
```python
def check_timing(sequence):
    """Check timing constraints."""
    total = 0
    for stage in sequence:
        if not hasattr(stage, "duration"):
            continue
        try:
            total += float(stage.duration)
        except (ValueError, TypeError):
            continue
    return total
```

## Performance Tips

1. Cache computed properties:
```python
class Pipeline:
    def __init__(self, sequence):
        self._sequence = sequence
        self._total_duration = None
        self._resource_usage = None
        
    @property
    def total_duration(self):
        if self._total_duration is None:
            self._total_duration = sum(
                stage.duration for stage in self._sequence
                if hasattr(stage, "duration")
            )
        return self._total_duration
        
    @property
    def resource_usage(self):
        if self._resource_usage is None:
            self._resource_usage = set()
            for stage in self._sequence:
                if hasattr(stage, "resources"):
                    self._resource_usage.update(stage.resources)
        return self._resource_usage
```

2. Use efficient lookups:
```python
def find_stage(sequence, stage_name):
    """Find a stage efficiently."""
    stage_dict = {
        stage.stage: stage
        for stage in sequence
        if hasattr(stage, "stage")
    }
    return stage_dict.get(stage_name)
```

3. Implement early returns:
```python
def check_dependencies(sequence, dependencies):
    """Check dependencies with early returns."""
    if not sequence:
        return False
        
    seen_stages = set()
    for stage in sequence:
        if not hasattr(stage, "stage"):
            return False
            
        stage_name = stage.stage
        if stage_name in dependencies:
            required = dependencies[stage_name]
            if not all(req in seen_stages for req in required):
                return False
                
        seen_stages.add(stage_name)
        
    return True
```

## Pipeline Constants

```python
# Common stage types
STAGES = {
    "build": {
        "required": True,
        "resources": ["cpu", "memory"],
        "max_duration": 30
    },
    "test": {
        "required": True,
        "resources": ["cpu", "memory"],
        "max_duration": 60
    },
    "deploy": {
        "required": True,
        "resources": ["network"],
        "max_duration": 120
    }
}

# Resource constraints
RESOURCES = {
    "cpu": {
        "limit": 4,
        "unit": "cores"
    },
    "memory": {
        "limit": 16,
        "unit": "GB"
    },
    "network": {
        "limit": 1000,
        "unit": "Mbps"
    }
}

# Error handling strategies
ERROR_HANDLERS = {
    "timeout": {
        "max_retries": 3,
        "backoff": 1.5
    },
    "network": {
        "max_retries": 5,
        "backoff": 2.0
    },
    "resource": {
        "max_retries": 2,
        "backoff": 1.0
    }
}
``` 
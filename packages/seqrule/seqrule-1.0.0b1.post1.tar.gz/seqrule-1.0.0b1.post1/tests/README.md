# SeqRule Test Suite

This directory contains tests for the SeqRule library, which provides tools for defining, analyzing, and validating sequence rules.

## Directory Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interactions
└── functional/     # Functional tests for end-to-end scenarios
```

## Running Tests

### All Tests

```bash
python -m pytest
```

### Unit Tests Only

```bash
python -m pytest tests/unit
```

### Integration Tests Only

```bash
python -m pytest tests/integration
```

### Functional Tests Only

```bash
python -m pytest tests/functional
```

### Specific Test Modules

```bash
# Test core functionality
python -m pytest tests/unit/core

# Test property analysis
python -m pytest tests/unit/analysis/property
```

## Test Design Principles

1. **Independence**: Tests should be independent and not rely on the state of other tests.
2. **Clarity**: Test names should clearly describe what they're testing.
3. **Completeness**: Tests should cover normal cases, edge cases, and error handling.
4. **Fixtures**: Use fixtures for common setup rather than duplicating code.

## Contributing Tests

When contributing new tests:

1. Place them in the appropriate directory based on what they're testing.
2. Use clear, descriptive names for test files, classes, and functions.
3. Include docstrings that explain what each test is verifying.
4. Use assertions that clearly communicate what's being tested. 
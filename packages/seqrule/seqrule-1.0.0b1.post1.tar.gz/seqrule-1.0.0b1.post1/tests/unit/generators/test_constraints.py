"""
Unit tests for the constraint-based sequence generation functionality.
"""

from seqrule.generators import Constraint


def test_constraint_creation():
    """Test basic constraint creation and initialization."""
    constraint = Constraint(
        property_name="value",
        condition=lambda x: x > 10,
        description="Value must be greater than 10",
    )

    # Check attributes are set correctly
    assert constraint.property_name == "value"
    assert constraint.description == "Value must be greater than 10"
    assert callable(constraint.condition)


def test_constraint_call():
    """Test calling a constraint directly."""
    # Create constraint for even values
    even_constraint = Constraint(
        property_name="value",
        condition=lambda x: x % 2 == 0,
        description="Value must be even",
    )

    # Test direct calling
    assert even_constraint(2) is True
    assert even_constraint(1) is False
    assert even_constraint(4) is True
    assert even_constraint(3) is False


def test_constraint_with_complex_condition():
    """Test constraint with a more complex condition."""
    # Create constraint with a more complex condition
    constraint = Constraint(
        property_name="text",
        condition=lambda x: x is not None and len(x) > 3 and x.startswith("a"),
        description="Text must be longer than 3 chars and start with 'a'",
    )

    # Test with various values
    assert constraint("abcd") is True
    assert constraint("abc") is False  # Too short
    assert constraint("bcde") is False  # Doesn't start with 'a'
    assert constraint(None) is False  # None value


def test_constraint_with_custom_description():
    """Test constraint with a custom description."""
    constraint = Constraint(
        property_name="count",
        condition=lambda x: 5 <= x <= 10,
        description="Count must be between 5 and 10, inclusive",
    )

    # Check description
    assert constraint.description == "Count must be between 5 and 10, inclusive"

    # Check functionality
    assert constraint(7) is True
    assert constraint(5) is True
    assert constraint(10) is True
    assert constraint(4) is False
    assert constraint(11) is False


def test_constraint_with_default_description():
    """Test constraint with default description."""
    constraint = Constraint(property_name="flag", condition=lambda x: x is True)

    # Should have empty description by default
    assert constraint.description == ""

    # Test functionality
    assert constraint(True) is True
    assert constraint(False) is False


def test_constraint_with_invalid_values():
    """Test constraint with invalid or unexpected value types."""
    # Constraint expecting numbers with a condition that handles errors gracefully
    constraint = Constraint(
        property_name="value",
        condition=lambda x: False if not isinstance(x, (int, float)) else x > 0,
    )

    # Test with valid input
    assert constraint(5) is True
    assert constraint(0) is False
    assert constraint(-5) is False

    # Test with invalid inputs
    assert constraint("not a number") is False
    assert constraint(None) is False

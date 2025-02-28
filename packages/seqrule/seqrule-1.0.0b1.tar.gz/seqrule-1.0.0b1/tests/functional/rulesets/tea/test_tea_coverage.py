"""
Coverage tests for the tea ruleset.

These tests focus on covering specific lines and edge cases in the tea ruleset
that aren't covered by the main test suite.
"""

import pytest

from seqrule.rulesets.tea import (
    ProcessingStep,
    TeaProcess,
    TeaType,
    create_tea_sequence_rule,
)


class TestTeaCoverage:
    """Test suite for tea ruleset coverage."""

    def test_tea_process_validation(self):
        """Test validation in TeaProcess initialization."""
        # Test temperature validation
        with pytest.raises(ValueError, match="Temperature cannot be negative"):
            TeaProcess(
                tea_type=TeaType.GREEN, step=ProcessingStep.FIXING, temperature=-10
            )

        # Test duration validation
        with pytest.raises(ValueError, match="Duration cannot be negative"):
            TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.FIXING, duration=-5)

        # Test humidity validation
        with pytest.raises(ValueError, match="Humidity must be between 0 and 100"):
            TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.FIXING, humidity=110)

        # Test leaf ratio validation
        with pytest.raises(ValueError, match="Leaf ratio must be positive"):
            TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.FIXING, leaf_ratio=0)

    def test_tea_process_repr(self):
        """Test the __repr__ method of TeaProcess."""
        tea_process = TeaProcess(
            tea_type=TeaType.GREEN,
            step=ProcessingStep.FIXING,
            temperature=80,
            duration=2,
        )

        # Check that __repr__ returns a string
        repr_str = repr(tea_process)
        assert isinstance(repr_str, str)
        assert "TeaProcess" in repr_str
        assert "green" in repr_str.lower()  # Check for lowercase tea type
        assert "fixing" in repr_str.lower()  # Check for lowercase step
        assert "temp=80" in repr_str
        assert "duration=2" in repr_str

    def test_tea_sequence_rule_with_invalid_step(self):
        """Test tea sequence rule with an invalid step."""
        rule = create_tea_sequence_rule(TeaType.GREEN)

        # Create a sequence with an invalid step (not in the required steps)
        seq = [TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.AGING)]

        # This should fail because AGING is not in the required steps for GREEN tea
        assert rule(seq) is False

        # Create a sequence with steps in wrong order
        seq = [
            TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.FIXING),
            TeaProcess(tea_type=TeaType.GREEN, step=ProcessingStep.PLUCKING),
        ]

        # This should fail because PLUCKING should come before FIXING
        assert rule(seq) is False

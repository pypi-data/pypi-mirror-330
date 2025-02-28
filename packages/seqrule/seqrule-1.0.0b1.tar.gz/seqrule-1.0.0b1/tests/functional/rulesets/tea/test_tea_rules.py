"""
Tests for the tea ruleset.

These tests verify that the tea rule factories create rules
that correctly validate tea processing sequences.
"""

import pytest

from seqrule.rulesets.tea import (
    ProcessingStep,
    QualityMetrics,
    TeaProcess,
    TeaType,
    create_duration_rule,
    create_humidity_rule,
    create_oxidation_level_rule,
    create_quality_rule,
    create_tea_sequence_rule,
    create_temperature_rule,
)


@pytest.fixture
def green_tea_sequence():
    """Provide a valid green tea processing sequence."""
    return [
        TeaProcess(TeaType.GREEN, ProcessingStep.PLUCKING),
        TeaProcess(
            TeaType.GREEN,
            ProcessingStep.WITHERING,
            temperature=25,
            duration=2,
            humidity=70,
        ),
        TeaProcess(
            TeaType.GREEN, ProcessingStep.FIXING, temperature=130, duration=0.1
        ),  # 6 minutes
        TeaProcess(TeaType.GREEN, ProcessingStep.ROLLING, duration=0.25),  # 15 minutes
        TeaProcess(TeaType.GREEN, ProcessingStep.DRYING, temperature=80, duration=1),
    ]


@pytest.fixture
def oolong_tea_sequence():
    """Provide a valid oolong tea processing sequence."""
    return [
        TeaProcess(TeaType.OOLONG, ProcessingStep.PLUCKING),
        TeaProcess(
            TeaType.OOLONG,
            ProcessingStep.WITHERING,
            temperature=25,
            duration=2,
            humidity=70,
        ),
        TeaProcess(TeaType.OOLONG, ProcessingStep.BRUISING, duration=0.5),
        TeaProcess(
            TeaType.OOLONG,
            ProcessingStep.OXIDATION,
            temperature=28,
            duration=3,
            humidity=80,
        ),
        TeaProcess(
            TeaType.OOLONG, ProcessingStep.FIXING, temperature=130, duration=0.1
        ),
        TeaProcess(TeaType.OOLONG, ProcessingStep.ROLLING, duration=0.25),
        TeaProcess(TeaType.OOLONG, ProcessingStep.DRYING, temperature=85, duration=1),
    ]


@pytest.fixture
def quality_metrics():
    """Provide quality metrics for testing."""
    return QualityMetrics(
        moisture_content=5.0,
        leaf_integrity=0.8,
        color_value=25.0,
        aroma_intensity=0.7,
        taste_profile={"sweetness": 0.6, "bitterness": 0.2},
    )


class TestTeaRules:
    """Test suite for tea processing rules."""

    def test_tea_sequence_rule(self, green_tea_sequence, oolong_tea_sequence):
        """Test that tea sequence rule correctly validates processing sequences."""
        # Create rules for different tea types
        green_rule = create_tea_sequence_rule(TeaType.GREEN)
        oolong_rule = create_tea_sequence_rule(TeaType.OOLONG)

        # Test with valid sequences
        assert green_rule(green_tea_sequence) is True
        assert oolong_rule(oolong_tea_sequence) is True

        # Test with wrong tea type
        assert green_rule(oolong_tea_sequence) is False
        assert oolong_rule(green_tea_sequence) is False

        # Test with incorrect order
        incorrect_order = list(green_tea_sequence)
        incorrect_order[1], incorrect_order[3] = incorrect_order[3], incorrect_order[1]
        assert green_rule(incorrect_order) is False

        # Test with missing step
        incomplete_sequence = green_tea_sequence[:-1]  # Remove drying step
        assert green_rule(incomplete_sequence) is True  # Partial sequences are valid

        # Test with empty sequence
        assert green_rule([]) is True  # Empty sequence is valid by default

    def test_temperature_rule(self, green_tea_sequence):
        """Test that temperature rule correctly validates temperature ranges."""
        # Create a rule for fixing temperature
        rule = create_temperature_rule(ProcessingStep.FIXING, 120, 140)

        # Test with valid temperature
        assert rule(green_tea_sequence) is True

        # Test with temperature too low
        low_temp = list(green_tea_sequence)
        low_temp[2] = TeaProcess(
            TeaType.GREEN, ProcessingStep.FIXING, temperature=110, duration=0.1
        )
        assert rule(low_temp) is False

        # Test with temperature too high
        high_temp = list(green_tea_sequence)
        high_temp[2] = TeaProcess(
            TeaType.GREEN, ProcessingStep.FIXING, temperature=150, duration=0.1
        )
        assert rule(high_temp) is False

        # Test with missing temperature
        no_temp = list(green_tea_sequence)
        no_temp[2] = TeaProcess(TeaType.GREEN, ProcessingStep.FIXING, duration=0.1)
        assert rule(no_temp) is True  # No temperature is valid (not checked)

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence is valid by default

    def test_humidity_rule(self, green_tea_sequence):
        """Test that humidity rule correctly validates humidity ranges."""
        # Create a rule for withering humidity
        rule = create_humidity_rule(ProcessingStep.WITHERING, 65, 75)

        # Test with valid humidity
        assert rule(green_tea_sequence) is True

        # Test with humidity too low
        low_humidity = list(green_tea_sequence)
        low_humidity[1] = TeaProcess(
            TeaType.GREEN,
            ProcessingStep.WITHERING,
            temperature=25,
            duration=2,
            humidity=60,
        )
        assert rule(low_humidity) is False

        # Test with humidity too high
        high_humidity = list(green_tea_sequence)
        high_humidity[1] = TeaProcess(
            TeaType.GREEN,
            ProcessingStep.WITHERING,
            temperature=25,
            duration=2,
            humidity=80,
        )
        assert rule(high_humidity) is False

        # Test with missing humidity
        no_humidity = list(green_tea_sequence)
        no_humidity[1] = TeaProcess(
            TeaType.GREEN, ProcessingStep.WITHERING, temperature=25, duration=2
        )
        assert rule(no_humidity) is True  # No humidity is valid (not checked)

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence is valid by default

    def test_duration_rule(self, green_tea_sequence):
        """Test that duration rule correctly validates duration ranges."""
        # Create a rule for drying duration
        rule = create_duration_rule(ProcessingStep.DRYING, 0.5, 1.5)

        # Test with valid duration
        assert rule(green_tea_sequence) is True

        # Test with duration too short
        short_duration = list(green_tea_sequence)
        short_duration[4] = TeaProcess(
            TeaType.GREEN, ProcessingStep.DRYING, temperature=80, duration=0.4
        )
        assert rule(short_duration) is False

        # Test with duration too long
        long_duration = list(green_tea_sequence)
        long_duration[4] = TeaProcess(
            TeaType.GREEN, ProcessingStep.DRYING, temperature=80, duration=2.0
        )
        assert rule(long_duration) is False

        # Test with missing duration
        no_duration = list(green_tea_sequence)
        no_duration[4] = TeaProcess(
            TeaType.GREEN, ProcessingStep.DRYING, temperature=80
        )
        assert rule(no_duration) is True  # No duration is valid (not checked)

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence is valid by default

    def test_oxidation_level_rule(self, oolong_tea_sequence):
        """Test that oxidation level rule correctly validates oxidation times."""
        # Create rules for different tea types
        green_rule = create_oxidation_level_rule(TeaType.GREEN)
        oolong_rule = create_oxidation_level_rule(TeaType.OOLONG)
        black_rule = create_oxidation_level_rule(TeaType.BLACK)

        # Test with valid oxidation for oolong
        assert oolong_rule(oolong_tea_sequence) is True

        # Test with incorrect oxidation time
        incorrect_oxidation = list(oolong_tea_sequence)
        incorrect_oxidation[3] = TeaProcess(
            TeaType.OOLONG,
            ProcessingStep.OXIDATION,
            temperature=28,
            duration=1.0,
            humidity=80,  # Too short for oolong
        )
        assert oolong_rule(incorrect_oxidation) is False

        # Test green tea rule with oolong sequence (should fail due to oxidation)
        assert green_rule(oolong_tea_sequence) is False

        # Test black tea rule with oolong sequence (should fail due to wrong oxidation time)
        assert black_rule(oolong_tea_sequence) is False

        # Test with missing oxidation step for green tea
        green_sequence = [
            TeaProcess(TeaType.GREEN, ProcessingStep.PLUCKING),
            TeaProcess(TeaType.GREEN, ProcessingStep.WITHERING),
            TeaProcess(TeaType.GREEN, ProcessingStep.FIXING),
            TeaProcess(TeaType.GREEN, ProcessingStep.DRYING),
        ]
        assert green_rule(green_sequence) is True  # No oxidation is valid for green tea

        # Test with empty sequence
        assert oolong_rule([]) is False  # Empty sequence is invalid (no oxidation step)
        assert (
            green_rule([]) is True
        )  # Empty sequence is valid for green tea (no oxidation needed)

    def test_quality_rule(self, green_tea_sequence, quality_metrics):
        """Test that quality rule correctly validates quality metrics."""
        # Create a quality rule with minimum standards
        min_metrics = QualityMetrics(
            moisture_content=7.0,  # Higher is worse
            leaf_integrity=0.7,  # Higher is better
            color_value=20.0,  # Not used in rule
            aroma_intensity=0.6,  # Higher is better
            taste_profile={},  # Not used in rule
        )
        rule = create_quality_rule(min_metrics)

        # Add quality metrics to the sequence
        sequence_with_quality = list(green_tea_sequence)
        for i in range(len(sequence_with_quality)):
            step_value = sequence_with_quality[i]["step"]
            step = (
                ProcessingStep(step_value)
                if isinstance(step_value, str)
                else step_value
            )
            sequence_with_quality[i] = TeaProcess(
                TeaType.GREEN,
                step,
                temperature=sequence_with_quality[i]["temperature"],
                duration=sequence_with_quality[i]["duration"],
                humidity=sequence_with_quality[i]["humidity"],
                quality=quality_metrics,
            )

        # Test with valid quality
        assert rule(sequence_with_quality) is True

        # Test with poor quality (high moisture)
        poor_quality = list(sequence_with_quality)
        poor_metrics = QualityMetrics(
            moisture_content=8.0,  # Too high
            leaf_integrity=0.8,
            color_value=25.0,
            aroma_intensity=0.7,
            taste_profile={"sweetness": 0.6},
        )
        poor_quality[0] = TeaProcess(
            TeaType.GREEN, ProcessingStep.PLUCKING, quality=poor_metrics
        )
        assert rule(poor_quality) is False

        # Test with poor quality (low leaf integrity)
        poor_quality = list(sequence_with_quality)
        poor_metrics = QualityMetrics(
            moisture_content=5.0,
            leaf_integrity=0.6,  # Too low
            color_value=25.0,
            aroma_intensity=0.7,
            taste_profile={"sweetness": 0.6},
        )
        poor_quality[0] = TeaProcess(
            TeaType.GREEN, ProcessingStep.PLUCKING, quality=poor_metrics
        )
        assert rule(poor_quality) is False

        # Test with poor quality (low aroma)
        poor_quality = list(sequence_with_quality)
        poor_metrics = QualityMetrics(
            moisture_content=5.0,
            leaf_integrity=0.8,
            color_value=25.0,
            aroma_intensity=0.5,  # Too low
            taste_profile={"sweetness": 0.6},
        )
        poor_quality[0] = TeaProcess(
            TeaType.GREEN, ProcessingStep.PLUCKING, quality=poor_metrics
        )
        assert rule(poor_quality) is False

        # Test with no quality metrics
        assert rule(green_tea_sequence) is True  # No quality metrics is valid

        # Test with empty sequence
        assert rule([]) is True  # Empty sequence is valid by default

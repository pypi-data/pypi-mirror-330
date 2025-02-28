"""
Tea Processing Rules.

This module implements sequence rules for tea processing, with support for:
- Different tea types and their processing requirements
- Temperature and humidity controls
- Processing step durations and order
- Oxidation and fermentation levels
- Quality control parameters
- Regional variations

Common use cases:
- Validating traditional processing methods
- Ensuring quality control standards
- Managing tea factory workflows
- Documenting regional variations
- Training tea processors
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from ..core import AbstractObject, Sequence
from ..dsl import DSLRule


class TeaType(Enum):
    """Types of tea based on processing method."""

    GREEN = "green"  # Unoxidized
    WHITE = "white"  # Slightly oxidized
    YELLOW = "yellow"  # Slightly oxidized, unique withering
    OOLONG = "oolong"  # Partially oxidized
    BLACK = "black"  # Fully oxidized
    PUERH = "puerh"  # Post-fermented
    DARK = "dark"  # Post-fermented (non-puerh)


class ProcessingStep(Enum):
    """Steps in tea processing."""

    PLUCKING = "plucking"  # Leaf harvesting
    WITHERING = "withering"  # Moisture reduction
    BRUISING = "bruising"  # Cell disruption
    ROLLING = "rolling"  # Leaf shaping
    OXIDATION = "oxidation"  # Enzymatic browning
    FIXING = "fixing"  # Enzyme deactivation
    FERMENTATION = "fermentation"  # Microbial fermentation
    DRYING = "drying"  # Final moisture removal
    AGING = "aging"  # Post-processing aging


@dataclass
class QualityMetrics:
    """Quality control metrics for tea processing."""

    moisture_content: float  # Percentage
    leaf_integrity: float  # 0-1 scale
    color_value: float  # L*a*b* color space
    aroma_intensity: float  # 0-1 scale
    taste_profile: Dict[str, float]  # Flavor wheel values


class TeaProcess(AbstractObject):
    """
    A tea processing step with properties.

    Properties:
        tea_type: Type of tea being processed
        step: Processing step being performed
        temperature: Temperature in Celsius
        duration: Duration in hours
        humidity: Relative humidity percentage
        leaf_ratio: Leaf to water ratio (if applicable)
        quality: Quality metrics at this step
    """

    def __init__(
        self,
        tea_type: TeaType,
        step: ProcessingStep,
        temperature: Optional[float] = None,
        duration: Optional[float] = None,
        humidity: Optional[float] = None,
        leaf_ratio: Optional[float] = None,
        quality: Optional[QualityMetrics] = None,
    ):
        """Initialize a tea processing step."""
        if temperature is not None and temperature < 0:
            raise ValueError("Temperature cannot be negative")

        if duration is not None and duration < 0:
            raise ValueError("Duration cannot be negative")

        if humidity is not None and not (0 <= humidity <= 100):
            raise ValueError("Humidity must be between 0 and 100")

        if leaf_ratio is not None and leaf_ratio <= 0:
            raise ValueError("Leaf ratio must be positive")

        super().__init__(
            tea_type=tea_type.value,
            step=step.value,
            temperature=temperature,
            duration=duration,
            humidity=humidity,
            leaf_ratio=leaf_ratio,
            quality=quality,
        )

    def __repr__(self) -> str:
        return (
            f"TeaProcess({self['tea_type']}, {self['step']}, "
            f"temp={self['temperature']}°C, "
            f"duration={self['duration']}h)"
        )


def create_tea_sequence_rule(tea_type: TeaType) -> DSLRule:
    """
    Creates a rule enforcing the correct processing sequence for a tea type.

    Example:
        green_tea_sequence = create_tea_sequence_rule(TeaType.GREEN)
    """
    sequences = {
        TeaType.GREEN: [
            ProcessingStep.PLUCKING,
            ProcessingStep.WITHERING,
            ProcessingStep.FIXING,
            ProcessingStep.ROLLING,
            ProcessingStep.DRYING,
        ],
        TeaType.OOLONG: [
            ProcessingStep.PLUCKING,
            ProcessingStep.WITHERING,
            ProcessingStep.BRUISING,
            ProcessingStep.OXIDATION,
            ProcessingStep.FIXING,
            ProcessingStep.ROLLING,
            ProcessingStep.DRYING,
        ],
        TeaType.BLACK: [
            ProcessingStep.PLUCKING,
            ProcessingStep.WITHERING,
            ProcessingStep.ROLLING,
            ProcessingStep.OXIDATION,
            ProcessingStep.DRYING,
        ],
        TeaType.PUERH: [
            ProcessingStep.PLUCKING,
            ProcessingStep.WITHERING,
            ProcessingStep.FIXING,
            ProcessingStep.ROLLING,
            ProcessingStep.FERMENTATION,
            ProcessingStep.DRYING,
            ProcessingStep.AGING,
        ],
    }

    required_steps = sequences.get(tea_type, [])

    def check_sequence(seq: Sequence) -> bool:
        if not seq:
            return True

        # Check tea type consistency
        if not all(step["tea_type"] == tea_type.value for step in seq):
            return False

        # Extract steps in sequence
        steps = [ProcessingStep(step["step"]) for step in seq]

        # Check if steps appear in correct order
        current_idx = 0
        for step in steps:
            if step not in required_steps:
                return False
            step_idx = required_steps.index(step)
            if step_idx < current_idx:
                return False
            current_idx = step_idx
        return True

    return DSLRule(check_sequence, f"follows {tea_type.value} tea processing sequence")


def create_temperature_rule(
    step: ProcessingStep, min_temp: float, max_temp: float
) -> DSLRule:
    """
    Creates a rule enforcing temperature range for a processing step.

    Example:
        fixing_temp = create_temperature_rule(ProcessingStep.FIXING, 120, 140)
    """

    def check_temperature(seq: Sequence) -> bool:
        for process in seq:
            if (
                ProcessingStep(process["step"]) == step
                and process["temperature"] is not None
            ):
                temp = process["temperature"]
                if not (min_temp <= temp <= max_temp):
                    return False
        return True

    return DSLRule(
        check_temperature,
        f"{step.value} temperature between {min_temp}°C and {max_temp}°C",
    )


def create_humidity_rule(
    step: ProcessingStep, min_humidity: float, max_humidity: float
) -> DSLRule:
    """
    Creates a rule enforcing humidity range for a processing step.

    Example:
        withering_humidity = create_humidity_rule(ProcessingStep.WITHERING, 65, 75)
    """

    def check_humidity(seq: Sequence) -> bool:
        for process in seq:
            if (
                ProcessingStep(process["step"]) == step
                and process["humidity"] is not None
            ):
                humidity = process["humidity"]
                if not (min_humidity <= humidity <= max_humidity):
                    return False
        return True

    return DSLRule(
        check_humidity,
        f"{step.value} humidity between {min_humidity}% and {max_humidity}%",
    )


def create_duration_rule(
    step: ProcessingStep, min_hours: float, max_hours: float
) -> DSLRule:
    """
    Creates a rule enforcing duration range for a processing step.

    Example:
        oxidation_time = create_duration_rule(ProcessingStep.OXIDATION, 2, 4)
    """

    def check_duration(seq: Sequence) -> bool:
        for process in seq:
            if (
                ProcessingStep(process["step"]) == step
                and process["duration"] is not None
            ):
                duration = process["duration"]
                if not (min_hours <= duration <= max_hours):
                    return False
        return True

    return DSLRule(
        check_duration, f"{step.value} duration between {min_hours}h and {max_hours}h"
    )


def create_oxidation_level_rule(tea_type: TeaType) -> DSLRule:
    """
    Creates a rule enforcing proper oxidation level for a tea type.

    Example:
        oolong_oxidation = create_oxidation_level_rule(TeaType.OOLONG)
    """
    # Oxidation levels in hours
    oxidation_times = {
        TeaType.GREEN: 0,
        TeaType.WHITE: 0,
        TeaType.YELLOW: 0.75,
        TeaType.OOLONG: 3,
        TeaType.BLACK: 5,
    }

    target_time = oxidation_times.get(tea_type, 0)

    def check_oxidation(seq: Sequence) -> bool:
        has_oxidation = False
        for process in seq:
            if (
                ProcessingStep(process["step"]) == ProcessingStep.OXIDATION
                and process["duration"] is not None
            ):
                has_oxidation = True
                if abs(process["duration"] - target_time) > 0.5:
                    return False
        return not has_oxidation if target_time == 0 else has_oxidation

    return DSLRule(check_oxidation, f"{tea_type.value} tea oxidation level")


def create_quality_rule(min_metrics: QualityMetrics) -> DSLRule:
    """
    Creates a rule enforcing minimum quality metrics.

    Example:
        quality_standard = create_quality_rule(min_metrics)
    """

    def check_quality(seq: Sequence) -> bool:
        for process in seq:
            if process["quality"] is not None:
                quality = process["quality"]
                if (
                    quality.moisture_content > min_metrics.moisture_content
                    or quality.leaf_integrity < min_metrics.leaf_integrity
                    or quality.aroma_intensity < min_metrics.aroma_intensity
                ):
                    return False
        return True

    return DSLRule(check_quality, "meets minimum quality standards")


# Common processing rules
green_tea_rules = [
    create_tea_sequence_rule(TeaType.GREEN),
    create_temperature_rule(ProcessingStep.FIXING, 120, 140),
    create_humidity_rule(ProcessingStep.WITHERING, 65, 75),
    create_duration_rule(ProcessingStep.DRYING, 0.5, 1.5),
]

oolong_tea_rules = [
    create_tea_sequence_rule(TeaType.OOLONG),
    create_temperature_rule(ProcessingStep.OXIDATION, 25, 30),
    create_humidity_rule(ProcessingStep.OXIDATION, 75, 85),
    create_oxidation_level_rule(TeaType.OOLONG),
]

puerh_tea_rules = [
    create_tea_sequence_rule(TeaType.PUERH),
    create_temperature_rule(ProcessingStep.FERMENTATION, 25, 35),
    create_humidity_rule(ProcessingStep.FERMENTATION, 85, 95),
    create_duration_rule(ProcessingStep.AGING, 720, float("inf")),  # Minimum 30 days
]

# Example sequences
green_tea_sequence = [
    TeaProcess(TeaType.GREEN, ProcessingStep.PLUCKING),
    TeaProcess(
        TeaType.GREEN, ProcessingStep.WITHERING, temperature=25, duration=2, humidity=70
    ),
    TeaProcess(
        TeaType.GREEN, ProcessingStep.FIXING, temperature=130, duration=0.1
    ),  # 6 minutes
    TeaProcess(TeaType.GREEN, ProcessingStep.ROLLING, duration=0.25),  # 15 minutes
    TeaProcess(TeaType.GREEN, ProcessingStep.DRYING, temperature=80, duration=1),
]

oolong_tea_sequence = [
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
    TeaProcess(TeaType.OOLONG, ProcessingStep.FIXING, temperature=130, duration=0.1),
    TeaProcess(TeaType.OOLONG, ProcessingStep.ROLLING, duration=0.25),
    TeaProcess(TeaType.OOLONG, ProcessingStep.DRYING, temperature=85, duration=1),
]

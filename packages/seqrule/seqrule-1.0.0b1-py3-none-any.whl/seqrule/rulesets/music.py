"""
Musical sequence rules.

This module implements sequence rules for musical sequences, with support for:
- Melodic patterns and phrases
- Rhythmic patterns and time signatures
- Note types (melody, harmony, rest)
- Duration constraints
- Basic harmony rules
- Common musical forms

Common use cases:
- Validating melodic patterns
- Checking rhythmic consistency
- Ensuring proper phrase structure
- Managing voice leading
- Creating musical variations
"""

from enum import Enum
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Union

from ..core import AbstractObject, Sequence
from ..dsl import DSLRule, if_then_rule


class NoteType(Enum):
    """Types of musical notes."""

    MELODY = "melody"  # Main melodic line
    HARMONY = "harmony"  # Harmonic accompaniment
    REST = "rest"  # Musical rest
    BASS = "bass"  # Bass line
    PERCUSSION = "percussion"  # Rhythmic percussion


class TimeSignature:
    """Musical time signature (e.g., 4/4, 3/4, 6/8)."""

    def __init__(self, beats: int, beat_unit: int):
        """
        Initialize a time signature.

        Args:
            beats: Number of beats per measure
            beat_unit: Note value of one beat (4 = quarter, 8 = eighth, etc.)
        """
        self.beats = beats
        self.beat_unit = beat_unit
        # Convert to quarter notes: multiply by 4/beat_unit to get quarter note duration
        self.measure_duration = Fraction(
            beats * 4, beat_unit
        )  # Duration in quarter notes

    def __repr__(self) -> str:
        return f"{self.beats}/{self.beat_unit}"


class Note(AbstractObject):
    """
    A musical note with properties.

    Properties:
        pitch: Note pitch (e.g., "C4", "F#5", "rest")
        duration: Duration in quarter notes (1.0 = quarter, 0.5 = eighth)
        note_type: Type of note (melody, harmony, rest, etc.)
        velocity: Note velocity/volume (0-127, MIDI standard)
        measure: Measure number in the sequence
        beat: Beat position within the measure
    """

    def __init__(
        self,
        pitch: str,
        duration: float,
        note_type: Union[str, NoteType],
        velocity: int = 64,
        measure: Optional[int] = None,
        beat: Optional[float] = None,
    ):
        """Initialize a note with its properties."""
        if isinstance(note_type, str):
            note_type = NoteType(note_type)

        if not (0 <= velocity <= 127):
            raise ValueError("Velocity must be between 0 and 127")

        if duration <= 0:
            raise ValueError("Duration must be positive")

        super().__init__(
            pitch=pitch,
            duration=float(duration),
            note_type=note_type.value,
            velocity=velocity,
            measure=measure,
            beat=float(beat) if beat is not None else None,
        )

    def __repr__(self) -> str:
        return (
            f"Note(pitch={self['pitch']}, "
            f"duration={self['duration']}, "
            f"type={self['note_type']})"
        )


def note_type_is(note_type: Union[str, NoteType]) -> Callable[[AbstractObject], bool]:
    """Creates a predicate that checks if a note has a specific type."""
    if isinstance(note_type, str):
        note_type = NoteType(note_type)
    return lambda obj: obj["note_type"] == note_type.value


def note_pitch_is(pitch: str) -> Callable[[AbstractObject], bool]:
    """Creates a predicate that checks if a note has a specific pitch."""
    return lambda obj: obj["pitch"] == pitch


def note_duration_is(duration: float) -> Callable[[AbstractObject], bool]:
    """Creates a predicate that checks if a note has a specific duration."""
    return lambda obj: obj["duration"] == duration


# Basic rules
rest_followed_by_melody = if_then_rule(
    note_type_is(NoteType.REST), note_type_is(NoteType.MELODY)
)


def create_rhythm_pattern_rule(
    durations: List[float], allow_consolidation: bool = False
) -> DSLRule:
    """
    Creates a rule requiring notes to follow a specific rhythm pattern.

    Args:
        durations: List of note durations (in quarter notes)
        allow_consolidation: Whether to allow combining consecutive notes

    Example:
        waltz = create_rhythm_pattern_rule([1.0, 0.5, 0.5])  # Basic waltz pattern
    """

    def check_rhythm(seq: Sequence) -> bool:
        if not seq:
            return True

        # Extract durations from sequence
        seq_durations = [note["duration"] for note in seq]

        if not allow_consolidation:
            if len(seq_durations) != len(durations):
                return False
            return all(sd == d for sd, d in zip(seq_durations, durations))

        # Check if sequence can be consolidated to match pattern
        total = 0
        pattern_idx = 0
        for duration in seq_durations:
            total += duration
            if total == durations[pattern_idx]:
                total = 0
                pattern_idx += 1
                if pattern_idx >= len(durations):
                    pattern_idx = 0
            elif total > durations[pattern_idx]:
                return False
        return total == 0  # All durations must be fully consumed

    return DSLRule(check_rhythm, f"matches rhythm pattern {durations}")


def create_melody_pattern_rule(pitches: List[str], transpose: bool = False) -> DSLRule:
    """
    Creates a rule requiring melody notes to follow a specific pitch pattern.

    Args:
        pitches: List of note pitches
        transpose: Whether to allow transposed versions of the pattern

    Example:
        motif = create_melody_pattern_rule(["C4", "E4", "G4"])  # C major arpeggio
    """

    def get_intervals(notes: List[str]) -> List[int]:
        """Convert pitch sequence to intervals."""
        if not notes or len(notes) < 2:
            return []
        base = get_semitones(notes[0])
        return [get_semitones(n) - base for n in notes[1:]]

    def get_semitones(note: str) -> int:
        """Convert note to semitone number (C4 = 60, etc.)."""
        if note == "rest":
            return -1

        # Extract pitch class and octave
        pitch_class = note[0].upper()

        # Handle accidentals properly
        accidental = 0
        if "#" in note:
            # Count number of sharps
            accidental = note.count("#")
        elif "b" in note:
            # Count number of flats (negative)
            accidental = -note.count("b")

        # Extract octave (last character)
        octave = int(note[-1])

        # Base semitones for each pitch class
        base = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        return base[pitch_class] + accidental + (octave + 1) * 12

    # Pre-calculate pattern intervals for transposition check
    pattern_melody = [p for p in pitches if p != "rest"]
    pattern_intervals = get_intervals(pattern_melody)

    def check_melody(seq: Sequence) -> bool:
        # Extract all notes in sequence
        all_notes = []
        for note in seq:
            if note["note_type"] == NoteType.MELODY.value:
                all_notes.append(note["pitch"])
            elif note["note_type"] == NoteType.REST.value:
                all_notes.append("rest")

        if len(all_notes) != len(pitches):
            return False

        if not transpose:
            return all(n == p for n, p in zip(all_notes, pitches))

        # Check if intervals match when transposed (ignoring rests)
        melody_notes = [n for n in all_notes if n != "rest"]
        if (
            not melody_notes
            or len(melody_notes) < 2
            or not pattern_melody
            or len(pattern_melody) < 2
        ):
            # If not enough notes to form intervals, check direct equality
            return all(n == p for n, p in zip(all_notes, pitches))

        # Calculate intervals for the sequence
        seq_intervals = get_intervals(melody_notes)

        # For transposition, we only care about the interval pattern, not the absolute pitches
        return seq_intervals == pattern_intervals

    return DSLRule(check_melody, f"melody matches pitch pattern {pitches}")


def create_measure_rule(time_sig: TimeSignature) -> DSLRule:
    """
    Creates a rule ensuring notes fit properly in measures.

    Example:
        common_time = create_measure_rule(TimeSignature(4, 4))
    """

    def check_measures(seq: Sequence) -> bool:
        if not seq:
            return True

        # Group notes by measure
        measures: Dict[int, List[AbstractObject]] = {}
        for note in seq:
            measure = note["measure"]
            if measure is None:
                return False
            if measure not in measures:
                measures[measure] = []
            measures[measure].append(note)

        # Check each measure's duration
        for measure_notes in measures.values():
            total = sum(note["duration"] for note in measure_notes)
            if total != time_sig.measure_duration:
                return False
        return True

    return DSLRule(check_measures, f"notes fit in {time_sig} measures")


def create_total_duration_rule(target: float, tolerance: float = 0.001) -> DSLRule:
    """
    Creates a rule requiring the total duration to match a target value.

    Example:
        eight_bars = create_total_duration_rule(32.0)  # 8 measures in 4/4
    """

    def check_total_duration(seq: Sequence) -> bool:
        total = sum(note["duration"] for note in seq)
        return abs(total - target) <= tolerance

    return DSLRule(check_total_duration, f"total duration = {target} ± {tolerance}")


def create_max_consecutive_rule(
    note_type: Union[str, NoteType], max_count: int
) -> DSLRule:
    """
    Creates a rule limiting the number of consecutive notes of a specific type.

    Example:
        max_rests = create_max_consecutive_rule(NoteType.REST, 2)
    """
    if isinstance(note_type, str):
        note_type = NoteType(note_type)

    def check_consecutive(seq: Sequence) -> bool:
        count = 0
        for note in seq:
            if note["note_type"] == note_type.value:
                count += 1
                if count > max_count:
                    return False
            else:
                count = 0
        return True

    return DSLRule(
        check_consecutive, f"at most {max_count} consecutive {note_type.value} notes"
    )


# Common musical patterns
basic_waltz = create_rhythm_pattern_rule([1.0, 0.5, 0.5])  # ONE-two-three
basic_march = create_rhythm_pattern_rule([1.0, 1.0])  # LEFT-right
swing_rhythm = create_rhythm_pattern_rule([0.66, 0.33])  # Long-short swing

# Example sequences
waltz_pattern = [
    Note("C4", 1.0, NoteType.MELODY, measure=1, beat=1),  # ONE
    Note("G3", 0.5, NoteType.HARMONY, measure=1, beat=2),  # two
    Note("E3", 0.5, NoteType.HARMONY, measure=1, beat=2.5),  # three
]

melody_with_rest = [
    Note("C4", 1.0, NoteType.MELODY),
    Note("rest", 0.5, NoteType.REST),
    Note("E4", 0.5, NoteType.MELODY),
]

c_major_scale = [
    Note(pitch, 0.25, NoteType.MELODY)
    for pitch in ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
]

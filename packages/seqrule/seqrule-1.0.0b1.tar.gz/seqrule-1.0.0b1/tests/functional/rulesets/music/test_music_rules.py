"""
Tests for the music ruleset.

These tests verify that the music rule factories create rules
that correctly validate sequences of musical notes.
"""

import pytest

from seqrule.dsl import if_then_rule
from seqrule.rulesets.music import (
    Note,
    NoteType,
    TimeSignature,
    create_max_consecutive_rule,
    create_measure_rule,
    create_melody_pattern_rule,
    create_rhythm_pattern_rule,
    create_total_duration_rule,
    note_duration_is,
    note_pitch_is,
    note_type_is,
)


class TestMusicRules:
    """Test suite for music rules."""

    def test_note_initialization(self):
        """Test that Note objects can be properly initialized."""
        # Basic note initialization
        note = Note("C4", 1.0, NoteType.MELODY, velocity=80, measure=1, beat=1.0)
        assert note["pitch"] == "C4"
        assert note["duration"] == 1.0
        assert note["note_type"] == "melody"
        assert note["velocity"] == 80
        assert note["measure"] == 1
        assert note["beat"] == 1.0

        # Initialize with string note type
        note = Note("D4", 0.5, "harmony")
        assert note["note_type"] == "harmony"

        # Test invalid velocity
        with pytest.raises(ValueError):
            Note("C4", 1.0, NoteType.MELODY, velocity=128)

        # Test invalid duration
        with pytest.raises(ValueError):
            Note("C4", 0, NoteType.MELODY)

    def test_time_signature(self):
        """Test that TimeSignature objects can be properly initialized."""
        # Common time (4/4)
        ts = TimeSignature(4, 4)
        assert ts.beats == 4
        assert ts.beat_unit == 4
        assert ts.measure_duration == 4.0  # 4 quarter notes

        # Waltz time (3/4)
        ts = TimeSignature(3, 4)
        assert ts.beats == 3
        assert ts.beat_unit == 4
        assert ts.measure_duration == 3.0  # 3 quarter notes

        # Compound time (6/8)
        ts = TimeSignature(6, 8)
        assert ts.beats == 6
        assert ts.beat_unit == 8
        assert ts.measure_duration == 3.0  # 6 eighth notes = 3 quarter notes

    def test_note_predicates(self):
        """Test the note predicate functions."""
        # Create test notes
        melody_note = Note("C4", 1.0, NoteType.MELODY)
        harmony_note = Note("G3", 0.5, NoteType.HARMONY)

        # Test note_type_is
        is_melody = note_type_is(NoteType.MELODY)
        is_harmony = note_type_is("harmony")

        assert is_melody(melody_note) is True
        assert is_melody(harmony_note) is False
        assert is_harmony(harmony_note) is True
        assert is_harmony(melody_note) is False

        # Test note_pitch_is
        is_c4 = note_pitch_is("C4")
        is_g3 = note_pitch_is("G3")

        assert is_c4(melody_note) is True
        assert is_c4(harmony_note) is False
        assert is_g3(harmony_note) is True
        assert is_g3(melody_note) is False

        # Test note_duration_is
        is_quarter = note_duration_is(1.0)
        is_eighth = note_duration_is(0.5)

        assert is_quarter(melody_note) is True
        assert is_quarter(harmony_note) is False
        assert is_eighth(harmony_note) is True
        assert is_eighth(melody_note) is False

    def test_rhythm_pattern_rule(self):
        """Test that rhythm pattern rule correctly validates rhythmic patterns."""
        # Create a rule for a basic waltz pattern (quarter, eighth, eighth)
        waltz_rule = create_rhythm_pattern_rule([1.0, 0.5, 0.5])

        # Valid waltz pattern
        valid_waltz = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("G3", 0.5, NoteType.HARMONY),
            Note("E3", 0.5, NoteType.HARMONY),
        ]
        assert waltz_rule(valid_waltz) is True

        # Invalid rhythm pattern
        invalid_rhythm = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("G3", 1.0, NoteType.HARMONY),  # Should be 0.5
            Note("E3", 0.5, NoteType.HARMONY),
        ]
        assert waltz_rule(invalid_rhythm) is False

        # Test with allow_consolidation=True
        consolidated_rule = create_rhythm_pattern_rule(
            [1.0, 0.5, 0.5], allow_consolidation=True
        )

        # Consolidated notes that match the pattern when consolidated
        # The pattern is [1.0, 0.5, 0.5] and we're providing [1.0, 1.0]
        # where the second 1.0 represents the consolidated 0.5 + 0.5
        consolidated_notes = [
            Note("C4", 1.0, NoteType.MELODY),  # Matches first 1.0
            Note("G3", 0.5, NoteType.HARMONY),  # Matches first 0.5
            Note("E3", 0.5, NoteType.HARMONY),  # Matches second 0.5
        ]
        assert consolidated_rule(consolidated_notes) is True

        # Another valid consolidated pattern
        another_consolidated = [
            Note("C4", 1.0, NoteType.MELODY),  # Matches first 1.0
            Note("G3", 0.25, NoteType.HARMONY),  # Part of first 0.5
            Note("E3", 0.25, NoteType.HARMONY),  # Part of first 0.5
            Note("D4", 0.5, NoteType.MELODY),  # Matches second 0.5
        ]
        assert consolidated_rule(another_consolidated) is True

        # Empty sequence should pass
        assert waltz_rule([]) is True

    def test_melody_pattern_rule(self):
        """Test that melody pattern rule correctly validates melodic patterns."""
        # Create a rule for a C major triad
        c_major_rule = create_melody_pattern_rule(["C4", "E4", "G4"])

        # Valid C major triad
        valid_triad = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("G4", 1.0, NoteType.MELODY),
        ]
        assert c_major_rule(valid_triad) is True

        # Invalid melody
        invalid_melody = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("F4", 1.0, NoteType.MELODY),  # Should be E4
            Note("G4", 1.0, NoteType.MELODY),
        ]
        assert c_major_rule(invalid_melody) is False

        # Test with transpose=True
        transposable_rule = create_melody_pattern_rule(
            ["C4", "E4", "G4"], transpose=True
        )

        # Transposed to D major
        d_major_triad = [
            Note("D4", 1.0, NoteType.MELODY),
            Note("F#4", 1.0, NoteType.MELODY),
            Note("A4", 1.0, NoteType.MELODY),
        ]
        assert transposable_rule(d_major_triad) is True

        # Test with rests
        melody_with_rest_rule = create_melody_pattern_rule(["C4", "rest", "E4"])

        # Valid melody with rest
        valid_with_rest = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("E4", 0.5, NoteType.MELODY),
        ]
        assert melody_with_rest_rule(valid_with_rest) is True

    def test_measure_rule(self):
        """Test that measure rule correctly validates measure structure."""
        # Create a rule for 4/4 time
        common_time_rule = create_measure_rule(TimeSignature(4, 4))

        # Valid 4/4 measure
        valid_measure = [
            Note("C4", 1.0, NoteType.MELODY, measure=1, beat=1.0),
            Note("D4", 1.0, NoteType.MELODY, measure=1, beat=2.0),
            Note("E4", 1.0, NoteType.MELODY, measure=1, beat=3.0),
            Note("F4", 1.0, NoteType.MELODY, measure=1, beat=4.0),
        ]
        assert common_time_rule(valid_measure) is True

        # Invalid measure (too many beats)
        invalid_measure = [
            Note("C4", 1.0, NoteType.MELODY, measure=1, beat=1.0),
            Note("D4", 1.0, NoteType.MELODY, measure=1, beat=2.0),
            Note("E4", 1.0, NoteType.MELODY, measure=1, beat=3.0),
            Note("F4", 1.0, NoteType.MELODY, measure=1, beat=4.0),
            Note("G4", 1.0, NoteType.MELODY, measure=1, beat=5.0),  # Extra beat
        ]
        assert common_time_rule(invalid_measure) is False

        # Test with multiple measures
        multi_measure = [
            Note("C4", 1.0, NoteType.MELODY, measure=1, beat=1.0),
            Note("D4", 1.0, NoteType.MELODY, measure=1, beat=2.0),
            Note("E4", 1.0, NoteType.MELODY, measure=1, beat=3.0),
            Note("F4", 1.0, NoteType.MELODY, measure=1, beat=4.0),
            Note("G4", 1.0, NoteType.MELODY, measure=2, beat=1.0),
            Note("A4", 1.0, NoteType.MELODY, measure=2, beat=2.0),
            Note("B4", 1.0, NoteType.MELODY, measure=2, beat=3.0),
            Note("C5", 1.0, NoteType.MELODY, measure=2, beat=4.0),
        ]
        assert common_time_rule(multi_measure) is True

        # Test with missing measure information
        missing_measure = [Note("C4", 1.0, NoteType.MELODY)]  # No measure specified
        assert common_time_rule(missing_measure) is False

    def test_total_duration_rule(self):
        """Test that total duration rule correctly validates sequence duration."""
        # Create a rule requiring exactly 4 beats
        four_beat_rule = create_total_duration_rule(4.0)

        # Valid 4-beat sequence
        valid_duration = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("D4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("F4", 1.0, NoteType.MELODY),
        ]
        assert four_beat_rule(valid_duration) is True

        # Invalid duration (too long)
        too_long = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("D4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("F4", 1.0, NoteType.MELODY),
            Note("G4", 1.0, NoteType.MELODY),  # Extra note
        ]
        assert four_beat_rule(too_long) is False

        # Test with tolerance
        approx_rule = create_total_duration_rule(4.0, tolerance=0.1)

        # Slightly off duration (within tolerance)
        slightly_off = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("D4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("F4", 1.05, NoteType.MELODY),  # Slightly longer
        ]
        assert approx_rule(slightly_off) is True

    def test_max_consecutive_rule(self):
        """Test that max consecutive rule correctly limits consecutive notes of a type."""
        # Create a rule allowing at most 2 consecutive rests
        max_rests_rule = create_max_consecutive_rule(NoteType.REST, 2)

        # Valid sequence (2 consecutive rests)
        valid_rests = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("rest", 0.5, NoteType.REST),
            Note("E4", 1.0, NoteType.MELODY),
        ]
        assert max_rests_rule(valid_rests) is True

        # Invalid sequence (3 consecutive rests)
        invalid_rests = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("rest", 0.5, NoteType.REST),
            Note("rest", 0.5, NoteType.REST),  # One too many
            Note("E4", 1.0, NoteType.MELODY),
        ]
        assert max_rests_rule(invalid_rests) is False

        # Test with string note type
        max_melody_rule = create_max_consecutive_rule("melody", 3)

        # Valid sequence (3 consecutive melody notes)
        valid_melody = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("D4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("F4", 1.0, NoteType.MELODY),
        ]
        assert max_melody_rule(valid_melody) is True

        # Invalid sequence (4 consecutive melody notes)
        invalid_melody = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("D4", 1.0, NoteType.MELODY),
            Note("E4", 1.0, NoteType.MELODY),
            Note("F4", 1.0, NoteType.MELODY),  # One too many
            Note("rest", 0.5, NoteType.REST),
        ]
        assert max_melody_rule(invalid_melody) is False

    def test_if_then_rule(self):
        """Test that if-then rules work correctly with musical notes."""
        # Create a rule: if a note is a rest, the next note must be a melody note
        rest_then_melody = if_then_rule(
            note_type_is(NoteType.REST), note_type_is(NoteType.MELODY)
        )

        # Valid sequence (rest followed by melody)
        valid_sequence = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("E4", 1.0, NoteType.MELODY),
        ]
        assert rest_then_melody(valid_sequence) is True

        # Invalid sequence (rest followed by harmony)
        invalid_sequence = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
            Note("G3", 1.0, NoteType.HARMONY),  # Should be melody
        ]
        assert rest_then_melody(invalid_sequence) is False

        # Edge case: rest at the end (should pass as there's no "then" to check)
        rest_at_end = [
            Note("C4", 1.0, NoteType.MELODY),
            Note("rest", 0.5, NoteType.REST),
        ]
        assert rest_then_melody(rest_at_end) is True

import unittest

from seqrule.core import AbstractObject
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
    rest_followed_by_melody,
)


class TestMusicCoverage(unittest.TestCase):
    """Test cases to improve coverage for music.py."""

    def test_rhythm_pattern_rule_with_consolidation(self):
        """Test create_rhythm_pattern_rule with consolidation of durations."""
        # Create a rhythm pattern
        pattern = [1, 2, 1]

        # Create a rule that checks if a sequence follows the rhythm pattern
        rule = create_rhythm_pattern_rule(pattern, True)

        # Create notes with durations that match the pattern when consolidated
        notes = [
            AbstractObject(duration=0.5),
            AbstractObject(duration=0.5),  # 0.5 + 0.5 = 1
            AbstractObject(duration=2),  # 2
            AbstractObject(duration=1),  # 1
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with durations that don't match the pattern even when consolidated
        notes = [
            AbstractObject(duration=0.5),
            AbstractObject(duration=1),  # 0.5 + 1 = 1.5, not 1
            AbstractObject(duration=2),  # 2
            AbstractObject(duration=1),  # 1
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_rhythm_pattern_rule_without_consolidation(self):
        """Test rhythm_pattern_rule without consolidation."""
        # Create a rule that checks if a sequence follows a rhythm pattern
        durations = [1, 2, 1]
        rule = create_rhythm_pattern_rule(durations, allow_consolidation=False)

        # Create a sequence that follows the pattern
        seq = [
            AbstractObject(duration=1),
            AbstractObject(duration=2),
            AbstractObject(duration=1),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with different length
        seq = [AbstractObject(duration=1), AbstractObject(duration=2)]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_rhythm_pattern_rule_with_empty_sequence(self):
        """Test create_rhythm_pattern_rule with an empty sequence."""
        # Create a rhythm pattern
        pattern = [1, 2, 1]

        # Create a rule that checks if a sequence follows the rhythm pattern
        rule = create_rhythm_pattern_rule(pattern, True)

        # Create an empty sequence
        notes = []

        # Check that an empty sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Test with non-consolidation as well
        rule = create_rhythm_pattern_rule(pattern, False)
        result = rule(notes)
        self.assertTrue(result)

    def test_melody_pattern_rule(self):
        """Test create_melody_pattern_rule with various inputs."""
        # Create a melody pattern
        pattern = ["C4", "D4", "E4"]

        # Create a rule that checks if a sequence follows the melody pattern
        rule = create_melody_pattern_rule(pattern)

        # Create notes with pitches that match the pattern
        notes = [
            AbstractObject(pitch="C4", note_type="melody"),
            AbstractObject(pitch="D4", note_type="melody"),
            AbstractObject(pitch="E4", note_type="melody"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with pitches that don't match the pattern
        notes = [
            AbstractObject(pitch="C4", note_type="melody"),
            AbstractObject(pitch="E4", note_type="melody"),  # Should be D4
            AbstractObject(pitch="E4", note_type="melody"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_time_signature(self):
        """Test TimeSignature class."""
        # Create a time signature
        time_sig = TimeSignature(4, 4)  # 4/4 time

        # Check the properties
        self.assertEqual(time_sig.beats, 4)
        self.assertEqual(time_sig.beat_unit, 4)
        self.assertEqual(time_sig.measure_duration, 4)  # 4 quarter notes

        # Create another time signature
        time_sig = TimeSignature(3, 4)  # 3/4 time

        # Check the properties
        self.assertEqual(time_sig.beats, 3)
        self.assertEqual(time_sig.beat_unit, 4)
        self.assertEqual(time_sig.measure_duration, 3)  # 3 quarter notes

    def test_measure_rule(self):
        """Test create_measure_rule with various inputs."""
        # Create a time signature
        time_sig = TimeSignature(4, 4)  # 4/4 time

        # Create a rule that checks if measures have the correct duration
        rule = create_measure_rule(time_sig)

        # Create notes with correct measure durations
        notes = [
            AbstractObject(duration=2, measure=1),
            AbstractObject(duration=2, measure=1),  # Measure 1: 2 + 2 = 4
            AbstractObject(duration=1, measure=2),
            AbstractObject(duration=1, measure=2),
            AbstractObject(duration=2, measure=2),  # Measure 2: 1 + 1 + 2 = 4
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with incorrect measure durations
        notes = [
            AbstractObject(duration=2, measure=1),
            AbstractObject(duration=1, measure=1),  # Measure 1: 2 + 1 = 3, not 4
            AbstractObject(duration=4, measure=2),  # Measure 2: 4, correct
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_total_duration_rule(self):
        """Test create_total_duration_rule with various inputs."""
        # Create a rule that checks if the total duration matches a target
        rule = create_total_duration_rule(4.0, 0.1)  # Target: 4.0 with tolerance 0.1

        # Create notes with a total duration that matches the target
        notes = [
            AbstractObject(duration=1.0),
            AbstractObject(duration=1.0),
            AbstractObject(duration=2.0),  # Total: 1 + 1 + 2 = 4
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with a total duration that's within tolerance
        notes = [
            AbstractObject(duration=1.0),
            AbstractObject(duration=1.0),
            AbstractObject(
                duration=2.05
            ),  # Total: 1 + 1 + 2.05 = 4.05 (within tolerance)
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with a total duration that's outside tolerance
        notes = [
            AbstractObject(duration=1.0),
            AbstractObject(duration=1.0),
            AbstractObject(
                duration=2.2
            ),  # Total: 1 + 1 + 2.2 = 4.2 (outside tolerance)
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_max_consecutive_rule(self):
        """Test create_max_consecutive_rule with various inputs."""
        # Create a rule that limits consecutive rests
        rule = create_max_consecutive_rule("rest", 2)  # Max 2 consecutive rests

        # Create notes with acceptable consecutive rests
        notes = [
            AbstractObject(note_type="melody"),
            AbstractObject(note_type="rest"),
            AbstractObject(note_type="rest"),  # 2 consecutive rests
            AbstractObject(note_type="melody"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with too many consecutive rests
        notes = [
            AbstractObject(note_type="melody"),
            AbstractObject(note_type="rest"),
            AbstractObject(note_type="rest"),
            AbstractObject(note_type="rest"),  # 3 consecutive rests
            AbstractObject(note_type="melody"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_melody_pattern_rule_with_transposition(self):
        """Test create_melody_pattern_rule with transposition."""
        # Create a melody pattern
        pattern = ["C4", "E4", "G4"]  # C major triad

        # Create a rule that checks if a sequence follows the melody pattern with transposition
        rule = create_melody_pattern_rule(pattern, transpose=True)

        # Create notes with pitches that match the pattern when transposed (D major triad)
        notes = [
            AbstractObject(pitch="D4", note_type="melody"),
            AbstractObject(pitch="F#4", note_type="melody"),
            AbstractObject(pitch="A4", note_type="melody"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create notes with pitches that don't match the pattern even when transposed
        notes = [
            AbstractObject(pitch="D4", note_type="melody"),
            AbstractObject(
                pitch="F4", note_type="melody"
            ),  # Should be F#4 for D major triad
            AbstractObject(pitch="A4", note_type="melody"),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(notes)
        self.assertFalse(result)

    def test_melody_pattern_rule_with_rests(self):
        """Test melody_pattern_rule with rests."""
        # Create a rule that checks if a sequence follows a melody pattern
        pitches = ["C4", "rest", "G4"]
        rule = create_melody_pattern_rule(pitches, transpose=False)

        # Create a sequence that follows the pattern
        seq = [
            AbstractObject(note_type=NoteType.MELODY.value, pitch="C4"),
            AbstractObject(note_type=NoteType.REST.value),
            AbstractObject(note_type=NoteType.MELODY.value, pitch="G4"),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with different length
        seq = [
            AbstractObject(note_type=NoteType.MELODY.value, pitch="C4"),
            AbstractObject(note_type=NoteType.REST.value),
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

        # Test with all rests
        pitches = ["rest", "rest", "rest"]
        rule = create_melody_pattern_rule(pitches, transpose=True)

        seq = [
            AbstractObject(note_type=NoteType.REST.value),
            AbstractObject(note_type=NoteType.REST.value),
            AbstractObject(note_type=NoteType.REST.value),
        ]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

    def test_measure_rule_empty_sequence(self):
        """Test measure_rule with an empty sequence."""
        # Create a rule that checks if notes fit properly in measures
        time_sig = TimeSignature(4, 4)
        rule = create_measure_rule(time_sig)

        # Check that an empty sequence satisfies the rule
        result = rule([])
        self.assertTrue(result)

    def test_measure_rule_with_missing_measure(self):
        """Test measure_rule with notes missing measure property."""
        # Create a rule that checks if notes fit properly in measures
        time_sig = TimeSignature(4, 4)
        rule = create_measure_rule(time_sig)

        # Create a sequence with a note missing measure property
        seq = [
            AbstractObject(measure=1, beat=1, duration=1),
            AbstractObject(beat=2, duration=1),  # Missing measure
        ]

        # Check that the sequence does not satisfy the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_note_constructor(self):
        """Test Note constructor with various inputs."""
        # Create a note with valid parameters
        note = Note(
            pitch="C4",
            duration=1.0,
            note_type="melody",
            velocity=64,
            measure=1,
            beat=1.0,
        )

        # Check the properties
        self.assertEqual(note["pitch"], "C4")
        self.assertEqual(note["duration"], 1.0)
        self.assertEqual(note["note_type"], "melody")
        self.assertEqual(note["velocity"], 64)
        self.assertEqual(note["measure"], 1)
        self.assertEqual(note["beat"], 1.0)

        # Test with NoteType enum
        note = Note(pitch="D4", duration=0.5, note_type=NoteType.HARMONY, velocity=80)

        # Check the properties
        self.assertEqual(note["pitch"], "D4")
        self.assertEqual(note["duration"], 0.5)
        self.assertEqual(note["note_type"], "harmony")
        self.assertEqual(note["velocity"], 80)

        # Test with invalid velocity
        with self.assertRaises(ValueError):
            Note(
                pitch="C4",
                duration=1.0,
                note_type="melody",
                velocity=128,  # Invalid: should be 0-127
            )

        # Test with invalid duration
        with self.assertRaises(ValueError):
            Note(
                pitch="C4",
                duration=0,  # Invalid: should be positive
                note_type="melody",
            )

    def test_melody_pattern_rule_with_accidentals(self):
        """Test melody_pattern_rule with notes containing accidentals (sharps and flats)."""
        # Create a rule that checks if a sequence follows a melody pattern with accidentals
        pattern = ["C4", "D#4", "Eb4"]  # Pattern with sharp and flat
        rule = create_melody_pattern_rule(pattern, transpose=False)

        # Create notes with pitches that match the pattern
        notes = [
            AbstractObject(pitch="C4", note_type="melody"),
            AbstractObject(pitch="D#4", note_type="melody"),  # Note with sharp
            AbstractObject(pitch="Eb4", note_type="melody"),  # Note with flat
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

        # Create a pattern with only accidentals
        pattern = ["C#4", "F#4", "Bb4"]
        rule = create_melody_pattern_rule(pattern, transpose=True)

        # Create notes with pitches that match the pattern when transposed
        # The intervals in the original pattern are:
        # C#4 to F#4: 5 semitones (perfect fourth)
        # C#4 to Bb4: 9 semitones (major sixth)
        # So we need to create a sequence with the same intervals
        notes = [
            AbstractObject(pitch="D#4", note_type="melody"),  # Starting note
            AbstractObject(pitch="G#4", note_type="melody"),  # D#4 + 5 semitones = G#4
            AbstractObject(pitch="C5", note_type="melody"),  # D#4 + 9 semitones = C5
        ]

        # Check that the sequence satisfies the rule
        result = rule(notes)
        self.assertTrue(result)

    def test_note_predicates(self):
        """Test the note predicate functions."""
        # Test note_type_is with string
        is_melody = note_type_is("melody")
        melody_note = AbstractObject(note_type="melody")
        rest_note = AbstractObject(note_type="rest")
        self.assertTrue(is_melody(melody_note))
        self.assertFalse(is_melody(rest_note))

        # Test note_type_is with enum
        is_harmony = note_type_is(NoteType.HARMONY)
        harmony_note = AbstractObject(note_type="harmony")
        self.assertTrue(is_harmony(harmony_note))
        self.assertFalse(is_harmony(melody_note))

        # Test note_pitch_is
        is_c4 = note_pitch_is("C4")
        c4_note = AbstractObject(pitch="C4")
        d4_note = AbstractObject(pitch="D4")
        self.assertTrue(is_c4(c4_note))
        self.assertFalse(is_c4(d4_note))

        # Test note_duration_is
        is_quarter = note_duration_is(1.0)
        quarter_note = AbstractObject(duration=1.0)
        eighth_note = AbstractObject(duration=0.5)
        self.assertTrue(is_quarter(quarter_note))
        self.assertFalse(is_quarter(eighth_note))

    def test_rest_followed_by_melody_rule(self):
        """Test the rest_followed_by_melody rule."""
        # Create a sequence that follows the rule
        seq = [AbstractObject(note_type="rest"), AbstractObject(note_type="melody")]

        # Check that the sequence satisfies the rule
        result = rest_followed_by_melody(seq)
        self.assertTrue(result)

        # Create a sequence that doesn't follow the rule
        seq = [AbstractObject(note_type="rest"), AbstractObject(note_type="rest")]

        # Check that the sequence does not satisfy the rule
        result = rest_followed_by_melody(seq)
        self.assertFalse(result)

        # Create a sequence with only one note
        # For if_then_rule, a sequence with only one element always returns True
        # because there are no adjacent pairs to check
        seq = [AbstractObject(note_type="rest")]

        # Check that the sequence satisfies the rule (vacuously true)
        result = rest_followed_by_melody(seq)
        self.assertTrue(result)

        # Create a sequence where the rule doesn't apply
        seq = [AbstractObject(note_type="melody"), AbstractObject(note_type="rest")]

        # Check that the sequence satisfies the rule (condition not met)
        result = rest_followed_by_melody(seq)
        self.assertTrue(result)

    def test_melody_pattern_rule_with_invalid_pitch(self):
        """Test melody_pattern_rule with an invalid pitch class."""
        # Create a melody pattern with a valid pitch
        pattern = ["C4"]
        rule = create_melody_pattern_rule(pattern, transpose=False)

        # Create a sequence with a note that has an invalid pitch class
        # This will test the code path in the get_semitones function
        # when it encounters a pitch class that's not in the standard pitch classes
        notes = [AbstractObject(pitch="X4", note_type="melody")]

        # The function should handle the invalid pitch class without raising an exception
        # but the rule should fail because the pattern doesn't match
        result = rule(notes)
        self.assertFalse(result)

    def test_note_type_is_with_string_and_enum(self):
        """Test note_type_is with both string and enum parameters."""
        # Test with string parameter
        is_melody_str = note_type_is("melody")
        melody_note = AbstractObject(note_type="melody")
        self.assertTrue(is_melody_str(melody_note))

        # Test with enum parameter (this covers line 95)
        is_melody_enum = note_type_is(NoteType.MELODY)
        self.assertTrue(is_melody_enum(melody_note))

        # Test with different note types
        rest_note = AbstractObject(note_type="rest")
        self.assertFalse(is_melody_enum(rest_note))

    def test_note_repr(self):
        """Test the __repr__ method of the Note class."""
        # Create a note
        note = Note(pitch="C4", duration=1.0, note_type="melody")

        # Test the __repr__ method
        repr_str = repr(note)
        self.assertIn("pitch=C4", repr_str)
        self.assertIn("duration=1.0", repr_str)
        self.assertIn("type=melody", repr_str)

    def test_get_semitones_with_different_pitch_classes(self):
        """Test the get_semitones function with different pitch classes."""
        # This test is removed because the get_semitones function is not directly importable
        pass

    def test_melody_pattern_rule_with_different_pitch_classes(self):
        """Test the melody_pattern_rule with different pitch classes to cover line 187 in music.py."""
        # Test with different pitch classes
        pattern = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
        rule = create_melody_pattern_rule(pattern, transpose=False)

        # Create a sequence with the same pattern
        notes = [
            AbstractObject(pitch="C4", note_type="melody"),
            AbstractObject(pitch="D4", note_type="melody"),
            AbstractObject(pitch="E4", note_type="melody"),
            AbstractObject(pitch="F4", note_type="melody"),
            AbstractObject(pitch="G4", note_type="melody"),
            AbstractObject(pitch="A4", note_type="melody"),
            AbstractObject(pitch="B4", note_type="melody"),
        ]

        # The rule should pass because the pattern matches
        result = rule(notes)
        self.assertTrue(result)

        # Test with a different pattern
        different_notes = [
            AbstractObject(pitch="C4", note_type="melody"),
            AbstractObject(pitch="E4", note_type="melody"),
            AbstractObject(pitch="G4", note_type="melody"),
        ]

        # The rule should fail because the pattern doesn't match
        result = rule(different_notes)
        self.assertFalse(result)

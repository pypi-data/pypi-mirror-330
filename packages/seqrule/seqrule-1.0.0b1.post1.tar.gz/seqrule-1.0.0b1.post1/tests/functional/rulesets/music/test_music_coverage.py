"""
Coverage tests for the music ruleset.

These tests focus on covering specific lines and edge cases in the music ruleset
that aren't covered by the main test suite.
"""

from seqrule.rulesets.music import (
    Note,
    NoteType,
    TimeSignature,
    create_melody_pattern_rule,
    create_rhythm_pattern_rule,
)


class TestMusicCoverage:
    """Test suite for music ruleset coverage."""

    def test_note_repr(self):
        """Test the __repr__ method of Note."""
        note = Note(
            pitch="C4", duration=1.0, velocity=64, note_type=NoteType.MELODY.value
        )

        # Check that __repr__ returns a string
        repr_str = repr(note)
        assert isinstance(repr_str, str)
        assert "Note" in repr_str
        assert "pitch=C4" in repr_str  # No quotes around C4
        assert "duration=1.0" in repr_str
        assert "type=melody" in repr_str

    def test_time_signature_repr(self):
        """Test the __repr__ method of TimeSignature."""
        time_sig = TimeSignature(beats=4, beat_unit=4)

        # Check that __repr__ returns a string
        repr_str = repr(time_sig)
        assert isinstance(repr_str, str)
        assert "4/4" in repr_str

    def test_rhythm_pattern_rule_with_exact_match(self):
        """Test rhythm pattern rule with exact match."""
        # Test with exact match
        pattern = [1.0]

        # Create a sequence with a matching note
        seq = [
            Note(pitch="C4", duration=1.0, velocity=64, note_type=NoteType.MELODY.value)
        ]

        # Create the rule with allow_consolidation=False
        rule = create_rhythm_pattern_rule(pattern, allow_consolidation=False)

        # This should pass because the pattern exactly matches the sequence
        assert rule(seq) is True

    def test_rhythm_pattern_rule_with_consolidation(self):
        """Test rhythm pattern rule with consolidation."""
        # Test with consolidation
        pattern = [1.0]

        # Create a sequence with notes that can be consolidated
        seq = [
            Note(
                pitch="C4", duration=0.5, velocity=64, note_type=NoteType.MELODY.value
            ),
            Note(
                pitch="E4", duration=0.5, velocity=64, note_type=NoteType.MELODY.value
            ),
        ]

        # Create the rule with allow_consolidation=True
        rule = create_rhythm_pattern_rule(pattern, allow_consolidation=True)

        # This should pass because the notes can be consolidated to match the pattern
        assert rule(seq) is True

    def test_melody_pattern_rule_with_exact_match(self):
        """Test melody pattern rule with exact match."""
        # Test with exact match
        pattern = ["C4"]

        # Create a sequence with a matching note
        seq = [
            Note(pitch="C4", duration=1.0, velocity=64, note_type=NoteType.MELODY.value)
        ]

        # Create the rule
        rule = create_melody_pattern_rule(pattern)

        # This should pass because the pattern exactly matches the sequence
        assert rule(seq) is True

    def test_melody_pattern_rule_with_transposition(self):
        """Test melody pattern rule with transposition."""
        # Test with transposition
        pattern = ["C4", "E4"]

        # Create a sequence with a transposed pattern
        seq = [
            Note(
                pitch="D4", duration=1.0, velocity=64, note_type=NoteType.MELODY.value
            ),
            Note(
                pitch="F#4", duration=0.5, velocity=64, note_type=NoteType.MELODY.value
            ),
        ]

        # Create the rule with transpose=True
        rule = create_melody_pattern_rule(pattern, transpose=True)

        # This should pass because the sequence is a transposition of the pattern
        assert rule(seq) is True

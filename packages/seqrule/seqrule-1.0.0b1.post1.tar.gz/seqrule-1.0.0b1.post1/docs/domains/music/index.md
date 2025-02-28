# Musical Sequence Analysis

The music module provides specialized rules and objects for analyzing musical sequences. It supports various aspects of music theory including:
- Scale membership
- Chord progressions
- Voice leading
- Rhythm patterns
- Melodic contour

## Basic Usage

```python
from seqrule import AbstractObject
from seqrule.rulesets.music import (
    create_scale_rule,
    create_chord_rule,
    create_rhythm_rule
)

# Create a melody sequence
sequence = [
    AbstractObject(pitch="C4", duration=0.25, velocity=64),
    AbstractObject(pitch="E4", duration=0.25, velocity=64),
    AbstractObject(pitch="G4", duration=0.5, velocity=64),
]

# Check scale membership
c_major = create_scale_rule("major", "C")
is_valid = c_major(sequence)  # True

# Check chord structure
c_major_chord = create_chord_rule("major", "C")
is_chord = c_major_chord(sequence)  # True
```

## Musical Rules

### Scale Membership

```python
def create_scale_rule(scale_name, root_note):
    """
    Create a rule requiring notes to be in a scale.
    
    Args:
        scale_name (str): Name of the scale (e.g., "major", "minor")
        root_note (str): Root note of the scale
        
    Returns:
        Rule: A rule checking scale membership
        
    Example:
        >>> c_major = create_scale_rule("major", "C")
        >>> c_major(sequence)  # True if all notes in C major
    """
```

### Chord Structure

```python
def create_chord_rule(
    chord_type,
    root_note,
    allow_inversions=True
):
    """
    Create a rule checking chord structure.
    
    Args:
        chord_type (str): Type of chord (e.g., "major", "minor7")
        root_note (str): Root note of the chord
        allow_inversions (bool): Whether to allow chord inversions
        
    Returns:
        Rule: A rule checking chord structure
        
    Example:
        >>> c_maj7 = create_chord_rule("major7", "C")
        >>> c_maj7(sequence)  # True if forms C major 7
    """
```

### Rhythm Patterns

```python
def create_rhythm_rule(
    time_signature,
    allowed_durations=None
):
    """
    Create a rule checking rhythmic constraints.
    
    Args:
        time_signature (tuple): Time signature as (beats, beat_unit)
        allowed_durations (list, optional): List of allowed note durations
        
    Returns:
        Rule: A rule checking rhythmic requirements
        
    Example:
        >>> rhythm = create_rhythm_rule((4, 4))
        >>> rhythm(sequence)  # True if valid in 4/4
    """
```

## Advanced Features

### Voice Leading

```python
def create_voice_leading_rule(
    max_leap=12,
    resolve_leaps=True
):
    """
    Create a rule checking voice leading.
    
    Args:
        max_leap (int): Maximum allowed interval in semitones
        resolve_leaps (bool): Whether large leaps must resolve
        
    Returns:
        Rule: A rule checking voice leading
        
    Example:
        >>> voice_leading = create_voice_leading_rule()
        >>> voice_leading(sequence)  # True if good voice leading
    """
```

### Melodic Contour

```python
def create_contour_rule(contour_type):
    """
    Create a rule checking melodic contour.
    
    Args:
        contour_type (str): Type of contour (e.g., "ascending")
        
    Returns:
        Rule: A rule checking melodic contour
        
    Example:
        >>> ascending = create_contour_rule("ascending")
        >>> ascending(sequence)  # True if melody ascends
    """
```

### Complex Rules

Combine multiple rules for comprehensive analysis:

```python
from seqrule import And, Or, Not

# Create a melody rule
melody_rule = And(
    create_scale_rule("major", "C"),
    create_voice_leading_rule(max_leap=8),
    create_rhythm_rule((4, 4)),
    Not(create_chord_rule("diminished", "C"))
)

# Create a chord progression rule
progression_rule = And(
    create_chord_rule("major", "C"),
    Or(
        create_chord_rule("major", "F"),
        create_chord_rule("major", "G")
    )
)
```

## Best Practices

### 1. Note Validation

Always validate musical notes:
```python
def validate_note(note):
    """Check if note has required properties."""
    required = {"pitch", "duration"}
    return all(
        hasattr(note, prop)
        for prop in required
    )
```

### 2. Pitch Handling

Use consistent pitch notation:
```python
def normalize_pitch(note):
    """Normalize pitch to scientific notation."""
    if hasattr(note, "midi_note"):
        # Convert MIDI note number to scientific notation
        octave = (note.midi_note // 12) - 1
        pitch_class = ["C", "C#", "D", "D#", "E", "F",
                      "F#", "G", "G#", "A", "A#", "B"][
            note.midi_note % 12
        ]
        note.pitch = f"{pitch_class}{octave}"
    return note
```

### 3. Duration Formatting

Use consistent duration units (quarter notes = 1.0):
```python
def normalize_duration(note):
    """Convert duration to quarter note units."""
    if hasattr(note, "duration_ms"):
        note.duration = note.duration_ms / 500  # assuming 120 BPM
    return note
```

### 4. Error Handling

Handle missing or invalid properties gracefully:
```python
def get_pitch_class(note):
    """Get pitch class safely."""
    if not hasattr(note, "pitch"):
        return None
    try:
        return note.pitch[:-1]  # Remove octave number
    except (IndexError, TypeError):
        return None
```

## Performance Tips

1. Cache computed properties:
```python
class MusicSequence:
    def __init__(self, sequence):
        self._sequence = sequence
        self._total_duration = None
        
    @property
    def total_duration(self):
        if self._total_duration is None:
            self._total_duration = sum(
                note.duration for note in self._sequence
                if hasattr(note, "duration")
            )
        return self._total_duration
```

2. Use efficient pitch comparisons:
```python
def get_semitones(pitch1, pitch2):
    """Calculate semitones between pitches efficiently."""
    midi_map = {
        "C": 0, "C#": 1, "D": 2, "D#": 3,
        "E": 4, "F": 5, "F#": 6, "G": 7,
        "G#": 8, "A": 9, "A#": 10, "B": 11
    }
    p1_class = pitch1[:-1]
    p1_octave = int(pitch1[-1])
    p2_class = pitch2[:-1]
    p2_octave = int(pitch2[-1])
    
    return (midi_map[p2_class] + p2_octave * 12) - \
           (midi_map[p1_class] + p1_octave * 12)
```

3. Implement early returns:
```python
def check_scale_membership(sequence, scale_notes):
    """Check scale membership with early returns."""
    if not sequence:
        return True
        
    scale_set = set(scale_notes)
    for note in sequence:
        pitch_class = get_pitch_class(note)
        if pitch_class is None:
            continue
        if pitch_class not in scale_set:
            return False
            
    return True
```

## Musical Constants

```python
# Scale patterns (intervals from root)
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
}

# Chord patterns (intervals from root)
CHORDS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
    "dominant7": [0, 4, 7, 10],
}

# Common note durations (in quarter notes)
DURATIONS = {
    "whole": 4.0,
    "half": 2.0,
    "quarter": 1.0,
    "eighth": 0.5,
    "sixteenth": 0.25,
    "thirty_second": 0.125,
}
``` 
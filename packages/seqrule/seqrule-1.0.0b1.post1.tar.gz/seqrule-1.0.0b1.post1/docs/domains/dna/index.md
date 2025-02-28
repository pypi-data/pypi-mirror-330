# DNA Sequence Analysis

The DNA module provides specialized rules and objects for analyzing DNA sequences. It supports common bioinformatics tasks such as:
- GC content analysis
- Motif finding
- Restriction site identification
- Primer design validation
- Secondary structure prediction

## Basic Usage

```python
from seqrule import AbstractObject
from seqrule.rulesets.dna import (
    create_gc_content_rule,
    create_motif_rule,
    create_restriction_site_rule
)

# Create a DNA sequence
sequence = [
    AbstractObject(base="A", position=1),
    AbstractObject(base="T", position=2),
    AbstractObject(base="G", position=3),
    AbstractObject(base="C", position=4),
]

# Check GC content
gc_rule = create_gc_content_rule(
    min_percent=40,
    max_percent=60
)
is_valid = gc_rule(sequence)  # True (50% GC)

# Check for motif
motif_rule = create_motif_rule("ATG")
has_motif = motif_rule(sequence)  # False
```

## DNA Rules

### GC Content

```python
def create_gc_content_rule(min_percent=0, max_percent=100):
    """
    Create a rule checking GC content percentage.
    
    Args:
        min_percent (float): Minimum allowed GC percentage
        max_percent (float): Maximum allowed GC percentage
        
    Returns:
        Rule: A rule checking GC content
        
    Example:
        >>> gc_rule = create_gc_content_rule(40, 60)
        >>> gc_rule(sequence)  # True if GC% between 40-60
    """
```

### Motif Finding

```python
def create_motif_rule(motif, allow_gaps=False, max_gap=None):
    """
    Create a rule requiring a specific sequence motif.
    
    Args:
        motif (str): The DNA sequence motif to find
        allow_gaps (bool): Whether to allow gaps in the motif
        max_gap (int, optional): Maximum allowed gap length
        
    Returns:
        Rule: A rule checking for the motif
        
    Example:
        >>> motif_rule = create_motif_rule("TATA", allow_gaps=True)
        >>> motif_rule(sequence)  # True if TATA box found
    """
```

### Restriction Sites

```python
def create_restriction_site_rule(site):
    """
    Create a rule checking for restriction sites.
    
    Args:
        site (str): The restriction site sequence
        
    Returns:
        Rule: A rule checking for the site
        
    Example:
        >>> ecori_rule = create_restriction_site_rule("GAATTC")
        >>> ecori_rule(sequence)  # True if EcoRI site found
    """
```

### Primer Design

```python
def create_primer_rule(
    length=20,
    gc_content=(40, 60),
    max_repeat=4,
    end_gc=True
):
    """
    Create a rule for valid primer sequences.
    
    Args:
        length (int): Required primer length
        gc_content (tuple): (min%, max%) GC content
        max_repeat (int): Maximum base repetition
        end_gc (bool): Require G/C at 3' end
        
    Returns:
        Rule: A rule checking primer requirements
        
    Example:
        >>> primer_rule = create_primer_rule(length=18)
        >>> primer_rule(sequence)  # True if valid primer
    """
```

## Advanced Features

### Secondary Structure

```python
def create_secondary_structure_rule(
    max_hairpin=4,
    max_dimer=6
):
    """
    Create a rule checking secondary structure.
    
    Args:
        max_hairpin (int): Maximum hairpin length
        max_dimer (int): Maximum dimer length
        
    Returns:
        Rule: A rule checking structure constraints
        
    Example:
        >>> structure_rule = create_secondary_structure_rule()
        >>> structure_rule(sequence)  # True if no bad structures
    """
```

### Base Types and Methylation States

The DNA module provides enums for working with different base types and methylation states:

```python
from seqrule.rulesets.dna import BaseType, MethylationState

# Base types categorize DNA bases by chemical properties
class BaseType(Enum):
    PURINE = "purine"         # A, G
    PYRIMIDINE = "pyrimidine" # C, T
    STRONG = "strong"         # G, C (3 H-bonds)
    WEAK = "weak"             # A, T (2 H-bonds)
    AMINO = "amino"           # A, C (amino group)
    KETO = "keto"             # G, T (keto group)

# Methylation states track DNA methylation
class MethylationState(Enum):
    UNMETHYLATED = "unmethylated"
    METHYLATED = "methylated"
    HYDROXYMETHYLATED = "hydroxymethylated"  # 5-hmC
    UNKNOWN = "unknown"
```

### Structural Elements

Define and analyze structural elements in DNA sequences:

```python
from seqrule.rulesets.dna import StructuralElement

# Create a structural element with specific properties
promoter = StructuralElement(
    name="TATA box",
    sequence="TATAAA",
    position_range=(35, 45),  # Relative to transcription start
    importance="high"
)

# Use structural elements in rules
def create_has_element_rule(element):
    """Create a rule requiring a specific structural element."""
    # Implementation
```

### Complex Rules

Combine multiple DNA rules for comprehensive analysis:

```python
from seqrule import And, Or, Not

# Create a complex primer rule
primer_rule = And(
    create_primer_rule(length=20),
    Not(create_motif_rule("AAAAA")),  # No poly-A
    create_gc_content_rule(45, 55)
)

# Create a cloning rule
cloning_rule = And(
    create_restriction_site_rule("GAATTC"),  # EcoRI
    create_restriction_site_rule("GGATCC"),  # BamHI
    Not(create_restriction_site_rule("CTGCAG"))  # No PstI
)
```

## Best Practices

### 1. Sequence Validation

Always validate input sequences:
```python
def validate_dna_sequence(sequence):
    """Check if sequence contains valid DNA bases."""
    valid_bases = set("ATCG")
    return all(
        obj.base.upper() in valid_bases
        for obj in sequence
    )
```

### 2. Position Handling

Use 1-based positions consistently:
```python
sequence = [
    AbstractObject(base="A", position=1),
    AbstractObject(base="T", position=2),
]
```

### 3. Case Sensitivity

Handle case insensitively but preserve input:
```python
def normalize_sequence(sequence):
    """Normalize bases to uppercase."""
    return [
        AbstractObject(
            base=obj.base.upper(),
            position=obj.position
        )
        for obj in sequence
    ]
```

### 4. Error Handling

Handle missing or invalid bases gracefully:
```python
def count_gc(sequence):
    """Count GC content safely."""
    gc = 0
    total = 0
    for obj in sequence:
        if not hasattr(obj, "base"):
            continue
        base = obj.base.upper()
        if base not in "ATCG":
            continue
        if base in "GC":
            gc += 1
        total += 1
    return gc, total
```

## Performance Tips

1. Cache computed properties:
```python
class DNASequence:
    def __init__(self, sequence):
        self._sequence = sequence
        self._gc_content = None
        
    @property
    def gc_content(self):
        if self._gc_content is None:
            gc, total = count_gc(self._sequence)
            self._gc_content = gc / total if total > 0 else 0
        return self._gc_content
```

2. Use efficient data structures:
```python
def find_motifs(sequence, motif):
    """Find all occurrences of a motif efficiently."""
    bases = "".join(obj.base for obj in sequence)
    positions = []
    start = 0
    while True:
        pos = bases.find(motif, start)
        if pos == -1:
            break
        positions.append(pos + 1)
        start = pos + 1
    return positions
```

3. Implement early returns:
```python
def check_primer(sequence):
    """Check primer validity with early returns."""
    if len(sequence) != 20:
        return False
    if not sequence[-1].base.upper() in "GC":
        return False
    gc, total = count_gc(sequence)
    if not 40 <= (gc/total)*100 <= 60:
        return False
    return True
``` 
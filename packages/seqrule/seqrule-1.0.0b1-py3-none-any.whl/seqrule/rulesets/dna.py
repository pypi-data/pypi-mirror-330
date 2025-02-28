"""
DNA sequence rules.

This module implements sequence rules for DNA sequences, with support for:
- Base patterns and structural constraints
- Motif detection and analysis
- Secondary structure prediction
- Methylation patterns
- Common sequence elements (promoters, binding sites)
- GC content and skew analysis
- Codon usage patterns

Common use cases:
- Validating PCR primers
- Checking promoter sequences
- Analyzing CpG islands
- Detecting binding motifs
- Validating gene sequences
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from ..core import AbstractObject, Sequence
from ..dsl import DSLRule


class BaseType(Enum):
    """Types of DNA bases."""

    PURINE = "purine"  # A, G
    PYRIMIDINE = "pyrimidine"  # C, T
    STRONG = "strong"  # G, C (3 H-bonds)
    WEAK = "weak"  # A, T (2 H-bonds)
    AMINO = "amino"  # A, C (amino group)
    KETO = "keto"  # G, T (keto group)


class MethylationState(Enum):
    """DNA methylation states."""

    UNMETHYLATED = "unmethylated"
    METHYLATED = "methylated"
    HYDROXYMETHYLATED = "hydroxymethylated"  # 5-hmC
    UNKNOWN = "unknown"


@dataclass
class StructuralElement:
    """DNA structural element properties."""

    melting_temp: float  # Melting temperature in Celsius
    gc_content: float  # GC content as fraction
    stability: float  # Free energy (ΔG) in kcal/mol
    complexity: float  # Sequence complexity score


class Nucleotide(AbstractObject):
    """
    Represents a DNA nucleotide with properties.

    Properties:
        base: The nucleotide base (A, T, G, C)
        type: Base type classification
        methylation: Methylation state
        position: Position in sequence (0-based)
    """

    def __init__(
        self,
        base: str,
        methylation: MethylationState = MethylationState.UNKNOWN,
        position: Optional[int] = None,
    ):
        """Initialize a nucleotide with its properties."""
        if base not in ["A", "T", "G", "C"]:
            raise ValueError(f"Invalid base: {base}. Must be one of A, T, G, C")

        # Determine base types
        types = set()
        if base in ["A", "G"]:
            types.add(BaseType.PURINE)
        if base in ["C", "T"]:
            types.add(BaseType.PYRIMIDINE)
        if base in ["G", "C"]:
            types.add(BaseType.STRONG)
        if base in ["A", "T"]:
            types.add(BaseType.WEAK)
        if base in ["A", "C"]:
            types.add(BaseType.AMINO)
        if base in ["G", "T"]:
            types.add(BaseType.KETO)

        super().__init__(
            base=base, types=types, methylation=methylation.value, position=position
        )

    def __repr__(self) -> str:
        return f"Nucleotide({self.properties.get('base')})"


def nucleotide_base_is(base: str) -> Callable[[AbstractObject], bool]:
    """Creates a predicate that checks if a nucleotide has a specific base."""
    return lambda obj: obj["base"] == base


def nucleotide_type_is(base_type: BaseType) -> Callable[[AbstractObject], bool]:
    """Creates a predicate that checks if a nucleotide is of a specific type."""
    return lambda obj: base_type in obj["types"]


def create_no_consecutive_rule(count: int) -> DSLRule:
    """
    Creates a rule forbidding 'count' consecutive identical bases.

    Example:
        no_poly_a = create_no_consecutive_rule(4)  # No poly-A stretches
    """

    def check_consecutive(seq: Sequence) -> bool:
        if len(seq) < count:
            return True
        for i in range(len(seq) - count + 1):
            base = seq[i]["base"]
            consecutive_count = 1
            for j in range(i + 1, len(seq)):
                if seq[j]["base"] == base:
                    consecutive_count += 1
                    if consecutive_count > count:
                        return False
                else:
                    break
        return True

    return DSLRule(check_consecutive, f"no {count} consecutive identical bases")


def create_motif_rule(
    motif: str, max_mismatches: int = 0, allow_iupac: bool = True
) -> DSLRule:
    """
    Creates a rule requiring a specific sequence motif.

    Args:
        motif: The sequence motif (can include IUPAC codes if allow_iupac=True)
        max_mismatches: Maximum allowed mismatches
        allow_iupac: Whether to interpret IUPAC ambiguity codes

    Example:
        tata_box = create_motif_rule("TATAAA")
        cpg_site = create_motif_rule("CG")
    """
    iupac_map = {
        "R": "[AG]",  # Purine
        "Y": "[CT]",  # Pyrimidine
        "S": "[GC]",  # Strong
        "W": "[AT]",  # Weak
        "K": "[GT]",  # Keto
        "M": "[AC]",  # Amino
        "B": "[CGT]",  # Not A
        "D": "[AGT]",  # Not C
        "H": "[ACT]",  # Not G
        "V": "[ACG]",  # Not T
        "N": "[ACGT]",  # Any
    }

    if allow_iupac:
        pattern = "".join(iupac_map.get(b, b) for b in motif.upper())
    else:
        pattern = motif.upper()

    regex = re.compile(pattern)

    def check_motif(seq: Sequence) -> bool:
        sequence = "".join(n["base"] for n in seq)
        return bool(regex.search(sequence))

    return DSLRule(check_motif, f"contains motif {motif}")


def create_gc_content_rule(min_percent: float, max_percent: float) -> DSLRule:
    """
    Creates a rule requiring GC content within a percentage range.

    Example:
        cpg_island = create_gc_content_rule(min_percent=60, max_percent=100)
    """

    def check_gc_content(seq: Sequence) -> bool:
        if not seq:
            return False
        gc_count = sum(1 for obj in seq if obj["base"] in ["G", "C"])
        gc_percent = (gc_count / len(seq)) * 100
        return min_percent <= gc_percent <= max_percent

    return DSLRule(
        check_gc_content, f"GC content between {min_percent}% and {max_percent}%"
    )


def create_gc_skew_rule(window_size: int, threshold: float) -> DSLRule:
    """
    Creates a rule checking GC skew [(G-C)/(G+C)] in sliding windows.

    Example:
        ori_finder = create_gc_skew_rule(window_size=1000, threshold=0.2)
    """

    def check_gc_skew(seq: Sequence) -> bool:
        if len(seq) < window_size:
            return True

        for i in range(len(seq) - window_size + 1):
            window = seq[i : i + window_size]
            g_count = sum(1 for n in window if n["base"] == "G")
            c_count = sum(1 for n in window if n["base"] == "C")
            if g_count + c_count == 0:
                continue
            skew = (g_count - c_count) / (g_count + c_count)
            if abs(skew) > threshold:
                return False
        return True

    return DSLRule(check_gc_skew, f"GC skew <= {threshold} in {window_size}bp windows")


def create_methylation_rule(pattern: str = "CG") -> DSLRule:
    """
    Creates a rule checking methylation patterns.

    Example:
        cpg_methylation = create_methylation_rule("CG")
    """

    def check_methylation(seq: Sequence) -> bool:
        bases = "".join(n["base"] for n in seq)
        for match in re.finditer(pattern, bases):
            start = match.start()
            if any(
                seq[i]["methylation"] == MethylationState.UNMETHYLATED.value
                for i in range(start, start + len(pattern))
            ):
                return False
        return True

    return DSLRule(check_methylation, f"methylated {pattern} sites")


def create_complementary_rule(other_seq: Sequence) -> DSLRule:
    """
    Creates a rule requiring the sequence to be complementary to another.

    Example:
        is_complement = create_complementary_rule(forward_strand)
    """
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}

    def check_complementary(seq: Sequence) -> bool:
        if len(seq) != len(other_seq):
            return False
        return all(
            seq[i]["base"] == complement[other_seq[i]["base"]] for i in range(len(seq))
        )

    return DSLRule(check_complementary, "is complementary to reference sequence")


def create_complexity_rule(min_complexity: float) -> DSLRule:
    """
    Creates a rule checking sequence complexity.

    Example:
        sufficient_complexity = create_complexity_rule(min_complexity=0.8)
    """

    def calculate_complexity(seq: Sequence) -> float:
        if not seq:
            return 0.0
        # Use linguistic complexity (unique k-mers / possible k-mers)
        k = min(len(seq), 5)
        bases = "".join(n["base"] for n in seq)

        # For very short sequences or repeating sequences, adjust complexity
        if (
            len(bases) < 3
        ):  # Sequences shorter than 3 bases are considered low complexity
            return 0.0

        # For repeating sequences (all same base), return 0 complexity
        if len(set(bases)) == 1:
            return 0.0

        unique_kmers = {bases[i : i + k] for i in range(len(bases) - k + 1)}
        max_kmers = min(4**k, len(seq) - k + 1)
        return len(unique_kmers) / max_kmers

    def check_complexity(seq: Sequence) -> bool:
        return calculate_complexity(seq) >= min_complexity

    return DSLRule(check_complexity, f"sequence complexity >= {min_complexity}")


# Common DNA sequence rules
promoter_rules = [
    create_motif_rule("TATAAA", max_mismatches=1),  # TATA box
    create_gc_content_rule(min_percent=40, max_percent=60),
]

cpg_island_rules = [
    create_gc_content_rule(min_percent=60, max_percent=100),
    create_motif_rule("CG"),
    create_complexity_rule(min_complexity=0.8),
]

primer_rules = [
    create_gc_content_rule(min_percent=40, max_percent=60),
    create_no_consecutive_rule(4),
]

# Example sequences
tata_box = [Nucleotide(base) for base in "TATAAA"]
cpg_site = [
    Nucleotide("C", methylation=MethylationState.METHYLATED),
    Nucleotide("G", methylation=MethylationState.METHYLATED),
]
primer = [Nucleotide(base) for base in "ATCGATCGATCG"]

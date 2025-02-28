"""
Example of extending SeqRule with a custom domain module.

This example demonstrates how to create a custom domain module for
protein sequence analysis, showing how to leverage the core SeqRule
abstractions and extend them with domain-specific functionality.
"""

from enum import Enum
from typing import List, Dict, Optional, Callable, Union

from seqrule import (
    AbstractObject, 
    Sequence, 
    DSLRule, 
    And, 
    Or, 
    Not,
    PredicateFunction,
    create_property_trend_rule,
    generate_sequences,
)

# Define domain-specific enums
class AminoAcidProperty(Enum):
    """Properties of amino acids."""
    HYDROPHOBIC = "hydrophobic"
    HYDROPHILIC = "hydrophilic"
    POLAR = "polar"
    CHARGED = "charged"
    AROMATIC = "aromatic"

# Define mappings for domain-specific knowledge
AMINO_ACID_PROPERTIES = {
    'A': [AminoAcidProperty.HYDROPHOBIC],
    'C': [AminoAcidProperty.HYDROPHOBIC],
    'D': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.CHARGED],
    'E': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.CHARGED],
    'F': [AminoAcidProperty.HYDROPHOBIC, AminoAcidProperty.AROMATIC],
    'G': [AminoAcidProperty.HYDROPHOBIC],
    'H': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.CHARGED, AminoAcidProperty.AROMATIC],
    'I': [AminoAcidProperty.HYDROPHOBIC],
    'K': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.CHARGED],
    'L': [AminoAcidProperty.HYDROPHOBIC],
    'M': [AminoAcidProperty.HYDROPHOBIC],
    'N': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.POLAR],
    'P': [AminoAcidProperty.HYDROPHOBIC],
    'Q': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.POLAR],
    'R': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.CHARGED],
    'S': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.POLAR],
    'T': [AminoAcidProperty.HYDROPHILIC, AminoAcidProperty.POLAR],
    'V': [AminoAcidProperty.HYDROPHOBIC],
    'W': [AminoAcidProperty.HYDROPHOBIC, AminoAcidProperty.AROMATIC],
    'Y': [AminoAcidProperty.HYDROPHOBIC, AminoAcidProperty.AROMATIC],
}

# Domain-specific helper functions
def create_amino_acid(code: str, position: int) -> AbstractObject:
    """
    Create an amino acid AbstractObject with appropriate properties.
    
    Args:
        code: Single-letter amino acid code
        position: Position in the protein sequence
        
    Returns:
        AbstractObject: Representing the amino acid
    """
    properties = AMINO_ACID_PROPERTIES.get(code.upper(), [])
    return AbstractObject(
        code=code.upper(),
        position=position,
        hydrophobic=AminoAcidProperty.HYDROPHOBIC in properties,
        hydrophilic=AminoAcidProperty.HYDROPHILIC in properties,
        polar=AminoAcidProperty.POLAR in properties,
        charged=AminoAcidProperty.CHARGED in properties,
        aromatic=AminoAcidProperty.AROMATIC in properties,
        properties=properties
    )

def protein_from_string(sequence: str) -> Sequence:
    """
    Convert a string of amino acid codes to a sequence of AbstractObjects.
    
    Args:
        sequence: String of amino acid single-letter codes
        
    Returns:
        Sequence: List of AbstractObjects representing amino acids
    """
    return [create_amino_acid(aa, i+1) for i, aa in enumerate(sequence.upper())]

# Domain-specific rule factory functions
def create_hydrophobic_pattern_rule(pattern: str, tolerance: int = 0) -> DSLRule:
    """
    Create a rule that checks if hydrophobic amino acids follow a pattern.
    
    Args:
        pattern: String of 1s and 0s, where 1 means hydrophobic and 0 means not
        tolerance: Number of allowed mismatches
        
    Returns:
        DSLRule: Rule checking the hydrophobic pattern
    """
    def check_pattern(seq: Sequence) -> bool:
        if len(seq) < len(pattern):
            return False
            
        mismatches = 0
        for i, expected in enumerate(pattern):
            expected_hydrophobic = expected == '1'
            actual_hydrophobic = seq[i].get("hydrophobic", False)
            
            if expected_hydrophobic != actual_hydrophobic:
                mismatches += 1
                if mismatches > tolerance:
                    return False
        return True
    
    pattern_desc = pattern.replace('1', 'H').replace('0', 'P')
    return DSLRule(check_pattern, f"hydrophobic pattern {pattern_desc} with tolerance {tolerance}")

def create_motif_rule(motif: str) -> DSLRule:
    """
    Create a rule that checks for a specific amino acid motif.
    
    Args:
        motif: String of amino acid codes to match
        
    Returns:
        DSLRule: Rule checking for the motif
    """
    motif = motif.upper()
    
    def check_motif(seq: Sequence) -> bool:
        if len(seq) < len(motif):
            return False
            
        # Check for motif at each possible starting position
        for start in range(len(seq) - len(motif) + 1):
            matches = True
            for i, expected in enumerate(motif):
                if seq[start + i].get("code") != expected:
                    matches = False
                    break
            if matches:
                return True
        return False
    
    return DSLRule(check_motif, f"contains motif {motif}")

def create_charge_distribution_rule(min_charge_distance: int = 2) -> DSLRule:
    """
    Create a rule that checks if charged amino acids are well-distributed.
    
    Args:
        min_charge_distance: Minimum distance between charged amino acids
        
    Returns:
        DSLRule: Rule checking charge distribution
    """
    def check_distribution(seq: Sequence) -> bool:
        charged_positions = []
        for i, aa in enumerate(seq):
            if aa.get("charged", False):
                charged_positions.append(i)
                
        # Check distances between charged amino acids
        for i in range(1, len(charged_positions)):
            if charged_positions[i] - charged_positions[i-1] < min_charge_distance:
                return False
        return True
    
    return DSLRule(check_distribution, f"charged amino acids separated by at least {min_charge_distance}")

# Example usage
def main():
    # Create a sequence
    protein_seq = protein_from_string("MKTAFLLLSSVVMLSEPQIGWFQGPYSWKPVSSIDCAKYLDKGCLRVTNSGTTLESFIPNQPFKDLLIMKNGQIRLEESRSIWEGKPLDYSNISFTSCFKSEDCQVLSESYKLNDHGTKCLEWPGVEISCKSGHSICQFTNGTFHVTDKKVRIYQSNTISVSCLKEAFLNK")
    
    # Create individual rules
    hydrophobic_rule = create_hydrophobic_pattern_rule("10101", tolerance=1)
    motif_rule = create_motif_rule("PGVE")
    charge_rule = create_charge_distribution_rule(min_charge_distance=3)
    
    # Combine rules
    complex_rule = And(
        hydrophobic_rule,
        Or(
            motif_rule,
            Not(charge_rule)
        )
    )
    
    # Validate sequence
    print(f"Sequence valid against complex rule: {complex_rule(protein_seq)}")
    
    # Use existing factory functions from seqrule
    # This demonstrates the integration of core seqrule functionality
    ascending_positions = create_property_trend_rule("position", "ascending")
    print(f"Positions are ascending: {ascending_positions(protein_seq)}")
    
    # Generate sequences
    domain = [create_amino_acid(aa, 0) for aa in "ACDEFGHIKLMNPQRSTVWY"]
    hydrophobic_sequences = generate_sequences(domain, max_length=5, filter_rule=hydrophobic_rule)
    print(f"Generated {len(hydrophobic_sequences)} sequences matching the hydrophobic pattern")
    
if __name__ == "__main__":
    main() 
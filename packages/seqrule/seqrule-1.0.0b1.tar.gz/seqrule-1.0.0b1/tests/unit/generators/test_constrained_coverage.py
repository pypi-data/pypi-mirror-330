import unittest

from seqrule.core import AbstractObject
from seqrule.generators.constrained import ConstrainedGenerator, GeneratorConfig
from seqrule.generators.patterns import PropertyPattern


class TestConstrainedGeneratorCoverage(unittest.TestCase):
    """Test cases to improve coverage for constrained.py."""

    def test_generate_with_no_randomization(self):
        """Test the generate method with randomize_candidates=False."""
        # Create a domain of objects
        domain = [
            AbstractObject(value=1, color="red"),
            AbstractObject(value=2, color="blue"),
            AbstractObject(value=3, color="green"),
        ]

        # Create a config with randomize_candidates=False
        config = GeneratorConfig(
            randomize_candidates=False, max_candidates_per_step=0  # No limit
        )

        # Create a generator
        generator = ConstrainedGenerator(domain, config)

        # Add a constraint
        generator.add_constraint(lambda seq: len(seq) <= 2)

        # Generate sequences
        sequences = list(generator.generate(max_length=2))

        # Check that sequences were generated
        self.assertTrue(len(sequences) > 0)

        # Check that all sequences satisfy the constraint
        for seq in sequences:
            self.assertTrue(len(seq) <= 2)

    def test_generate_with_pattern(self):
        """Test the generate method with a pattern."""
        # Create a domain of objects
        domain = [
            AbstractObject(value=1, color="red"),
            AbstractObject(value=2, color="blue"),
            AbstractObject(value=3, color="green"),
        ]

        # Create a generator
        generator = ConstrainedGenerator(domain)

        # Add a pattern
        pattern = PropertyPattern("color", ["red", "blue"])
        generator.add_pattern(pattern)

        # Generate sequences
        sequences = list(generator.generate(max_length=2))

        # Check that sequences were generated
        self.assertTrue(len(sequences) > 0)

        # Check that all sequences follow the pattern
        for seq in sequences:
            if len(seq) >= 2:
                self.assertEqual(seq[0]["color"], "red")
                self.assertEqual(seq[1]["color"], "blue")

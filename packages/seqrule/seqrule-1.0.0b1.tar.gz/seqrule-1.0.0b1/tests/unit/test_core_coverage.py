import unittest

from seqrule.core import AbstractObject, check_sequence


class TestCoreCoverage(unittest.TestCase):
    """Test cases to improve coverage for core.py."""

    def test_check_sequence(self):
        """Test the check_sequence function."""

        # Create a simple rule
        def simple_rule(seq):
            return len(seq) > 0

        # Create a sequence
        seq = [AbstractObject(value=1), AbstractObject(value=2)]

        # Check that the sequence satisfies the rule
        result = check_sequence(seq, simple_rule)
        self.assertTrue(result)

        # Check with an empty sequence
        empty_seq = []
        result = check_sequence(empty_seq, simple_rule)
        self.assertFalse(result)

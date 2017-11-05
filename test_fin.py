"""Unit tests for fin main cli code."""
import unittest
from click.testing import CliRunner
import fin


class FinTest(unittest.TestCase):
    """Test fun cli."""

    def test_fin_bare(self):
        """Test fin bare cli output."""
        runner = CliRunner()
        result = runner.invoke(fin.fin, [])
        golden = ""
        with open("testfiles/fin_bare.golden", "r") as f:
            golden = f.read()
        f.closed
        self.assertEqual(golden, result.output)

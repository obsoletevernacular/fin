"""Unit tests for utils.py."""
import unittest
import utils
from report import Transaction


class UtilsTest(unittest.TestCase):
    """Test utility functions."""

    def test_csvload_happy(self):
        """Test csvload happy path."""
        ts = []
        with open("testfiles/csvload_happy.test", "r") as f:
            ts = utils.csvload(f)
        f.closed
        self.assertEqual(2, len(ts))
        for t in ts:
            self.assertIsInstance(t, Transaction)

    def test_csvload_unopened_file(self):
        """Test csvload with an unopened file."""
        self.assertRaises(utils.InvalidCSV, utils.csvload,
                          "testfiles/csvload_happy.test")

    def test_csvload_notacsv(self):
        """Test csvload with non-csv file."""
        self.assertRaises(utils.InvalidCSV, utils.csvload,
                          "testfiles/csvload_notacsv.test")

    def test_csvload_invalidfieldscsv(self):
        """Test csvload with a csv file with invalid field headers."""
        self.assertRaises(utils.InvalidCSV, utils.csvload,
                          "testfiles/csvload_invalidfieldscsv.test")

    def test_csvload_nodescriptioncsv(self):
        """Test csvload with a csv file with poorly formatted rows."""
        self.assertRaises(utils.InvalidCSV, utils.csvload,
                          "testfiles/csvload_nodescriptioncsv.test")

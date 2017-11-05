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

    def test_fin_report_oct_individual(self):
        """Test fin report on each individual account file."""
        runner = CliRunner()
        tests = ["fin_report_credit_oct",
                 "fin_report_checking_oct",
                 "fin_report_savings_oct"]
        for t in tests:
            testpath = "testfiles/" + t + ".test"
            result = runner.invoke(fin.fin, ["report", testpath])
            goldenpath = "testfiles/" + t + ".golden"
            golden = ""
            with open(goldenpath, "r") as f:
                golden = f.read()
            f.closed
            self.assertEqual(golden, result.output)

    def test_fin_report_oct_composed(self):
        """Test fin report with multiple transaction files."""
        runner = CliRunner()
        tests = ["testfiles/fin_report_checking_oct.test",
                 "testfiles/fin_report_credit_oct.test",
                 "testfiles/fin_report_savings_oct.test"]
        # args = ["report"].append(tests)
        result = runner.invoke(fin.report, tests)
        golden = ""
        with open("testfiles/fin_report_oct.golden", "r") as f:
            golden = f.read()
        f.closed
        self.assertEqual(golden, result.output)

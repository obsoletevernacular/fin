"""Unit tests for fin main cli code."""
import unittest
from click.testing import CliRunner
import fin
import os
import pytest


@pytest.fixture()
def finrunner():
    """Fin CLI testing fixture."""
    return CliRunner()


@pytest.fixture()
def testfiles():
    """Return the location for the testfiles."""
    return os.path.join(os.getcwd(), "testfiles")


def test_fin_import_checking(testfiles, finrunner):
    """Test fin import."""
    golden = ""
    with open("testfiles/fin_import_checking_oct.golden", "r") as f:
        golden = f.read()
    f.closed
    with finrunner.isolated_filesystem():
        test = os.path.join(testfiles, "fin_import_checking_oct.test")
        res = finrunner.invoke(fin.import_transactions, [test])
        assert not res.exception
        assert os.path.exists(".default.obj")
        assert golden == res.output


def test_fin_import_credit(testfiles, finrunner):
    """Test fin import."""
    golden = ""
    with open("testfiles/fin_import_credit_oct.golden", "r") as f:
        golden = f.read()
    f.closed
    with finrunner.isolated_filesystem():
        test = os.path.join(testfiles, "fin_import_credit_oct.test")
        res = finrunner.invoke(fin.import_transactions, [test])
        assert not res.exception
        assert os.path.exists(".default.obj")
        assert golden == res.output


def test_fin_import_savings(testfiles, finrunner):
    """Test fin import."""
    golden = ""
    with open("testfiles/fin_import_savings_oct.golden", "r") as f:
        golden = f.read()
    f.closed
    with finrunner.isolated_filesystem():
        test = os.path.join(testfiles, "fin_import_savings_oct.test")
        # assert os.path.exists(test)
        res = finrunner.invoke(fin.import_transactions, [test])
        assert not res.exception
        assert os.path.exists(".default.obj")
        assert golden == res.output


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
        result = runner.invoke(fin.report, tests)
        golden = ""
        with open("testfiles/fin_report_oct.golden", "r") as f:
            golden = f.read()
        f.closed
        self.assertEqual(golden, result.output)

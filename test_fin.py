"""Unit tests for fin main cli code."""
from click.testing import CliRunner
import os
import pytest

import fin


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


def test_fin_bare(testfiles, finrunner):
    """Test fin bare cli output."""
    result = finrunner.invoke(fin.fin, [])
    golden = ""
    with open(os.path.join(testfiles,"fin_bare.golden"), "r") as f:
        golden = f.read()
    f.closed
    assert golden == result.output


def test_fin_report_oct_individual(testfiles, finrunner):
    """Test fin report on each individual account file."""
    tests = ["fin_report_credit_oct",
             "fin_report_checking_oct",
             "fin_report_savings_oct"]
    for t in tests:
        testfile = "%s.test" % t
        testpath = os.path.join(testfiles, testfile)
        result = finrunner.invoke(fin.fin, ["report", testpath])
        goldenfile = "%s.golden" % t
        goldenpath = os.path.join(testfiles, goldenfile)
        golden = ""
        with open(goldenpath, "r") as f:
            golden = f.read()
        f.closed
        assert golden ==  result.output


def test_fin_report_oct_composed(testfiles, finrunner):
    """Test fin report with multiple transaction files."""
    tests = [os.path.join(testfiles,"fin_report_checking_oct.test"),
             os.path.join(testfiles,"fin_report_credit_oct.test"),
             os.path.join(testfiles,"fin_report_savings_oct.test")]
    result = finrunner.invoke(fin.report, tests)
    golden = ""
    goldenpath = os.path.join(testfiles, "fin_report_oct.golden")
    with open(goldenpath, "r") as f:
        golden = f.read()
    f.closed
    assert golden == result.output

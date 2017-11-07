"""Unit tests for report.py."""
import unittest
from report import Report
from report import SuperReport
from report import Transaction
import os
import pickle
import pytest


@pytest.fixture
def report(tmpdir):
    """Pytest fixture to return a default report."""
    cwd = tmpdir.chdir()
    yield Report()
    cwd.chdir()


@pytest.fixture
def superreport(tmpdir):
    """Pytest fixture to return a default super report."""
    cwd = tmpdir.chdir()
    yield SuperReport()
    cwd.chdir()


def test_super_report_save(superreport):
    """Test report save functionality."""
    superreport.save()
    fh = open(".default.obj", "r")
    z = pickle.load(fh)
    # assume two reports are equal if their str() are equal
    assert str(z) == str(superreport)


def test_superreport_save_default(superreport):
    """Test report save default location."""
    default_obj = ".default.obj"
    superreport.save()
    assert os.path.exists(default_obj)


def test_superreport_save_db(superreport):
    """Test report save with a passed db path."""
    db_path = ".testdb.obj"
    superreport.save(db_path)
    assert os.path.exists(db_path)


def test_superreport_load(superreport):
    """Test report load."""
    db_path = ".testdb.obj"
    r = SuperReport("saved")
    r.save(db_path)
    superreport.load(db_path)
    assert str(r) == str(superreport)


def test_superreport_add_report(superreport):
    """Test superreport adding a report."""
    r = Report("test1")
    r.add_transaction(Transaction())
    r.add_transaction(Transaction())
    r.add_transaction(Transaction())
    superreport.add_report(r)
    assert 3 == len(superreport.transactions)


def test_supereport_str(superreport):
    """Test superreport string representation."""
    expect = """test1
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00
test2
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00
test3
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00
3 files processed. summary report below:
summary
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00"""
    for i in range(1, 4):
        superreport.add_report(Report("test%d" % i))
    assert expect == str(superreport)


def test_report_load_notreport(report):
    """Test report load with a non report object."""
    db_file = ".notreport.obj"

    class NotReport():
        pass

    with open(db_file, "w") as fh:
        nr = NotReport()
        pickle.dump(nr, fh)
    fh.closed
    pytest.raises(Report.ReportLoadError, report.load, db_file)


def test_report_load_badpickle(report):
    """Test report load with a non picklable object."""
    db_file = ".badpickle.obj"
    with open(db_file, "w") as fh:
        fh.write("This is not a pickle.")
    fh.closed
    pytest.raises(Report.ReportLoadError, report.load, db_file)


def test_report_load_nofile(report):
    """Test loading a report with a nonexistent file."""
    db_path = ".noexist.obj"
    pytest.raises(Report.ReportLoadError, report.load, db_path)


class ReportTest(unittest.TestCase):
    """ReportTest defines test cases for Report."""

    def test_create_default_report(self):
        """Test report creation with default params."""
        r = Report()
        self.assertNotEqual(None, r)

    def test_create_report(self):
        """Test report creation with custom params."""
        r = Report("testaccount")
        self.assertEqual("testaccount", r.account)

    def test_add_transaction(self):
        """Test adding a transaction to a report."""
        r = Report("testaccount")
        t = Transaction()
        r.add_transaction(t)
        self.assertEqual(1, len(r.transactions))

    def test_add_transactions(self):
        """Test adding a set of transactions to a report."""
        r = Report("testaccount")
        for i in range(1, 5):
            t = Transaction()
            r.add_transaction(t)
        self.assertEqual(4, len(r.transactions))

    def test_report_default_print(self):
        """Test string representation of Report."""
        r = Report()
        expected_str = """default
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00"""
        self.assertEqual(0, len(r.transactions))
        self.assertEqual(expected_str, str(r))

    def test_report_sum(self):
        """Test report summation."""
        r = Report("testaccount")
        for i in range(1, 5):
            t = Transaction(amt=i)
            r.add_transaction(t)
        self.assertEqual(10, r.sum)

    def test_report_sum_in(self):
        """Test report summation of incoming (positive) transactions."""
        r = Report("testaccount")
        for i in range(1, 5):
            t = Transaction(amt=i)
            r.add_transaction(t)
        self.assertEqual(10, r.sum_in)

    def test_report_sum_out(self):
        """Test report summation of outgoing (negative) transactions."""
        r = Report("testaccount")
        for i in range(1, 5):
            t = Transaction(amt=-i)
            r.add_transaction(t)
        self.assertEqual(-10, r.sum_out)

    def test_report_sum_in_and_out(self):
        """Test report summation of outgoing (negative) transactions."""
        r = Report("testaccount")
        for i in range(1, 5):
            t = Transaction(amt=-i)
            r.add_transaction(t)
        for i in range(1, 5):
            t = Transaction(amt=i)
            r.add_transaction(t)
        # assert summations
        self.assertEqual(-10, r.sum_out)
        self.assertEqual(10, r.sum_in)
        self.assertEqual(0, r.sum)
        # assert transaction counts
        self.assertEqual(4, len(r.trans_in))
        self.assertEqual(4, len(r.trans_out))
        # assert 0 amt transaction goes to trans_in
        r.add_transaction(Transaction())
        self.assertEqual(5, len(r.trans_in))

    def test_report_basic_average(self):
        """Test report average."""
        r = Report("testaccount")
        for i in range(0, 5):
            t = Transaction(amt=i)
            r.add_transaction(t)
            # t = Transaction(amt=-i)
            # r.add_transaction(t)
        self.assertEqual(2, r.avg())

    def test_report_default_average(self):
        """Test report average with 0 transactions."""
        r = Report()
        self.assertEqual(0, r.avg())

    def test_report_negative_average(self):
        """Test report average with negative transactions."""
        r = Report("testaccount")
        for i in range(0, 5):
            t = Transaction(amt=-i)
            r.add_transaction(t)
        self.assertEqual(-2, r.avg())


class TransactionTest(unittest.TestCase):
    """TransactionTest defines test cases for Transaction objects."""

    def test_create_default_transaction(self):
        """Test Transaction creation with defaults."""
        t = Transaction()
        self.assertNotEqual(None, t)

    def test_create_transaction(self):
        """Test Transaction creation with custom inputs."""
        ***REMOVED***
        ***REMOVED***
        ***REMOVED***
        ***REMOVED***
        ***REMOVED***
        pmt_type = "ACH"
        t = Transaction(t_id, date, amt, desc, pmt_type, bal)

        self.assertEqual(t_id, t.t_id)
        self.assertEqual(date, t.date)
        self.assertEqual(float(amt), t.amount)
        self.assertEqual(desc, t.description)
        self.assertEqual(float(bal), t.balance)
        self.assertEqual(pmt_type, t.pmt_type)
        # test blank category
        self.assertEqual("", t.category)

    def test_create_bad_transaction(self):
        """Test Transaction creation with bad inputs."""
        with self.assertRaises(ValueError):
            Transaction(bal="notanumber", amt="alsonotanumber")

    def test_update_category(self):
        """Test updating the category of a Transaction."""
        t = Transaction()
        t.update_category("atm")
        self.assertEqual("atm", t.category)

    @unittest.skip("categorize not quite there yet.")
    def test_categorize_pos(self):
        """Test tranasaction self-catorization funcitonality."""
        t = Transaction(desc="POS Transaction PLACE      LOCATION")
        t.categorize()
        self.assertEqual("POS Transaction", t.type)
        self.assertEqual("PLACE", t.business)
        self.assertEqual("LOCATION", t.locale)

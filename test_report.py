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


def test_report_load_notreport(superreport):
    """Test report load with a non report object."""
    db_file = ".notreport.obj"

    class NotSuperReport():
        pass

    with open(db_file, "w") as fh:
        nr = NotSuperReport()
        pickle.dump(nr, fh)
    fh.closed
    pytest.raises(SuperReport.LoadError, superreport.load, db_file)


def test_report_load_badpickle(superreport):
    """Test report load with a non picklable object."""
    db_file = ".badpickle.obj"
    with open(db_file, "w") as fh:
        fh.write("This is not a pickle.")
    fh.closed
    pytest.raises(SuperReport.LoadError, superreport.load, db_file)


def test_report_load_nofile(superreport):
    """Test loading a report with a nonexistent file."""
    db_path = ".noexist.obj"
    pytest.raises(SuperReport.LoadError, superreport.load, db_path)


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


@pytest.fixture
def report():
    r = Report("testaccount")
    return r


@pytest.fixture
def transaction():
    t = Transaction()
    return t


@pytest.fixture
def report_with_transactions(report):
    # r = Report("testaccount")
    for i in range(1, 5):
        t = Transaction(amt=i)
        report.add_transaction(t)
        t = Transaction(amt=-i)
        report.add_transaction(t)
    return report    


def test_create_default_report(report):
    """Test report creation with default params."""
    assert None != report


def test_account_name(report):
    """Test report creation with custom params."""
    # r = Report("testaccount")
    assert "testaccount" == report.account


def test_add_transaction(report, transaction):
    """Test adding a transaction to a report."""
    report.add_transaction(transaction)
    assert 1 == len(report.transactions)


def test_add_transactions(report):
    """Test adding a set of transactions to a report."""
    for i in range(1, 5):
        t = Transaction()
        report.add_transaction(t)
    assert 4 == len(report.transactions)


def test_empty_report_transactions(report):
    """Test a default report has zero transactions."""
    assert 0 == len(report.transactions)


def test_report_default_print(report):
    """Test string representation of Report."""
    expected_str = """testaccount
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00"""
    assert expected_str == str(report)


def test_report_sum(report_with_transactions):
    """Test report summation."""
    report_with_transactions.add_transaction(Transaction(amt="50.50"))
    assert 50.50 == report_with_transactions.sum


def test_report_sum_in(report_with_transactions):
    """Test report summation of incoming (positive) transactions."""
    assert 10 == report_with_transactions.sum_in


def test_report_sum_out(report_with_transactions):
    """Test report summation of outgoing (negative) transactions."""
    assert -10 == report_with_transactions.sum_out


def test_report_trans_in(report_with_transactions):
    """Test report transactions in."""
    assert 4 == len(report_with_transactions.trans_in)


def test_report_trans_out(report_with_transactions):
    """Test report transactions in."""
    assert 4 == len(report_with_transactions.trans_out)


def test_report_zero_transaction(report):
    """Test amt=0 transaction goes to "in" pile."""
    report.add_transaction(Transaction(amt=0))
    assert 1 == len(report.trans_in)


def test_report_basic_average(report):
    """Test report average."""
    for i in range(0,5):
        report.add_transaction(Transaction(amt=i))
    assert 2 == report.avg()


def test_report_default_average(report):
    """Test report average with 0 transactions."""
    assert 0 == report.avg()


def test_report_negative_average(report):
    """Test report average with negative transactions."""
    for i in range(0, 5):
        t = Transaction(amt=-i)
        report.add_transaction(t)
    assert -2 == report.avg()


class TransactionTest(unittest.TestCase):
    """TransactionTest defines test cases for Transaction objects."""

    def test_create_default_transaction(self):
        """Test Transaction creation with defaults."""
        t = Transaction()
        self.assertNotEqual(None, t)

    def test_create_transaction(self):
        """Test Transaction creation with custom inputs."""
        t_id = "012345678"
        date = "1/1/1999"
        amt = "0000.00000"
        desc = "ACH Deposit BUSINESS  - COMMENT"
        bal = "00000.00000"
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

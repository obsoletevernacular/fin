"""Unit tests for report.py."""
import unittest
from report import Report
from report import Transaction


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
    sum_out: 0.00"""
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
        t = Transaction(date, amt, desc, bal)

        self.assertEqual(date, t.date)
        self.assertEqual(float(amt), t.amount)
        self.assertEqual(desc, t.description)
        self.assertEqual(float(bal), t.balance)
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

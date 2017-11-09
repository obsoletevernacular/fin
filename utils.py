"""Utility functions for fin."""
from report import Transaction
import csv

expected_headers = ['Transaction ID',
                    'Posting Date',
                    'Effective Date',
                    'Transaction Type',
                    'Amount',
                    'Check Number',
                    'Reference Number',
                    'Description',
                    'Transaction Category',
                    'Type',
                    'Balance']


class InvalidCSV(Exception):
    """Raise for improper headers in a CSV file."""

    pass


def csvload(infile):
    """Load an opened csv file and return a list of Transaction() objects."""
    reader = csv.DictReader(infile)
    headers = reader.fieldnames
    if headers != expected_headers:
        raise InvalidCSV("CSV headers don't match: %s" % str(headers))

    ts = []
    for row in reader:
        t_id = row['Reference Number']
        desc = row['Description']
        date = row['Effective Date']
        amt = row['Amount']
        bal = row['Balance']
        pmt_type = row['Type']
        t = Transaction(t_id, date, amt, desc, pmt_type, bal)
        ts.append(t)
    return ts

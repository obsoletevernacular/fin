"""Utility functions for fin."""
from report import Transaction
import csv


def csvload(infile):
    """Load a csv file and return a list of Transaction() objects."""
    ts = []
    try:
        with open(infile, "rw") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t_id = row['Reference Number']
                desc = row['Description']
                date = row['Effective Date']
                amt = row['Amount']
                bal = row['Balance']
                pmt_type = row['Type']
                t = Transaction(t_id, date, amt, desc, pmt_type, bal)
                ts.append(t)
        f.closed
    except Exception:
        return None
    return ts

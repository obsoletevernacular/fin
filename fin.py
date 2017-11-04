#!/usr/bin/env python
"""fin.py."""
from report import Transaction
from report import Report

import csv
import sys


def main():
    """Execute main program function."""
    if len(sys.argv) != 2:
        print("Error: usage: ./fin.py <infile>.csv")
        exit()
    infile = sys.argv[1]

    filename = str.split(infile, "_")
    if len(filename) != 2:
        print("Error: filename must be in the form <account>_<month>.csv")
        exit()
    account = filename[0]

    r = Report(account)
    with open(infile, "rw") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row['Description']
            date = row['Effective Date']
            amt = row['Amount']
            bal = row['Balance']
            t = Transaction(date, amt, desc, bal)
            r.add_transaction(t)
    f.closed
    print(r)


if __name__ == '__main__':
    main()

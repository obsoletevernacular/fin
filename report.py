"""This module defines a Report and Transaction object."""
import pickle


class Report(object):
    """Report is a group of transactions."""

    template = """%s
    transactions: %d
    transactions_in: %d
    transactions_out: %d
    sum: %.2f
    sum_in: %.2f
    sum_out: %.2f
    avg: %.2f"""

    class ReportSaveError(Exception):
        """Raise when report fails to save."""

    class ReportLoadError(Exception):
        """Raise when report fails to load."""

    def __init__(self, account="default"):
        """Report() creates a report."""
        self.transactions = []
        self.trans_in = []
        self.trans_out = []
        self.account = account
        self.sum = 0
        self.sum_in = 0
        self.sum_out = 0

    def add_transaction(self, transaction):
        """Add a new transaction to the report."""
        self.transactions.append(transaction)
        self.sum += transaction.amount
        if transaction.amount >= 0:
            self.sum_in += transaction.amount
            self.trans_in.append(transaction)
        else:
            self.sum_out += transaction.amount
            self.trans_out.append(transaction)

    def avg(self):
        """Calculate the average of all transactions."""
        count = len(self.transactions)
        if count == 0:
            return 0
        return self.sum / count

    def save(self, db=".default.obj"):
        """Save a Report() object to the fs using pickle."""
        try:
            with open(db, "w") as fh:
                pickle.dump(self, fh)
            fh.closed
        except Exception as e:
            raise Report.ReportSaveError(str(e))

    def load(self, db='.default.obj'):
        """Reassign the self from a pickle obj in the fs."""
        try:
            with open(db, "r") as fh:
                r = pickle.load(fh)
            fh.closed
            self.__dict__.update(r.__dict__)
        except Exception as e:
            raise Report.ReportLoadError(str(e))

    def __str__(self):
        """Report string representation."""
        return Report.template % (self.account,
                                  len(self.transactions),
                                  len(self.trans_in),
                                  len(self.trans_out),
                                  self.sum,
                                  self.sum_in,
                                  self.sum_out,
                                  self.avg())


class SuperReport(Report):
    """Enhanced report, moslty a container for several other reports."""

    def __init__(self, name="summary"):
        """Build a superreport."""
        super(SuperReport, self).__init__(name)
        self.reports = []

    def add_report(self, r):
        """Add a sub-report to the report."""
        self.reports.append(r)
        for t in r.transactions:
            self.add_transaction(t)

    def __str__(self):
        """Representation for SuperReport."""
        r0 = ""
        for r in self.reports:
            r0 += str(r)
            r0 += "\n"
        r1 = "%d files processed. summary report below:" % len(self.reports)
        r2 = super(SuperReport, self).__str__()
        rep = "%s%s\n%s" % (r0, r1, r2)
        return rep


class Transaction(object):
    """Transaction is a record of a single transaction."""

    def __init__(self, t_id="0",
                 date="1/1/1993",
                 amt=0.0,
                 desc="empty",
                 pmt_type="none",
                 bal=0.0):
        """Transaction() creates a new transaction record."""
        super(Transaction, self).__init__()
        self.t_id = t_id
        self.date = date
        self.amount = float(amt)
        self.description = desc
        self.balance = float(bal)
        self.pmt_type = pmt_type
        self.category = ""

    def update_category(self, category=""):
        """Update the category for a transaction."""
        self.category = category

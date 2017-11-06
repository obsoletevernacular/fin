# fin

Simple personal finance manager. Attempts to provide basic analysis from sets of
exported transactions.

## Usage

### Importing transactions:

Transactions can be imported from csv files and stored to python object files
for later retrieval (analysis).

```
$ fin import --db myreport.obj infile1.csv infile2.csv
```

Inputs:

* `db` location to store objects, defaults to `.default.obj`
* `INFILES` files to load

**A note** on CSV formatting: `fin` will reject any csv file without these headers:
```
"Transaction ID"
"Posting Date"
"Effective Date"
"Transaction Type"
"Amount"
"Check Number"
"Reference Number"
"Description"
"Transaction Category"
"Type"
"Balance""Transaction ID"
"Posting Date"
"Effective Date"
"Transaction Type"
"Amount"
"Check Number"
"Reference Number"
"Description"
"Transaction Category"
"Type"
"Balance"
```

### Retrieving Transactions

A stored group of transactions can be retrieved from a stored file:

```
$ fin load --db myreport.obj
```

Inputs:

* `db` location to store objects, defaults to `.default.obj`


### Basic Reports

Basic reports can be generated from csv files containing transactions using the
`fin report` subcommand. Any number of files are allowed. For each file a report
will be generated, and additionally a summary report will be outputted.

Files are expected to be in the format `<account>_<timeframe>.csv` but it's not
exactly enforced - it just makes output nicer.

For example:

```
$ fin report credit_nov.csv savings_nov.csv checking_nov.csv
checking_nov
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00
credit_nov
    transactions: 0
    transactions_in: 0
    transactions_out: 0
    sum: 0.00
    sum_in: 0.00
    sum_out: 0.00
    avg: 0.00
savings_nov
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
    avg: 0.00
```

The interface here is geared towards csv files downloaded from an online banking
site. This makes it easy to do something like `fin report bank/2017/*_jan.csv`
to get a report of all transactions from January 2017.



## Dev Setup


### virtualenv

Virtualenv and setuptools are used to manage dependencies and setup. Make sure
both are installed:

```
$ pip install setuptools virtualenv
```

Next you can setup a new virtualenv:

```
$ virtualenv venv
```

And activate it to enter the venv:

```
$ . venv/bin/activate
```

Next use `pip` to setup the environment:

```
$ pip install --editable .
```

### Running Tests

Unit tests for each module are provided in `test_<module>.py` with use of the
`unittest` library. For integration with setuptools, and to provide a transition
to `pytest` down the road, `pytest` is marked as a dependency in `setup.py`.
Until the tests are re-written using `pytest` we can make use of integraion with
`unittest`.

```
(venv) ❯ pytest
================================================== test session starts ==================================================
platform darwin -- Python 2.7.10, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
rootdir: /Users/ggreving/gh/ggreving/fin, inifile:
collected 22 items

test_fin.py .
test_report.py ................
test_utils.py .....

=============================================== 22 passed in 0.06 seconds ===============================================

```

### Test Files

Test files are locate in `testfiles/` - these are used as inputs/outputs to
assist unittesting. By convention any file with the extension `.test` is an
*input* (for example a test `.csv` input file), and any `.golden` file is an
*output*, for example expected output of a particular command. Also by
convention, testfile names should correspond to a particular test function, and
should contain some information about what is being tested.

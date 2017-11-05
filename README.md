# fin

## Usage

### Basic Reports

Basic reports can be generated from csv files containing transactions using the
`fin report` subcommand. Any number of files are allowed. For each file a report
will be generated, and additionally a summary report will be outputted.

Files are expected to be in the format `<account>_<timeframe>.csv` but it's not
exactly enforced - it just makes output nicer.

For example:

```
fin report credit_nov.csv savings_nov.csv checking_nov.csv
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

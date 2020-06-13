"""fin.py."""
import click
# from report import Report
# from report import SuperReport
# import utils
import os.path as path
import re
import pandas as pd

import dateutil
from datetime import datetime

@click.group()
def fin():
    """Manage personal finances, simply."""
    pass

def process_file(f):
    df = pd.read_csv(f, skiprows=0)
    try:
        account = path.basename(f.name).split('.')[0]
    except Exception:
        account = f.name
    for acct in ["checking", "credit", "savings"]:
        if acct in account:
            account = acct
            break
    if account == "":
        raise ValueError("Invalid Filename. Must contain one of: checking, savings, or credit.")
    # set the account name for all the records
    df['account'] = account
    df.index = pd.DatetimeIndex(df['Effective Date'].apply(dateutil.parser.parse))
    return df

@click.command("import")
@click.argument('infiles', type=click.File('r'), nargs=-1, required=True)
@click.option('--db', default=".dataframe.pkl", type=click.Path())
@click.pass_context
def import_transactions(ctx, infiles, db):
    """Import a set of transactions from csv files."""
    # superreport = SuperReport("summary")
    if path.exists(db):
        df = pd.read_pickle(db)
    else:
        df = pd.DataFrame()

    orig_rows = df.shape[0]
    frames = [df]
    for f in infiles:
        try:
            df = process_file(f)
        except ValueError as e:
             ctx.fail(e)
        frames.append(df)

    df = pd.concat(frames)
    df.index = pd.DatetimeIndex(df['Effective Date'].apply(dateutil.parser.parse))
    processed_rows = df.shape[0] - orig_rows
    df.drop_duplicates(inplace=True)
    df.sort_index(inplace=True)
    pd.to_pickle(df,db)

    click.echo("%d files processed and stored to %s" % (len(infiles), db))
    click.echo("%d rows processed, %d rows added" % (processed_rows, df.shape[0] - orig_rows))
    click.echo("total rows: %d" % (df.shape[0]))

    print(df)


fin.add_command(import_transactions)

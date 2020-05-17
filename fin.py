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
    frames = []
    for f in infiles:
        df = pd.read_csv(f, skiprows=0)
        try:
            account = path.basename(f.name).split('.')[0]
        except Exception:
            account = f.name
        for acct in ["checking", "credit", "savings"]:
            if acct in account:
                account = acct
                break
        else:
            ctx.fail("Invalid filename: %s" % account)
        # set the account name for all the records
        df['account'] = account
        df.index = pd.DatetimeIndex(df['Effective Date'].apply(dateutil.parser.parse))
        frames.append(df)

    df = pd.concat(frames)
    df.index = pd.DatetimeIndex(df['Effective Date'].apply(dateutil.parser.parse))
    processed_rows = df.shape[0]
    df.drop_duplicates(inplace = True)
    df.reset_index(drop=True)
    pd.to_pickle(df,db)

    click.echo("%d files processed and stored to %s" % (len(infiles), db))
    click.echo("%d rows processed, %d rows added" % (processed_rows, df.shape[0] - orig_rows))

@click.command()
@click.pass_context
@click.option('--db', default=".default.obj", type=click.Path(exists=True))
def load(ctx, db):
    """Load and display a stored report."""
    click.echo("Generating a report from %s" % db)
    try:
        r = SuperReport()
        r.load(db)
        click.echo(r)
    except SuperReport.LoadError as e:
        ctx.fail("Failed to load db %s:" % db)
    except Exception as e:
        ctx.fail(e)


@click.command()
@click.pass_context
@click.option('--db', default=".dataframe.pkl", type=click.Path(exists=True))
def report(ctx, db):
    """Generate a basic report from the loaded dataframe.
    """
    try:
        df = pd.read_pickle(db)
        click.echo(df.head(10))
    except Exception as e:
        ctx.fail(e) 

@click.command()
@click.pass_context
@click.option('--db', default=".dataframe.pkl", type=click.Path(exists=True))
@click.argument('searchstr', type=click.STRING)
def search(ctx, db, searchstr):
    """Search a report for transactions containing a string."""
    try:
        df = pd.read_pickle(db)
        results = df[df['Description'].str.contains(searchstr)]

        click.echo("matched %d transactions" % results.shape[0])
    except Exception as e:
        ctx.fail(e) 

fin.add_command(import_transactions)
fin.add_command(report)
fin.add_command(load)
fin.add_command(search)
"""fin.py."""
import click
# from report import Report
# from report import SuperReport
# import utils
import os.path as path
import re
import pandas as pd


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

    orig_rows = df.size
    frames = []
    for f in infiles:
        df = pd.read_csv(f, skiprows=0)
        try:
            account = path.basename(f.name).split('.')[0]
        except Exception:
            account = f.name
        if re.search("'checking'|'savings'|'credit'", account):
            ctx.fail("Invalid filename: %s" % account)
        # set the account name for all the records
        df['account'] = account
        frames.append(df)

    df = pd.concat(frames)
    processed_rows = df.size
    df.drop_duplicates(inplace = True, ignore_index=True)
    pd.to_pickle(df,db)
    click.echo("%d files processed and stored to %s" % (len(infiles), db))
    click.echo("%d rows processed, %d rows added" % (processed_rows,df.size - orig_rows))

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
@click.argument('infiles', type=click.File('r'), nargs=-1, required=True)
@click.pass_context
def report(ctx, infiles):
    """Generate a basic report from a group of csv files.

    INFILES - <account>_<timeframe>.csv ...
    """
    s = SuperReport()
    for f in infiles:
        try:
            ts = utils.csvload(f)
        except utils.InvalidCSV as e:
            ctx.fail("Failed to load %s: %s" % (f, str(e)))
        try:
            account = path.basename(f.name).split('.')[0]
        except Exception:
            account = f.name
        r = Report(account)
        for t in ts:
            r.add_transaction(t)
        s.add_report(r)
    click.echo(s)


@click.command()
@click.pass_context
@click.option('--db', default=".default.obj", type=click.Path(exists=True))
@click.argument('searchstr', type=click.STRING)
def search(ctx, db, searchstr):
    """Search a report for transactions containing a string."""
    try:
        r = SuperReport()
        r.load(db)
        found = r.search(searchstr)
        for t in found.transactions:
            print(t)
        print(found)

    except SuperReport.LoadError as e:
        ctx.fail("Failed to load db %s:" % db)
    except Report.SearchFailed as e:
        ctx.exit("No transactions found.")
    except Exception as e:
        ctx.fail(e) 

fin.add_command(import_transactions)
fin.add_command(report)
fin.add_command(load)
fin.add_command(search)
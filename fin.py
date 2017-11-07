"""fin.py."""
import click
from report import Report
from report import SuperReport
import utils
import os.path as path


@click.group()
def fin():
    """Manage personal finances, simply."""
    pass


@click.command("import")
@click.argument('infiles', type=click.File('r'), nargs=-1, required=True)
@click.option('--db', default=".default.obj", type=click.Path())
@click.pass_context
def import_transactions(ctx, infiles, db):
    """Import a set of transactions from csv files."""
    superreport = SuperReport("summary")
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
        superreport.add_report(r)
    try:
        superreport.save(db)
    except Report.ReportSaveError as e:
        ctx.fail("Failed to save transactions to %s" % db)
    except Exception as e:
        ctx.fail(e)

    click.echo("%d files processed and stored to %s" % (len(infiles), db))
    click.echo(superreport)


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
    except Report.ReportLoadError as e:
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


fin.add_command(import_transactions)
fin.add_command(report)
fin.add_command(load)

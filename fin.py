#!/usr/bin/env python
"""fin.py."""
import click
from report import Report
import utils
import os.path as path


@click.group()
def cli():
    """Manage personal finances, simply."""
    pass


@click.command()
@click.argument('infiles', type=click.File('r'), nargs=-1)
@click.pass_context
def report(ctx, infiles):
    """Generate a basic report from a csv file."""
    report = Report("summary")
    rs = []
    if len(infiles) == 0:
        ctx.fail("No files given.")
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
            report.add_transaction(t)
        rs.append(r)
    for r in rs:
        click.echo(r)
    click.echo("%d files processed. summary report below:" % len(rs))
    click.echo(report)


cli.add_command(report)

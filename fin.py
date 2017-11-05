#!/usr/bin/env python
"""fin.py."""
import click
from report import Report
import utils


@click.group()
def cli():
    """Manage personal finances, simply."""
    pass


@click.command()
@click.argument('infiles', type=click.File('r'), nargs=-1)
@click.pass_context
def report(ctx, infiles):
    """Generate a basic report from a csv file."""
    report = Report("autoreport")
    if len(infiles) == 0:
        ctx.fail("No files given.")
    for f in infiles:
        try:
            ts = utils.csvload(f)
        except utils.InvalidCSV as e:
            ctx.fail("Failed to load %s: %s" % (f, str(e)))
        for t in ts:
            report.add_transaction(t)
    click.echo(report)


cli.add_command(report)

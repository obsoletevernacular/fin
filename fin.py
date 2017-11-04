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
@click.argument('infile', type=click.File('r'))
@click.pass_context
def report(ctx, infile):
    """Generate a basic report from a csv file."""
    r = Report()
    try:
        ts = utils.csvload(infile)
    except utils.InvalidCSV as e:
        ctx.fail("Failed to load %s: %s" % (infile, str(e)))
    for t in ts:
        r.add_transaction(t)
    click.echo(r)


cli.add_command(report)

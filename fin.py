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
@click.argument('infile', type=click.File('rb'))
def report(infile):
    """Generate a basic report from a csv file."""
    r = Report()
    ts = utils.csvload(infile)
    for t in ts:
        r.add_transaction(t)
    click.echo(r)


cli.add_command(report)

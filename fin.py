#!/usr/bin/env python
"""fin.py."""
import click
from report import Report
import utils

import sys


@click.command()
def cli():
    """Cli entrypoint for fin cli application."""
    click.echo('Hello Fin.')
    r = Report("blank")
    ts = utils.csvload("test.csv")
    if ts is None:
        sys.exit(-1)
    for t in ts:
        r.add_transaction(t)

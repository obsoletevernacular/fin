"""Unit tests for utils.py."""
import pytest
import os

import utils
from report import Transaction


@pytest.fixture()
def csvload_happy():
    """Test fixture for csvload - happ path."""
    csvload_happy = os.path.join(os.getcwd(), "testfiles/csvload_happy.test")
    ts = []
    with open(csvload_happy, "r") as f:
        ts = utils.csvload(f)
    f.closed
    return ts

def test_csvload_happy_size(csvload_happy):
    assert 2 == len(csvload_happy)
    """Test csvload happy path."""


def test_csvload_happy_transaction(csvload_happy):
    for t in csvload_happy:
        assert isinstance(t, Transaction)


def test_csvload_unopened_file():
    """Test csvload with an unopened file."""
    pytest.raises(utils.InvalidCSV, utils.csvload,
                      "testfiles/csvload_happy.test")


def test_csvload_notacsv():
    """Test csvload with non-csv file."""
    pytest.raises(utils.InvalidCSV, utils.csvload,
                      "testfiles/csvload_notacsv.test")


def test_csvload_invalidfieldscsv():
    """Test csvload with a csv file with invalid field headers."""
    pytest.raises(utils.InvalidCSV, utils.csvload,
                      "testfiles/csvload_invalidfieldscsv.test")


def test_csvload_nodescriptioncsv():
    """Test csvload with a csv file with poorly formatted rows."""
    pytest.raises(utils.InvalidCSV, utils.csvload,
                      "testfiles/csvload_nodescriptioncsv.test")

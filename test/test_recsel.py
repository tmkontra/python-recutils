import pytest
from click.testing import CliRunner

from recutils import parse
from recutils.parse import FileParser

from common import resource_path

from recutils.commands.recsel import recsel

database = resource_path("stations.rec")
db_filepath = str(database)


def test_recsel():
    runner = CliRunner()
    result = runner.invoke(recsel, [db_filepath])
    assert result.exit_code == 0

def test_recsel_include_descriptors():
    runner = CliRunner()
    result = runner.invoke(recsel, [db_filepath, "--include-descriptors"])
    assert result.exit_code == 0

def test_recsel_collapse():
    runner = CliRunner()
    result = runner.invoke(recsel, [db_filepath, "--collapse"])
    assert result.exit_code == 0

def test_recsel_sort():
    runner = CliRunner()
    result = runner.invoke(recsel, [db_filepath, "--sort", "Name"])
    assert result.exit_code == 0

def test_recsel_random():
    runner = CliRunner()
    result = runner.invoke(recsel, [db_filepath, "--random", 0])
    assert result.exit_code == 0
    result = runner.invoke(recsel, [db_filepath, "--random", 2])
    assert result.exit_code == 0
    
    

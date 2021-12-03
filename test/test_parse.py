import pytest

from recutils import parse
from recutils.parse import FileParser

from common import resource_path

def _parser(fn):
    return FileParser(resource_path(fn))

def test_valid_parse():
    fn = "stations.rec"
    record_count = 2
    records = list(_parser(fn).get_db().all_records)
    assert len(records) == record_count

def test_invalid_parse():
    fn = "invalid.rec"
    with pytest.raises(parse.RecfileSyntaxError):
        _parser(fn).get_db()

def test_parse_type():
    fn = "single_type.rec"
    record_count = 2
    records = list(_parser(fn).get_db().all_records)
    assert len(records) == record_count

def test_parse_anonymous_with_type():
    fn = "anonymous_type.rec"
    record_count = 3
    records = list(_parser(fn).get_db().all_records)
    assert len(records) == record_count
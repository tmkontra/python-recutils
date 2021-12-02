from recutils import parse

from common import resource_path

def test_valid_parse():
    fn = "stations.rec"
    record_count = 2
    records = list(parse.FileParser(resource_path(fn)).get_db().all_records)
    assert len(records) == record_count
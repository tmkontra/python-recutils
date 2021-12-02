from . import parse
from .db import RecDb


class SelectionError(Exception):
    pass


class Select:
    def __init__(self, db: RecDb, typ=None, sexes=None, indexes=None, random=None):
        self._db = db
        self._typ = typ
        self._sexes = sexes or []
        self._indexes = indexes
        
    @property
    def by_type(self):
        return self._typ
        
    @property
    def records(self):
        if self._typ:
            recs = self._db.of_type(self._typ)
        else:
            recs = self._db.all_records
        for filtr in self._sexes:
            recs = filter(filtr, recs)
        return list(recs)
    
    @property
    def stdout(self):
        records = self.records
        for record in records[:-1]:
            for field in record:
                yield field.stdout
                yield "\n"
            yield "\n"
        for field in records[-1]:
            yield field.stdout
            yield "\n"
    


if __name__ == "__main__":
    import sys
    db = parse.FileParser(sys.argv[1]).get_db()
    select = Select(db)
    records = select.records
    for line in select.stdout:
        print(line, end="")
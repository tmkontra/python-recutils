import enum
from . import parse
from .db import RecDb


class SelectionError(Exception):
    pass


class Select:
    def __init__(self, db: RecDb, 
        typ=None, sexes=None, 
        indexes=None, random=None, 
        include_descriptors=False,
        collapse=False
    ):
        if db.multiple_types and typ is None:
            raise ValueError("several record types found! please specify a type.")
        self._db = db
        self._typ = typ
        self._sexes = sexes or []
        self._indexes = indexes
        self._include_descriptors = include_descriptors
        self._record_separator = "" if collapse else "\n"
        
    @property
    def by_type(self):
        return self._typ
        
    @property
    def records(self):
        if self._typ:
            recs = self._db.of_type(self._typ)
        else:
            recs = self._db.all_records
        filters = []
        filters.extend(self._sexes)
        for filtr in filters:
            recs = filter(filtr, recs)
        if self._indexes:
            return [
                r for i, r in enumerate(recs) if i in self._indexes
            ]
        else:
            return list(recs)
    
    @property
    def stdout(self):
        if self._include_descriptors:
            for line in self._db.types_by_name[self._typ].lines:
                yield line
                yield  "\n"
            yield "\n"
        records = self.records
        for record in records[:-1]:
            for field in record:
                yield field.stdout
                yield "\n"
            yield self._record_separator
        for field in records[-1]:
            yield field.stdout
            yield "\n"

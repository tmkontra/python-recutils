import enum
import random

from . import parse
from .db import RecDb


class SelectionError(Exception):
    pass


class Select:
    def __init__(self, db: RecDb, 
        typ=None, sexes=None, 
        indexes=None, random: int = None, 
        include_descriptors=False,
        collapse=False
    ):
        if db.multiple_types and typ is None:
            raise ValueError("several record types found.  Please use -t to specify one")
        self._db = db
        self._typ = typ
        self._sexes = sexes or []
        self._indexes = indexes
        self._random = random
        self._include_descriptors = include_descriptors
        self._record_separator = "" if collapse else "\n"
        self._records = None
        
    @property
    def by_type(self):
        return self._typ

    def random_indices(self, count):
        if self._random == 0:
            return [i for i in range(count)]
        else:
            population = [i for i in range(count)]
            choices = random.sample(population, k=self._random)
            return choices
        
    @property
    def records(self):
        if self._records is not None:
            return self._records
        if self._typ:
            recs = self._db.of_type(self._typ)
        else:
            recs = self._db.all_records
        if self._random is not None:
            indices = self.random_indices(len(recs))
            recs = [
                r for i,r in enumerate(recs) if i in indices
            ]
        else: # random and SEXPRS are mutually exclusive
            filters = []
            filters.extend(self._sexes)
            for filtr in filters:
                recs = filter(filtr, recs)
        if self._indexes:
            self._records = [
                r for i, r in enumerate(recs) if i in self._indexes
            ]
        else:
            self._records = list(recs)
        return self._records
    
    @property
    def stdout(self):
        if self._include_descriptors:
            if self._typ:
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

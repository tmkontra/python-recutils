import itertools


class RecDb:
    def __init__(self, records: dict):
        self._records = records
        
    def of_type(self, type_name):
        typ = self.types_by_name[type_name]
        return self._records.get(typ)
        
    @property
    def all_records(self):
        return itertools.chain.from_iterable(self._records.values())
        
    @property
    def types(self):
        return [t for t in self._records.keys() if t is not None]
    
    @property
    def types_seen(self):
        return [t.name for t in self.types]
    
    @property
    def types_by_name(self):
        return {t.name: t for t in self.types}
        
    def has_type(self, type_name):
        return type_name in self.types_seen
        
    def insert(self, record, typ=None):
        if typ:
            self.of_type(typ).append(record)
        else:
            self._records[None].append(record)
    
    def write(self, filename):
        with open(filename, "w") as f:
            for record in self._records[None]:
                self.write_record(f, record)
                f.write("\n")
            for t in self.types:
                for line in t.lines:
                    f.write(line)
                    f.write("\n")
                f.write("\n")
                for record in self._records[t]:
                    self.write_record(f, record)
                    f.write("\n")
        
    @staticmethod
    def write_record(f, record):
        for field in record:
            f.write(field.stdout)
            f.write("\n")
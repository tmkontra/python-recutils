import re
from .db import RecDb


class RecfileSyntaxError(Exception):
    pass

class Field:
    _name_regex = re.compile(
        r"^[a-zA-Z%][a-zA-Z0-9_]*$")

    def __init__(self, name, value):
        if not self._name_regex.match(name):
            raise RecfileSyntaxError("Invalid field name: {}".format(name))
        self._name = name
        self._value = value
        
    def __repr__(self):
        return str(self._value)
        
    @property
    def stdout(self):
        return "{}: {}".format(self._name, self._value)

class Record:
    def __init__(self, fields, descriptor=None):
        if not fields:
            raise ValueError("Got record with no fields")
        self._fields = fields
        self._desc = descriptor
    
    @property
    def descriptor(self):
        return self._desc
        
    def __repr__(self):
        if self._desc:
            return "<{} {}>".format(self._desc.name, self._fields[0])
        else:
            return "<%DefaultRec {}>".format(self._fields[0])
        
    def __iter__(self):
        yield from self._fields
        
class RecordDescriptor:
    def __init__(self, rec, **properties):
        self._rec = rec
        self._properties = properties or {}
        
    def put(self, key, val):
        self._properties[key] = val
    
    @property
    def name(self):
        return self._rec
    
    def __repr__(self):
        return "<Desc {}>".format(self.name)
        
    @property
    def lines(self):
        yield "%rec: {}".format(self.name)
        for prop, val in self._properties.items():
            yield "{}: {}".format(prop, val)
        
class BaseParser:
    def __init__(self):
        self._closed = False
        self._records = {None: []}
        self._next_fields = []
        self._next_desc = None
        self._desc = None
        self._line_no = 1
        
    @property
    def lines(self):
        raise NotImplementedError

    @property
    def types(self):
        return self._records.keys()
    
    @property
    def types_seen(self):
        return [t.name for t in self.types if t is not None]
        
        
    def has_type(self, type_name):
        return type_name in self.types_seen
    
    @property
    def records(self):
        return self._records
    
    def parse_line(self, line):
        line = line.strip()
        if line.startswith("#"):
            pass
        elif line.startswith("%rec"):
            _, typ = line.split(":")
            typ = typ.strip()
            if typ not in self._records:
                self._next_desc = RecordDescriptor(typ)
            else:
                raise RecfileSyntaxError("Got record type {} twice".format(typ))
        elif not line:
            if self._next_desc:
                self._desc = self._next_desc
                self._records[self._desc] = []
                self._next_desc = None
            elif self._next_fields:
                self._flush_record()
        else:
            key, val = line.split(":")
            if self._next_desc:
                self._next_desc.put(key.strip(), val.strip())
            else:
                self._next_fields.append(Field(key.strip(), val.strip()))
        self._line_no += 1
    
    def _flush_record(self):
        self._records[self._desc].append(Record(self._next_fields, descriptor=self._desc))
        self._next_fields = []
        
    def advance(self):
        try:
            self.parse_line(next(self.lines))
        except StopIteration:
            self._flush_record()
            self._close()
        
    def get_db(self):
        self._open()
        while not self._closed:
            self.advance()
        return RecDb(self.records)
    
    def _close(self):
        self._closed = True
        
    
class FileParser(BaseParser):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename
        self._file = None
        
    @property
    def lines(self):
        return self._file
        
    def _open(self):
        if self._file is None and not self._closed:
            self._file = open(self._filename, "r")

    def _close(self):
        if self._file is not None:
            self._file.close()
            super()._close()
            

if __name__ == "__main__":
    import sys
    db = FileParser(sys.argv[1]).get_db()
    print(db)

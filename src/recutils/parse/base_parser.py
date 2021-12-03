import re
from ..db import RecDb

from .exceptions import RecfileSyntaxError
from .field import Field
from .record import Record
from .descriptor import RecordDescriptor


        
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
                try:
                    self._next_fields.append(Field(key.strip(), val.strip()))
                except ValueError as e:
                    raise RecfileSyntaxError(str(e))
        self._line_no += 1
    
    def _flush_record(self):
        try:
            self._records[self._desc].append(Record(self._next_fields, descriptor=self._desc))
        except ValueError as e:
            msg = str(e) + " at line {}".format(self._line_no)
            raise RecfileSyntaxError(msg)
        self._next_fields = []
        
    def advance(self):
        try:
            self.parse_line(next(self.lines))
        except StopIteration:
            try:
                self._flush_record()
            except RecfileSyntaxError: # end of file, no record pending
                pass
            self._close()
        
    def get_db(self):
        self._open()
        while not self._closed:
            self.advance()
        return RecDb(self.records)
    
    def _close(self):
        self._closed = True

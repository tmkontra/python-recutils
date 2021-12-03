
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
        
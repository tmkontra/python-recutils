

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
from . import parse
import pdb

class Insert:
    def __init__(self, db):
        self._db = db
        
    def insert(self, fields, typ=None):
        if typ:
            if not self._db.has_type(typ):
                raise Exception("No type '{}'".format(self.typ))
            self._db.insert(parse.Record(fields, descriptor=typ))
        else:
            self._db.insert(parse.Record(fields))
    
    def write(self, filename):
        self._db.write(filename)
        
if __name__ == "__main__":
    import sys
    db = parse.FileParser(sys.argv[1]).get_db()
    ins = Insert(db)
    ins.insert([parse.Field("Id", 101)])
    ins.write(sys.argv[1])
    
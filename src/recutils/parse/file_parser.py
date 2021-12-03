from .base_parser import BaseParser

class FileParser(BaseParser):
    def __init__(self, filepath):
        super().__init__()
        self._filename = filepath
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
            

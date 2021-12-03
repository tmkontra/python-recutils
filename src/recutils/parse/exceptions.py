
class RecfileSyntaxError(Exception):
    def __init__(self, msg, line_no=None):
        self.msg = msg
        self.line_no = line_no
        super().__init__(msg)
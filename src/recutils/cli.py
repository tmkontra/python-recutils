import sys

from . import parse
from .select import Select
from .commands import recsel

def main():
    args = sys.argv
    fn = args[1]
    try:
        db = parse.FileParser(fn).get_db()
        select = Select(db)
        for line in select.stdout:
            print(line, end="")
    except parse.RecfileSyntaxError as e:
        print(f"{fn}: {e.line_no}: error: {str(e)}")

if __name__ == "__main__":
    recsel.recsel()
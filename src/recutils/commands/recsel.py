import click

from ..commands import ArgumentError
from ..select import Select
from ..parse import FileParser

@click.command()
# global options
@click.option("-d", "--include-descriptors", is_flag=True) # YES
@click.option("-C", "--collapse", is_flag=True) # YES
@click.option("-S", "--sort") # no
@click.option("-G", "--group-by") # no
@click.option("-U", "--uniq", is_flag=True) # no
# select options
@click.option("-n", "--number") # YES
@click.option("-e", "--expression", multiple=True) # no
@click.option("-q", "--quick") # no
@click.option("-m", "--random") # no
@click.option("-t", "--type") # no
@click.option("-j", "--field") # no
# output options
@click.option("-p", "--print") # no
@click.option("-P", "--print-value") # no
@click.option("-R", "--print-row") # no
@click.option("-c", "--count") # no
@click.option("--print-sexps") # no
@click.argument("recfile", type=click.Path(exists=True))
def recsel(recfile, **kwargs):
    indexes = kwargs.pop("number")
    if indexes:
        indexes = [int(i) for i in indexes.split(",")]
    expressions = kwargs.pop("expression")
    random = kwargs.pop("random")
    typ = kwargs.pop("type")
    if expressions and indexes:
        raise ArgumentError("cannot specify -n and also -e")
    if random and indexes:
        raise ArgumentError("cannot specify -m and also -n")
    include_descriptors = kwargs.pop("include_descriptors")
    collapse = kwargs.pop("collapse")
    db = FileParser(recfile).get_db()
    select = Select(db, indexes=indexes, typ=typ, include_descriptors=include_descriptors, collapse=collapse)
    for line in select.stdout:
        print(line, end="")
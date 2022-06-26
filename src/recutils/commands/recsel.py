from io import UnsupportedOperation
from itertools import groupby
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
@click.option("-m", "--random", type=int) # yes
@click.option("-t", "--type") # yes
@click.option("-j", "--field") # WIP
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
    expression = kwargs.pop("expression")
    if expression: # TODO  
        raise UnsupportedOperation("expressions")
    random = kwargs.pop("random")
    typ = kwargs.pop("type")
    field = kwargs.pop("field") # WIP!
    if field: # TODO  
        raise UnsupportedOperation("field")
    if expression and indexes:
        raise ArgumentError("cannot specify -n and also -e")
    if random and indexes:
        raise ArgumentError("cannot specify -m and also -n")
    include_descriptors = kwargs.pop("include_descriptors")
    collapse = kwargs.pop("collapse")
    sort = kwargs.pop("sort")
    if sort: # TODO  
        raise UnsupportedOperation("sort") 
    group_by = kwargs.pop("group_by")
    if group_by: # TODO  
        raise UnsupportedOperation("group by") 
    unique = kwargs.pop("uniq")
    if unique: # TODO  
        raise UnsupportedOperation("unique")
    quick = kwargs.pop("quick")
    if quick: # TODO  
        raise UnsupportedOperation("quick")
    print_arg = kwargs.pop("print")
    if print_arg: # TODO  
        raise UnsupportedOperation("print")
    print_value = kwargs.pop("print_value")
    if print_value: # TODO  
        raise UnsupportedOperation("print_value")
    print_row = kwargs.pop("print_row")
    if print_row: # TODO  
        raise UnsupportedOperation("print_row")
    count = kwargs.pop("count")
    if count: # TODO  
        raise UnsupportedOperation("count")
    print_sexps = kwargs.pop("print_sexps")
    if print_sexps: # TODO  
        raise UnsupportedOperation("print_sexps")

    db = FileParser(recfile).get_db()
    select = Select(db, 
        indexes=indexes, typ=typ, 
        include_descriptors=include_descriptors, 
        collapse=collapse,
        random=random
        )
    for line in select.stdout:
        print(line, end="")

if __name__ == "__main__":
    recsel()
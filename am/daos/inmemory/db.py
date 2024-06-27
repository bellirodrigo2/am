""" In Memory Database """
from typing import Generator, Any
from contextlib import contextmanager

from treelib import Tree

################################################################################

def bootstrap(filename: str | None = None): #, **kwargs):
    
    filename = filename or 'MemoryTree'
    tree = Tree(identifier=filename)
    # tree.create_node(tag='root')
    return tree

@contextmanager
def get_memory_db(tree: Tree)->Generator[Tree, Any, None]:
    """ """
    
    try:
        yield tree
    finally:
        pass


if __name__ == '__main__':

    tree = bootstrap()
    with get_memory_db(tree) as db:
        one = db.create_node(tag='one')
        db.create_node(tag='two', parent=one)
        print(db)
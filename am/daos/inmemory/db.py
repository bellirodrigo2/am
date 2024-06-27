""" In Memory Database """

from contextlib import contextmanager
from typing import Any, Generator

from treelib import Tree

###############################################################################


def bootstrap(filename: str | None = None):  # , **kwargs):

    tree = Tree(identifier=filename or "treeExample")
    return tree


@contextmanager
def get_memory_db(tree: Tree) -> Generator[Tree, Any, None]:
    """ """

    try:
        yield tree
    finally:
        pass


if __name__ == "__main__":
    pass
    # tree = bootstrap()
    # with get_memory_db(tree) as db:
    #     one = db.create_node(tag='one')
    #     db.create_node(tag='two', parent=one)
    #     print(db)

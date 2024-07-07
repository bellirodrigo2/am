""""""

from enum import Enum

from sqlalchemy import Table

from am.getobj import get_obj_class_iter, lower_name, upper_name
from am.interfaces import LabelInterface
from am.repo.sql.interfaces import ClosureTable, LabelTable

# from am.repo.sql.maketable import make_foreign, make_primary, make_table

tables: dict[str, Table] = {}

str_transf = lower_name

# make_label e add to tables
# make_tree e add to tables

# make the closure tree table e add to tables

for cls in get_obj_class_iter():

    name, objcls = cls
    # make obj table here

TableEnum = Enum("TableEnum", {upper_name(x): lower_name(x) for x in tables.keys()})


def get_obj_class(name: str | Enum) -> Table:

    key = name if isinstance(name, str) else name.name
    return tables[str_transf(key)]

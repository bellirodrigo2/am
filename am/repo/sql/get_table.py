""""""

from sqlalchemy import Table

from am.getobj import get_obj_class, get_obj_class_iter
from am.interfaces import LabelInterface
from am.repo.sql.interfaces import ClosureTable, LabelTable

# from am.repo.sql.maketable import make_foreign, make_primary, make_table

tables: dict[str, Table] = {}

for field in LabelInterface.__annotations__:
    # make the label table here
    ...

# make the closure tree table here

for cls in get_obj_class_iter():
    class_ = get_obj_class[cls]
    # make sql table here

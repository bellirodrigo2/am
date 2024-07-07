""""""

from sqlalchemy import Column, Index, Integer, MetaData, String, Table

from am.repo.sql.maketable import make_foreign, make_primary

meta = MetaData()

label = Table(
    "label",
    meta,
    make_primary("webid", String(32)),
    Column("name", String(64)),  # TODO FAZER DINAMICO A PARTIR DA INTERFACE LABEL
    Column("description", String(256)),
    Column("clientid", String(32)),
)

link = Table(
    "link",
    meta,
    make_foreign("label", "webid", "parent", String(32), True),
    make_foreign("label", "webid", "child", String(32), True),
    Column("depth", Integer),
    extend_existing=True,
)
Index("tree_idx", link.c.parent, link.c.depth, link.c.child, unique=True)
Index("tree_idx2", link.c.child, link.c.parent, link.c.depth, unique=True)


# make the closure tree table e add to tables

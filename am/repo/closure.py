""""""

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import (
    Column,
    Engine,
    Index,
    Insert,
    Integer,
    Select,
    String,
    Table,
    func,
    insert,
    join,
    literal,
    over,
    select,
)

from am.interfaces import JsonObj
from am.repo.base_table import Base, TableWrap

link = Table(
    "link",
    Base.metadata,
    Column("parent", String(32), primary_key=True),
    Column("child", String(32), primary_key=True),
    Column("depth", Integer),
    extend_existing=True,
)
Index("tree_idx", link.c.parent, link.c.depth, link.c.child, unique=True)
Index("tree_idx2", link.c.child, link.c.parent, link.c.depth, unique=True)


@dataclass(frozen=True, slots=True)
class LinkTable:

    tab: Table = field(default=link)

    @property
    def parent(self) -> Column[str]:
        return self.tab.c.parent

    @property
    def child(self) -> Column[str]:
        return self.tab.c.child

    @property
    def depth(self) -> Column[str]:
        return self.tab.c.depth

    async def insert_link(self, engine: Engine, parentid: str, childid: str) -> None:

        with engine.begin() as conn:

            iobj = insert(table=self.tab).values(
                {"parent": childid, "child": childid, "depth": 0}
            )

            ilinks = self._make_insert_link_stmt(parentid, childid)
            conn.execute(iobj)
            conn.execute(ilinks)

    async def select_descendants(
        self,
        engine: Engine,
        obj: TableWrap,
        id: str,
        full_hierarchy: bool,
        cols: set[Any],
    ) -> Iterable[JsonObj]:
        bquery = self._base_join(obj, cols)

        where_func = (
            self._where_all_children if full_hierarchy else self._where_direct_children
        )

        with engine.begin() as conn:

            stmt = where_func(bquery, id)
            res = conn.execute(stmt)
        return res

    def print(self, engine: Engine):

        with engine.begin() as conn:
            res = conn.execute(select(self.tab).order_by(self.depth.asc()))
            for r in res:
                print(r)

    def _base_join(self, obj: TableWrap, cols: set[Any]):

        j = join(obj.tab, self.tab, obj.id == self.child)
        return select(*cols).select_from(j)

    def _where_direct_children(self, sel: Select[Any], id: str) -> Select[Any]:

        return sel.where(self.parent == id, self.depth == 1)

    def _where_all_children(self, sel: Select[Any], id: str) -> Select[Any]:

        return sel.where(self.parent == id, self.depth > 0).order_by(self.depth.asc())

    def _make_insert_link_stmt(self, parentid: str, childid: str) -> Insert:

        sstmt = select(
            self.parent,
            literal(childid),
            over(func.row_number(), order_by=self.depth),
        ).where(self.child == parentid)

        link = self.tab.insert().from_select(
            ["parent", "child", "depth"],
            sstmt,
        )
        return link

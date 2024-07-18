""""""

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

from am.repo.base_table import Base

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

    def select_children(self, obj: Any, id: str, *fields: str) -> Select[Any]:

        cols = [getattr(obj, field) for field in fields]  # if fields else [obj]

        j = join(obj, self.tab, obj.web_id == self.child)
        return select(*cols).select_from(j).where(self.parent == id, self.depth == 1)

    def select_descendants(self, obj: Any, id: str, *fields: str) -> Select[Any]:
        j = join(obj, self.tab, obj.web_id == self.child)
        return (
            select(obj)
            .select_from(j)
            .where(self.parent == id, self.depth > 0)
            .order_by(self.depth.asc())
        )

    def _make_insert_link_stmt(
        self, parentid: str, childid: str
    ) -> tuple[Insert, Insert]:
        sstmt = select(
            self.parent,
            literal(childid),
            over(func.row_number(), order_by=self.depth),
        ).where(self.child == parentid)

        child = insert(table=self.tab).values(
            {"parent": childid, "child": childid, "depth": 0}
        )

        link = self.tab.insert().from_select(
            ["parent", "child", "depth"],
            sstmt,
        )
        return child, link

    async def insert_link(self, engine: Engine, parentid: str, childid: str) -> None:

        with engine.begin() as conn:
            iobj, ilinks = self._make_insert_link_stmt(parentid, childid)
            conn.execute(iobj)
            conn.execute(ilinks)

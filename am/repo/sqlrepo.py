from dataclasses import dataclass, field
from typing import Any, Protocol

from sqlalchemy import (Column, ForeignKey, Index, Insert, Integer, Select,
                        String, Table, create_engine, func, insert, join,
                        literal, over, select)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, aliased,
                            mapped_column)


class Base(DeclarativeBase): ...


def byte_rep(b: bytes) -> int:
    return int.from_bytes(b, byteorder="little")


class Label(Base):
    __tablename__ = "label"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str]
    type: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"base"),
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


class Node(Label):
    __tablename__ = "node"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.id"), primary_key=True
    )
    template: Mapped[str] = mapped_column(String(64), nullable=True)
    detached: Mapped[str] = mapped_column(String(8))

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"node"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.template}, {self.detached})"


class Item(Label):
    __tablename__ = "item"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.id"), primary_key=True
    )
    data_point: Mapped[str] = mapped_column(String(128), nullable=True)
    data_type: Mapped[str] = mapped_column(String(16))

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"item"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.data_point}, {self.data_type})"


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


class LinkTableInterface(Protocol):

    @property
    def tab(self) -> Table: ...

    @property
    def parent(self) -> Column[str]: ...
    @property
    def child(self) -> Column[str]: ...
    @property
    def depth(self) -> Column[str]: ...


@dataclass(frozen=True)
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

        j = join(obj, self.tab, obj.id == self.child)
        return select(*cols).select_from(j).where(self.parent == id, self.depth == 1)

    def select_descendants(self, obj: Any, id: str, *fields: str) -> Select[Any]:
        j = join(obj, self.tab, obj.id == self.child)
        return (
            select(obj)
            .select_from(j)
            .where(self.parent == id, self.depth > 0)
            .order_by(self.depth.asc())
        )


# TODO no fim de que sr chamado por func(target:str, *fields:str)
def select_children(
    obj: Any, link: LinkTableInterface, id: str, *fields: str
) -> Select[Any]:

    cols = [getattr(obj, field) for field in fields] if fields else [obj]
    j = join(obj, link.tab, obj.id == link.child)
    return select(*cols).select_from(j).where(link.parent == id, link.depth == 1)


def select_descendants(
    obj: Any, link: LinkTableInterface, id: str, *fields: str
) -> Select[Any]:

    cols = [getattr(obj, field) for field in fields] if fields else [obj]
    j = join(obj, link.tab, obj.id == link.child)
    return (
        select(*cols)
        .select_from(j)
        .where(link.parent == id, link.depth > 0)
        .order_by(link.depth.asc())
    )


def insert_link(link: LinkTableInterface, parentid: str, childid: str) -> Insert:
    sstmt = select(
        link.parent,
        literal(childid),
        over(func.row_number(), order_by=link.depth),
    ).where(link.child == parentid)
    return link.tab.insert().from_select(
        ["parent", "child", "depth"],
        sstmt,
    )


def bootstrap(url: str, echo: bool = False):
    engine = create_engine(url, echo=echo)

    Base.metadata.create_all(engine)
    return engine


###############################################################################

url = "sqlite://"
echo = False
link_table = LinkTable()

engine = bootstrap(url, echo)

with Session(engine) as session:

    n = 12

    nodes = [
        Node(id=f"{i}", name=f"name{i}", template=f"temp{i}", detached="always")
        for i in range(n)
    ]
    items = [
        Item(id=f"{i}", name=f"name{i}", data_point=f"dp{i}", data_type=f"dt{i}")
        for i in range(n, 2 * n)
    ]

    session.add_all(nodes)

    session.add_all(items)
    session.commit()


with engine.begin() as conn:

    # TODO toda vez que criar o Node, tem que inserir o depth 0
    d00 = insert(link_table.tab).values({"parent": "0", "child": "0", "depth": 0})
    d01 = insert(link_table.tab).values({"parent": "1", "child": "1", "depth": 0})
    d02 = insert(link_table.tab).values({"parent": "2", "child": "2", "depth": 0})
    d03 = insert(link_table.tab).values({"parent": "3", "child": "3", "depth": 0})
    d04 = insert(link_table.tab).values({"parent": "4", "child": "4", "depth": 0})
    d05 = insert(link_table.tab).values({"parent": "5", "child": "5", "depth": 0})
    d06 = insert(link_table.tab).values({"parent": "6", "child": "6", "depth": 0})
    d07 = insert(link_table.tab).values({"parent": "7", "child": "7", "depth": 0})
    d08 = insert(link_table.tab).values({"parent": "8", "child": "8", "depth": 0})
    d09 = insert(link_table.tab).values({"parent": "9", "child": "9", "depth": 0})
    d10 = insert(link_table.tab).values({"parent": "10", "child": "10", "depth": 0})
    d11 = insert(link_table.tab).values({"parent": "11", "child": "11", "depth": 0})

    conn.execute(d00)
    conn.execute(d01)
    conn.execute(d02)
    conn.execute(d03)
    conn.execute(d04)
    conn.execute(d05)
    conn.execute(d06)
    conn.execute(d07)
    conn.execute(d08)
    conn.execute(d09)
    conn.execute(d10)
    conn.execute(d11)

    i1 = insert_link(link_table, "0", "1")
    i2 = insert_link(link_table, "0", "2")
    i3 = insert_link(link_table, "1", "3")
    i4 = insert_link(link_table, "1", "4")
    i5 = insert_link(link_table, "2", "5")
    i6 = insert_link(link_table, "2", "6")
    i7 = insert_link(link_table, "3", "7")
    i8 = insert_link(link_table, "7", "8")
    i9 = insert_link(link_table, "5", "9")
    i10 = insert_link(link_table, "5", "10")
    i11 = insert_link(link_table, "10", "11")

    conn.execute(i1)
    conn.execute(i2)
    conn.execute(i3)
    conn.execute(i4)
    conn.execute(i5)
    conn.execute(i6)
    conn.execute(i7)
    conn.execute(i8)
    conn.execute(i9)
    conn.execute(i10)
    conn.execute(i11)

    conn.commit()

# with Session(engine) as session:
#     q = session.query(Node)
#     print(q.all())

# with Session(engine) as session:
#     q = session.query(Item)
#     print(q.all())

with engine.begin() as conn:

    stmt = select_children(Node, link_table, "2", "id", "name", "template")
    print(stmt)
    # stmt = select(link_table.tab)
    res = conn.execute(stmt)
    for r in res:
        print(r)

with engine.begin() as conn:

    stmt = select_descendants(Node, link_table, "2")
    # stmt = select(link_table.tab)
    res = conn.execute(stmt)
    for r in res:
        print(r._asdict())  # type: ignore
        
    # q = select_descendants(uuids[0])
    # res = conn.execute(q)
    # assert len(res.fetchall()) == 2 * n - 1

# class SQLRepository:

#     def create(self, parentid: IdInterface, obj: VisitableInterface) -> None: ...

#     def create_many(self, objs: tuple[IdInterface, VisitableInterface]) -> None: ...

#     def read(self, *fields: str) -> JsonObj: ...

#     def list(self, options: ReadAllOptionsInterface | None) -> Iterable[JsonObj]: ...

#     def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj: ...

#     def delete(self) -> JsonObj: ...

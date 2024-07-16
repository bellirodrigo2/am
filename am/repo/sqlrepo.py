from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Index,
    Insert,
    Integer,
    Select,
    String,
    Table,
    create_engine,
    func,
    insert,
    join,
    literal,
    over,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from am.interfaces import IdInterface, JsonObj, TreeNodeInterface


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


class TemplateNode(Label):
    __tablename__ = "tempalte_node"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.id"), primary_key=True
    )
    extensible: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"teno"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.extensible})"


class TemplateItem(Label):
    __tablename__ = "template_item"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.id"), primary_key=True
    )
    temp_item: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"teit"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.temp_item})"


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

    # TODO no fim de que sr chamado por func(target:str, *fields:str)

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

    def insert_link(self, parentid: str, childid: str) -> tuple[Insert, Insert]:
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

    i01, i1 = link_table.insert_link("0", "1")
    i02, i2 = link_table.insert_link("0", "2")
    i03, i3 = link_table.insert_link("1", "3")
    i04, i4 = link_table.insert_link("1", "4")
    i05, i5 = link_table.insert_link("2", "5")
    i06, i6 = link_table.insert_link("2", "6")
    i07, i7 = link_table.insert_link("3", "7")
    i08, i8 = link_table.insert_link("7", "8")
    i09, i9 = link_table.insert_link("5", "9")
    i010, i10 = link_table.insert_link("5", "10")
    i011, i11 = link_table.insert_link("10", "11")

    conn.execute(i01)
    conn.execute(i02)
    conn.execute(i03)
    conn.execute(i04)
    conn.execute(i05)
    conn.execute(i06)
    conn.execute(i07)
    conn.execute(i08)
    conn.execute(i09)
    conn.execute(i010)
    conn.execute(i011)

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

    stmt = link_table.select_children(Node, "2", "id", "name", "template")
    res = conn.execute(stmt)
    for r in res:
        print(r)

with engine.begin() as conn:

    stmt = link_table.select_descendants(Node, "2")
    res = conn.execute(stmt)
    for r in res:
        print(r._asdict())  # type: ignore


_T = TypeVar("_T")


class _Getter(Generic[_T]):
    def get(self, target: str) -> _T:
        return getattr(self, target)


@dataclass()
class GetTable(_Getter[Any]):
    node: Node
    item: Item


@dataclass(frozen=True, slots=True)
class SQLRepository:

    _closure: LinkTable
    _table_getter: GetTable = field(init=False)
    _obj_table: Table = field(init=False)
    _engine: Engine

    obj_type: str
    id: str

    def __post_init__(self):
        self._obj_table = self._table_getter.get(self.obj_type)

    # TODO parece padrão...pegar as tables por id.prefix.decode('utf-8')
    async def create(self, obj: TreeNodeInterface) -> None:

        # TODO special case se obj for um template

        with Session(self._engine) as session:

            db_obj = self.obj_table(obj)
            session.add(db_obj)
            session.commit()

        with self._engine.begin() as conn:
            iobj, ilinks = self._closure.insert_link(str(self.id), str(obj.web_id))
            conn.execute(iobj)
            conn.execute(ilinks)

    async def read(self, *fields: str) -> JsonObj:

        with Session(self._engine) as session:
            q = session.query(self.obj_table).where(self.obj_table.id == self.id)
            return q.one()

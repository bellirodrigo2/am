""""""

from dataclasses import dataclass
from typing import Any, Iterable, Literal

from sqlalchemy import Column, Engine, Row, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from am.interfaces import JsonObj, TreeNodeInterface


class Base(DeclarativeBase): ...


def byte_rep(b: bytes, byteorder: Literal["little", "big"] = "little") -> int:
    return int.from_bytes(b, byteorder=byteorder)


def int_rep(n: int, byteorder: Literal["little", "big"] = "little") -> bytes:
    return n.to_bytes(4, byteorder=byteorder)


class Label(Base):
    __tablename__ = "label"

    web_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str]
    client_id: Mapped[str]
    description: Mapped[str]

    type: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"base"),
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


@dataclass(frozen=True, slots=True)
class TableWrap:

    tab: Any

    @property
    def id(self) -> Column[str]:
        return self.tab.fid

    def get_cols(self, col_name: Iterable[str]) -> set[Any]:

        if not col_name:
            return set([self.tab])
        cols = set([getattr(self.tab, col) for col in col_name])
        cols.add(self.tab.web_id)
        cols.add(self.tab.type)
        return cols

    async def add_row(self, engine: Engine, obj: TreeNodeInterface) -> None:

        with Session(engine) as session:

            row = obj.model_dump()
            row["web_id"] = row["web_id"]["bid"]

            db_obj = self.tab(**row)
            session.add(db_obj)
            session.commit()

    async def read_one(self, engine: Engine, target: str, *fields: str) -> JsonObj:

        # TODO fazer as conversões de type + fid para web_id

        with Session(engine) as session:

            cols = self.get_cols(fields)

            q = session.query(*cols).where(self.id == target)
            row = q.one()
            row_dict = row._asdict() if fields else row.__dict__

            row_dict["web_id"] = (
                row_dict["type"].to_bytes(4, "little").decode("utf-8")
                + row_dict["web_id"]
            )
            # iterar sobre o dict e remover todos iniciados com _
            del row_dict["type"]

            return row_dict

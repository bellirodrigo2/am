""""""

from dataclasses import dataclass
from typing import Any, Literal

from sqlalchemy import Column, Engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase): ...


def byte_rep(b: bytes, byteorder: Literal["little", "big"] = "little") -> int:
    return int.from_bytes(b, byteorder=byteorder)


def int_rep(n: int, byteorder: Literal["little", "big"] = "little") -> bytes:
    return n.to_bytes(4, byteorder=byteorder)


class Label(Base):
    __tablename__ = "label"

    web_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str]
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

    def get_col(self, col_name: str):
        return getattr(self.tab, col_name)

    async def add_row(self, engine: Engine, **kwargs: Any) -> None:

        with Session(engine) as session:

            db_obj = self.tab(**kwargs)
            session.add(db_obj)
            session.commit()

    async def read_one(self, engine: Engine, target: str, *fields: str):

        with Session(engine) as session:
            q = session.query(self.tab).where(self.id == target)
            return q.one()

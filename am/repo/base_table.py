""""""

from dataclasses import dataclass
from typing import Any

from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


def byte_rep(b: bytes) -> int:
    return int.from_bytes(b, byteorder="little")


def int_rep(n: int) -> bytes:
    return n.to_bytes(4, "little")


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
        return self.tab.web_id

    def get_col(self, col_name: str):
        return getattr(self.tab, col_name)

    def make_row(self) -> Any: ...

""""""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from am.repo.base_table import Label, byte_rep


class Item(Label):
    __tablename__ = "item"

    fid: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.web_id"), primary_key=True
    )
    data_point: Mapped[str] = mapped_column(String(128), nullable=True)
    data_type: Mapped[str] = mapped_column(String(16))

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"item"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.data_point}, {self.data_type})"

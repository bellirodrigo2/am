""""""

from base_table import Label, byte_rep
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Node(Label):
    __tablename__ = "node"

    fid: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.web_id"), primary_key=True
    )
    template: Mapped[str] = mapped_column(String(64), nullable=True)
    detached: Mapped[str] = mapped_column(String(8))

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"node"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.template}, {self.detached})"

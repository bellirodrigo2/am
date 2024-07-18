""""""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from am.repo.base_table import Label, byte_rep


class TemplateNode(Label):
    __tablename__ = "tempalte_node"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.web_id"), primary_key=True
    )
    extensible: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"teno"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.extensible})"

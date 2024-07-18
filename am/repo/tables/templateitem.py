""""""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from am.repo.base_table import Label, byte_rep


class TemplateItem(Label):
    __tablename__ = "template_item"

    id: Mapped[str] = mapped_column(
        String(32), ForeignKey("label.web_id"), primary_key=True
    )
    temp_item: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": byte_rep(b"teit"),
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.temp_item})"

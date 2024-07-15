""" View Object """

from collections.abc import Iterable

from pydantic import Field

from am.schemas.baseclass import BaseElement


class View(BaseElement):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"view"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["basenode", "baseitem"]

    view_str: str = Field()

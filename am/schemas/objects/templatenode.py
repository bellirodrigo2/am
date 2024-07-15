""" Template Node Object """

from typing import Iterable

from pydantic import Field

from am.schemas.baseclass import BaseNode


class TemplateNode(BaseNode):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"teno"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["templatenode", "templateitem"]

    extensible: bool = Field(default=True)

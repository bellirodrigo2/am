""" Node Object """

from typing import Iterable, Literal

from pydantic import Field

from am.schemas.baseclass import BaseNode

Detached = Literal["always", "never", "ondelete"]


class Node(BaseNode):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"node"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["node", "database"]

    template: str | None = Field(default=None)
    detached: Detached = Field(default="ondelete")

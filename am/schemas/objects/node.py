""" Node Object """

from typing import Literal

from pydantic import Field

from am.schemas.baseclass import BaseNode

Detached = Literal["always", "never", "ondelete"]


class Node(BaseNode):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"node"

    template: str | None = Field(default=None)
    detached: Detached = Field(default="ondelete")

""" Node Object """

from typing import Literal

from pydantic import Field

from am.schemas.baseclass import BaseClass

Detached = Literal["always", "never", "ondelete"]


class Node(BaseClass):

    template: str | None = Field(default=None)
    detached: Detached = Field(default="ondelete")

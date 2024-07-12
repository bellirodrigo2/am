""" Node Object """

from pydantic import Field

from am.schemas.baseclass import BaseNode


class Node(BaseNode):

    # @classmethod
    # def byte_rep(cls) -> bytes:
    #     return b"node"

    template: str = Field()

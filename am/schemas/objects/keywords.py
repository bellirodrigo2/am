""" Asset Keywords Object """

from pydantic import Field

from am.schemas.basenode import BaseElement

###############################################################################


class Keywords(BaseElement):
    # @classmethod
    # def byte_rep(cls) -> bytes:
    # return b"kewo"

    keywords: list[str] = Field()

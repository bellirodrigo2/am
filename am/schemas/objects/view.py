""" View Object """

from pydantic import Field

from am.schemas.baseobjs import BaseElement

###############################################################################


class View(BaseElement):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"view"

    view_str: str = Field()

""" View Object """

from pydantic import Field

from am.schemas.baseclass import TreeElement

###############################################################################


class View(TreeElement):

    # @classmethod
    # def byte_rep(cls) -> bytes:
    # return b"view"

    view_str: str = Field()

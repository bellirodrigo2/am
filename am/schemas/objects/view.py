""" View Object """

from pydantic import Field

from am.schemas.schemas import BaseElement

###############################################################################


class View(BaseElement):

    view_str: str = Field()

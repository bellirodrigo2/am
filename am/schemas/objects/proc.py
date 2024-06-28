""" Proc Object """

from pydantic import Field

from am.schemas.schemas import BaseElement

###############################################################################


class Proc(BaseElement):

    proc_str: str = Field()

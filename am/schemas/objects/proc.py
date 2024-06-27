""" Proc Object """

from typing import Annotated

from cahier.schemas.schemas import BaseElement
from pydantic import Field

###############################################################################


class Proc(BaseElement):

    proc_str: str = (Field(),)

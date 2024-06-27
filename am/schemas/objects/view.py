""" View Object """

from typing import Annotated

from cahier.schemas.schemas import BaseElement
from pydantic import Field

###############################################################################


class View(BaseElement):

    view_str: str = (Field(),)

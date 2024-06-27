""" Node Object """

from typing import Annotated

from cahier.schemas.schemas import BaseNode
from pydantic import Field

###############################################################################


class Node(BaseNode):

    template: str = (Field(),)

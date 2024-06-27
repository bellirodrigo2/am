""" Node Object """

from pydantic import Field

from am.schemas.schemas import BaseNode

###############################################################################


class Node(BaseNode):

    template: str = (Field(),)

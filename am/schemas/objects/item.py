""" Item Object """

from enum import Enum

from pydantic import Field

from am.schemas.schemas import BaseItem

# from am.schemas.timestamp import Timestamp

###############################################################################


class ItemType(Enum):
    string = "str"
    float = "float"
    int = "int"
    boolean = "bool"
    byte = "bytes"
    timestamp = "timestamp"


class Item(BaseItem):

    type: ItemType = Field()

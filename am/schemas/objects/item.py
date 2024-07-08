""" Item Object """

from enum import Enum

from pydantic import Field

from am.schemas.basenode import BaseItem

###############################################################################


class ItemType(Enum):
    string = "str"
    float = "float"
    int = "int"
    boolean = "bool"
    byte = "bytes"
    timestamp = "timestamp"


class Item(BaseItem):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"item"

    data_type: ItemType = Field()

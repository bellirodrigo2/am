""" Item Object """

from enum import Enum

from cahier.schemas.schemas import BaseItem
from cahier.schemas.timestamp import Timestamp
from pydantic import Field

###############################################################################


class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp


class Item(BaseItem):

    type: DataTypeEnum = (Field(),)

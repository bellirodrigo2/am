""" Item Object """

from pydantic import Field

from am.schemas.baseclass import BaseItem
from am.schemas.datatype import DataType


class Item(BaseItem):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"item"

    data_point: str  # webid do point
    data_type: DataType = Field()

""" Item Object """

from pydantic import Field

from am.schemas.baseclass import BaseClass
from am.schemas.datatype import DataType


class Item(BaseClass):

    data_point: str  # webid do point
    data_type: DataType = Field()

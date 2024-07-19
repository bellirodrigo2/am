""" Item Object """

from pydantic import Field

from am.schemas.baseclass import BaseClass
from am.schemas.models.datatype import DataType


class Item(BaseClass):

    data_point: str = Field(max_length=128)
    data_type: DataType

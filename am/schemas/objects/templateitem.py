""" Item Object """

from pydantic import Field

from am.schemas.baseclass import BaseClass
from am.schemas.datatype import DataType


class TemplateItem(BaseClass):

    data_point: str  # webid do point
    data_type: DataType = Field()

""" Item Object """

from pydantic import Field

from am.schemas.baseclass import BaseItem
from am.schemas.datatype import DataType


class TemplateItem(BaseItem):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"teit"

    data_point: str  # webid do point
    data_type: DataType = Field()

from pydantic import Field

from am.schemas.baseclass import BaseRoot
from am.schemas.datatype import DataType


class Point(BaseRoot):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"seel"

    server_host: str = Field()
    db_name: str
    db_table: str
    db_column: str
    point_type: DataType
    zero: float
    span: float

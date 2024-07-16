from am.schemas.baseclass import BaseClass
from am.schemas.objects.datatype import DataType


class Point(BaseClass):

    server_host: str
    db_name: str
    db_table: str
    db_column: str
    point_type: DataType
    zero: float
    span: float

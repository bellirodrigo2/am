from typing import Callable, get_args

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    MetaData,
    String,
    Table,
    Time,
)
from sqlalchemy.sql.sqltypes import TypeEngine

sqlalc_types = [
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Interval,
    String,
    Time,
]

types_map = {t().python_type: t for t in sqlalc_types}

# def make_col(field_name: str, field_info: FieldInfo):
#     title = to_snake(field_name)
#     args = get_args(field_info.annotation)
#     if len(args) == 0:
#         return Column(title, types_map[field_info.annotation])
#     elif len(args) == 2:
#         t1, t2 = args
#         field_type = t2 if (t1 is type(None)) else t1 if (t2 is type(None)) else None
#         return Column(title, types_map[field_type], nullable=True)
#     raise Exception()


def make_primary(name: str, coltype: TypeEngine):
    return Column(name, coltype, primary_key=True)


def make_foreign(
    pid_table: str,
    pid_col: str,
    name: str,
    coltype: TypeEngine,
    is_pk: bool,
):
    return Column(
        name, coltype, ForeignKey(f"{pid_table}.{pid_col}"), primary_key=is_pk
    )


str_conv = Callable[[str], str]


def make_table(
    table_name: str,
    meta: MetaData,
    name_transf: str_conv | None,
    *adds: Column,  # for primary and foreign columns
    **fields: type | None,  # for all other columns
) -> Table:

    def make_col(field_name: str, field_info: type | None) -> Column:

        if field_info is None:
            raise Exception(f'field_info is "None" for {field_name}')

        title = name_transf(field_name) if name_transf else field_name

        args = get_args(field_info)
        lenargs = len(args)
        if lenargs == 0:
            return Column(title, types_map[field_info])
        elif lenargs == 2:
            t1, t2 = args
            field_type = (
                t2 if (t1 is type(None)) else t1 if (t2 is type(None)) else None
            )
            return Column(title, types_map[field_type], nullable=True)
        raise Exception(
            f"field_info len() is {lenargs}. Should be zero or 2 to figure out Column Type"
        )

    cols = [make_col(key, value) for key, value in fields.items()]
    table_title = name_transf(table_name) if name_transf else table_name

    return Table(table_title, meta, *cols, *adds)


if __name__ == "__main__":

    print("OK")

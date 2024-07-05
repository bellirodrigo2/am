""""""

from sqlalchemy import Column, Connection, Table, insert, join, select

from am.exceptions import IdNotFound
from am.interfaces import IdInterface, JsonObj, ReadAllOptions


class SQLRepo:

    def __init__(
        self, conn: Connection, id: IdInterface, labeltab: Table, treetab: Table
    ) -> None:
        self._conn = conn
        self._id = id
        self._labeltab = labeltab
        self._treetab = treetab
        self._join = join(
            self._labeltab,
            self._treetab,
            self._labeltab.c["webid"] == self._treetab.c["child"],
        )

    def _get_columns(self, selected_fields: tuple[str, ...] | None) -> list[Column]:
        return []


class CreateRepository(SQLRepo):
    def __call__(self, base: JsonObj, obj_spec: JsonObj) -> IdInterface: ...


class ReadRepository(SQLRepo):

    def __call__(self, selected_fields: tuple[str, ...] | None) -> JsonObj:
        """"""

        label = self._labeltab
        j = self._join
        id = self._id
        cols: list[Column] = self._get_columns(selected_fields)

        stmt = select(*cols).select_from(j).where(label.c["webid"] == id)
        res = self._conn.execute(stmt).fetchone()

        if res:
            return res._asdict()
        raise IdNotFound()


class ListRepository(SQLRepo):

    def _select_children(self, *fields: str):

        tree = self._treetab
        j = self._join
        id = self._id
        cols: list[Column] = self._get_columns(fields)

        return (
            select(*cols)
            .select_from(j)
            .where(tree.c["parent"] == id, tree.c["depth"] == 1)
        )

    def _select_descendants(self, *fields: str):
        tree = self._treetab
        j = self._join
        id = self._id
        cols: list[Column] = self._get_columns(fields)

        return (
            select(*cols)
            .select_from(j)
            .where(tree.c["parent"] == id, tree.c["depth"] > 0)
            .order_by(tree.c["depth"].asc())
        )

    def __call__(self, options: ReadAllOptions | None) -> tuple[JsonObj, ...]: ...

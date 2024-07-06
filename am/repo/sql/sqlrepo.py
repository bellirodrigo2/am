""""""

from sqlalchemy import Column, Connection, Table, func, insert, join, over, select

from am.exceptions import IdNotFound
from am.interfaces import IdInterface, JsonObj, ReadAllOptions
from am.repo.sql.interfaces import ClosureTable, LabelTable


class SQLRepo:

    def __init__(
        self,
        conn: Connection,
        id: IdInterface,
        labeltab: LabelTable,
        treetab: ClosureTable,
    ) -> None:
        self._conn = conn
        self._id = id
        self._labeltab = labeltab
        self._treetab = treetab
        self._join = join(
            self._labeltab.table,
            self._treetab.table,
            self._labeltab.webid == self._treetab.child,
        )

    def _get_columns(self, selected_fields: tuple[str, ...] | None) -> list[Column]:
        return []


class CreateRepository(SQLRepo):

    def __init__(
        self,
        conn: Connection,
        id: IdInterface,
        labeltab: LabelTable,
        treetab: ClosureTable,
        objtab: Table,  # TODO must be the right table here... should match obj
    ) -> None:
        super().__init__(conn, id, labeltab, treetab)
        self._objtab = objtab

    def _link_tree(self):

        label = self._labeltab
        treetab = self._treetab
        id = self._id
        conn = self._conn
        stmt = select(
            self._treetab.parent,
            label.webid,
            over(func.row_number(), order_by=self._treetab.depth),
        ).where(self._treetab.child == id)

        ins = treetab.insert().from_select(
            # treetab.__annotations__ menos table
            ["parent", "child", "depth"],
            stmt,
        )
        conn.execute(ins)

    def __call__(self, base: JsonObj, obj: JsonObj, istree: bool) -> None:

        label = self._labeltab
        objtab = self._objtab
        conn = self._conn

        stmtlabel = insert(label.table).values(base)
        conn.execute(stmtlabel)

        if istree:
            try:
                self._link_tree()

            except Exception as e:
                # rollback stmtlabel
                raise
        try:
            stmtobj = insert(objtab).values(obj)
            conn.execute(stmtobj)
        except Exception as e:
            # rollback stmtlabel e tree
            raise


class ReadRepository(SQLRepo):

    def __call__(self, selected_fields: tuple[str, ...] | None) -> JsonObj:
        """"""

        label = self._labeltab
        j = self._join
        id = self._id
        cols: list[Column] = self._get_columns(selected_fields)

        stmt = select(*cols).select_from(j).where(label.webid == id)
        res = self._conn.execute(stmt).fetchone()

        if res:
            return res._asdict()
        raise IdNotFound()


class ListRepository(SQLRepo):

    def _select_children(self, *cols: Column):

        tree = self._treetab
        j = self._join
        id = self._id

        return select(*cols).select_from(j).where(tree.parent == id, tree.depth == 1)

    def _select_descendants(self, *cols: Column):
        tree = self._treetab
        j = self._join
        id = self._id

        return (
            select(*cols)
            .select_from(j)
            .where(tree.parent == id, tree.depth > 0)
            .order_by(tree.depth.asc())
        )

    def __call__(self, options: ReadAllOptions | None) -> tuple[JsonObj, ...]:

        if options:
            searchfull = options.search_full_hierarchy or False
            fields = options.selected_fields or None

        # TODO AQUI NAO ESTA CORRETO
        cols: list[Column] = self._get_columns(fields)

        stmt = (
            self._select_descendants(*cols)
            if searchfull
            else self._select_children(*cols)
        )
        res = self._conn.execute(stmt).fetchall()

        if res:
            return tuple([r._asdict() for r in res])
        raise IdNotFound()

""""""

from collections.abc import Iterable

from sqlalchemy import Column, Connection, Select, func, insert, join, over, select

from am.interfaces import IdInterface, JsonObj, ReadAllOptions
from am.repo.sql.interfaces import LinksInterface, TableInterface


class SQLRepo:

    def __init__(
        self,
        conn: Connection,
        id: IdInterface,
        linktab: LinksInterface,
        labeltab: TableInterface,
        objtab: TableInterface,
    ) -> None:
        self._conn = conn
        self._id = id
        self._labeltab = labeltab
        self._linktab = linktab
        self._objtab = objtab
        self._linkjoin = join(
            self._labeltab.table,
            self._linktab.table,
            self._labeltab.id == self._linktab.child,
        )
        self._objjoin = join(
            self._labeltab.table,
            self._objtab.table,
            self._labeltab.id == self._objtab.id,
        )

    def get_columns(self, *fields: str) -> Iterable[Column]:

        colslabel = self._labeltab.get_columns(*fields)
        colsobj = self._objtab.get_columns(*fields)

        return list(colslabel) + list(colsobj)

    def create(
        self, base: JsonObj, obj: JsonObj, id: IdInterface, istree: bool
    ) -> None:

        # ESSE ID VEM DE ONDE ??? PRECISA ADICIONAR AO OBJ ????
        insertlabel = insert(self._labeltab.table).values(base)
        if istree:
            insertlink = self._linktab.insert(id)
        insertobj = insert(self._objtab.table).values(obj)
        # EXECUTE AND COMMIT

    def read(self, *fields: str) -> JsonObj:

        cols = self.get_columns(*fields)
        sstmt = select(*cols).select_from(self._objjoin)
        # EXECUTE AND COMMIT
        return {}

    def list(self, options: ReadAllOptions) -> Iterable[JsonObj]:

        if options.selected_fields:
            cols = self.get_columns(*options.selected_fields)
        sstmt = select(*cols)
        if options.search_full_hierarchy:
            sstmt = self._linktab.select_descendants(id, sstmt)
        else:
            sstmt = self._linktab.select_children(id, sstmt)
        sstmt.select_from(self._objjoin)
        # add filter here com where
        return []

    def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj:
        return {}

    def delete(self) -> JsonObj:
        return {}

""""""

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import (
    Column,
    Connection,
    Join,
    Select,
    func,
    insert,
    join,
    over,
    select,
)

from am.interfaces import IdInterface, JsonObj, ReadAllOptions
from am.repo.sql.interfaces import LinksInterface, TableInterface


@dataclass(frozen=True, slots=True)
class SQLRepo:
    _conn: Connection
    _id: IdInterface
    _linktab: LinksInterface
    _labeltab: TableInterface
    _objtab: TableInterface

    @property
    def linkjoin(self) -> Join:
        return join(
            self._labeltab.table,
            self._linktab.table,
            self._labeltab.id == self._linktab.child,
        )

    @property
    def objtab(self) -> Join:
        return join(
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
        sstmt = select(*cols).select_from(self.objjoin)
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
        sstmt.select_from(self.objjoin)
        # add filter here com where
        return []

    def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj:
        return {}

    def delete(self) -> JsonObj:
        return {}

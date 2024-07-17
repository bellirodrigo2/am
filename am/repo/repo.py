from dataclasses import dataclass, field

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from am.interfaces import JsonObj, TreeNodeInterface
from am.repo.base_table import TableWrap
from am.repo.closure import LinkTable
from am.repo.tables.item import Item
from am.repo.tables.node import Node


@dataclass(frozen=True, slots=True)
class _GetTable:
    node: type = field(default=Node)
    item: type = field(default=Item)

    def get(self, target: str) -> type:
        return getattr(self, target)


table_getter = _GetTable()


@dataclass(frozen=True, slots=True)
class SQLRepository:

    _closure: LinkTable
    _engine: Engine

    obj_type: str
    id: str

    _obj_table: TableWrap

    async def create(self, obj: TreeNodeInterface) -> None:

        # TODO special case se obj for um template

        with Session(self._engine) as session:

            db_obj = self._obj_table.make_row(**obj.dump())
            session.add(db_obj)
            session.commit()

        with self._engine.begin() as conn:
            iobj, ilinks = self._closure.insert_link(self.id, str(obj.web_id))
            conn.execute(iobj)
            conn.execute(ilinks)

    async def read(self, *fields: str) -> JsonObj:

        with Session(self._engine) as session:
            q = session.query(self._obj_table.tab).where(self._obj_table.id == self.id)
            return q.one()

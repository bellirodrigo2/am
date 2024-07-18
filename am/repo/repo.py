from dataclasses import dataclass, field
from functools import partial

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from am.interfaces import IdInterface, JsonObj, TreeNodeInterface
from am.repo.base_table import TableWrap
from am.repo.closure import LinkTable
from am.repo.tables.item import Item
from am.repo.tables.node import Node

NodeTable = partial(TableWrap, tab=Node)
ItemTable = partial(TableWrap, tab=Item)


@dataclass(frozen=True, slots=True)
class _GetTable:

    node: TableWrap = field(default_factory=NodeTable)
    item: TableWrap = field(default_factory=ItemTable)

    def get(self, id: IdInterface) -> TableWrap:

        target = str(id.pref)
        return getattr(self, target)


table_getter = _GetTable()


@dataclass(frozen=True, slots=True)
class SQLRepository:

    _closure: LinkTable
    _engine: Engine

    async def create(self, obj: TreeNodeInterface, parent: IdInterface) -> None:

        # TODO special case se obj for um template
        obj_table: TableWrap = table_getter.get(obj.web_id)

        await obj_table.add_row(engine=self._engine, **obj.model_dump())
        await self._closure.insert_link(
            engine=self._engine, parentid=str(parent), childid=obj.web_id
        )

    async def read(self, target: IdInterface, *fields: str) -> JsonObj:

        obj_table: TableWrap = table_getter.get(target)

        return await obj_table.read_one(self._engine, target.bid, *fields)

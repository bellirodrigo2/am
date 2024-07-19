from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import partial

from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound

from am.exceptions import IdNotFoundError
from am.interfaces import JsonObj, ReadAllOptionsInterface, TreeNodeInterface
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

    def get_table(self, target: str) -> TableWrap:
        return getattr(self, target)


table_getter = _GetTable()


@dataclass(frozen=True, slots=True)
class SQLRepository:

    _closure: LinkTable
    _engine: Engine

    def _get_table(self, target: str) -> TableWrap:
        return table_getter.get_table(target)

    async def create(self, obj: TreeNodeInterface, parent_id: str) -> None:

        # TODO special case se obj for um template
        obj_table: TableWrap = self._get_table(target=obj.__class__.__name__.lower())

        await obj_table.add_row(engine=self._engine, obj=obj)
        await self._closure.insert_link(
            engine=self._engine, parentid=parent_id, childid=obj.web_id
        )

    async def read(self, target: str, id: str, *fields: str) -> JsonObj:

        obj_table: TableWrap = self._get_table(target)

        try:
            return await obj_table.read_one(self._engine, id, *fields)
        except NoResultFound:
            raise IdNotFoundError(id)

    async def list(
        self, target: str, id: str, options: ReadAllOptionsInterface
    ) -> Iterable[JsonObj]:

        obj_table: TableWrap = self._get_table(target)
        cols = obj_table.get_cols(options.selected_fields)

        return await self._closure.select_descendants(
            self._engine, obj_table, id, options.search_full_hierarchy, cols
        )

    def print(self):
        self._closure.print(self._engine)

    # field_filter: Mapping[field, str] | None
    # field_filter_like: Mapping[field, str] | None
    # sort_options: tuple[tuple[field, SortOrder], ...] | None
    # pag_options: tuple[start, max] | None

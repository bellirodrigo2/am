""""""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from am.interfaces import (
    JsonObj,
    ReadAllOptionsInterface,
    Repository,
    SortOrder,
    TreeNodeInterface,
)
from am.schemas.entry import Entry


@dataclass(frozen=True, slots=True)
class _TargetAsset:

    _repo: Repository
    _validator: type[Entry]

    target: str
    webid: str

    def __post_init__(self) -> None:
        self._validator(target=self.target, webid=self.webid)


@dataclass(frozen=True, slots=True)
class _TargetChildAsset:

    _repo: Repository
    _validator: type[Entry]

    target: str
    webid: str
    child: str

    def __post_init__(self) -> None:

        self._validator(target=self.target, webid=self.webid, child=self.child)


@dataclass(frozen=True, slots=True)
class CreateAsset(_TargetChildAsset):

    _cast: Callable[..., TreeNodeInterface]

    async def __call__(self, inpobj: JsonObj) -> JsonObj:

        obj: TreeNodeInterface = self._cast(target=self.child, **inpobj)

        # TODO USE VISITOR
        await self._repo.create(obj=obj, parent_id=self.webid)

        return {f"{self.child}": obj}


@dataclass(frozen=True, slots=True)
class ReadOneAsset(_TargetAsset):

    _split_fields: Callable[..., tuple[set[str], set[str]]]

    async def __call__(self, *fields: str) -> JsonObj:

        inters, out = self._split_fields(self.target, *fields)

        obj = await self._repo.read(self.target, self.webid, *inters)

        return {f"{self.target}": obj, "Errors": {"Unknown Fields": out}}


@dataclass(frozen=True, slots=True)
class ReadManyAsset(_TargetChildAsset):

    _split_fields: Callable[..., tuple[set[str], set[str]]]

    class ReadAllOptions:

        field_filter: Mapping[str, str] | None = None
        field_filter_like: Mapping[str, str] | None = None
        search_full_hierarchy: bool = False
        sort_options: tuple[tuple[str, SortOrder], ...] | None = None
        pag_options: tuple[int, int] | None = None
        selected_fields: tuple[str, ...] = ()

    async def __call__(self, options: ReadAllOptionsInterface | None = None) -> JsonObj:

        _options: ReadAllOptionsInterface = options or ReadManyAsset.ReadAllOptions()

        inters, out = self._split_fields(self.target, *_options.selected_fields)

        _options.selected_fields = tuple(inters)
        objs = await self._repo.list(options=options)

        return {f"{self.child}s": objs, "Errors": {"Unknown Fields": out}}


class UpdateAsset(_TargetChildAsset):

    _check_fields: Callable[[str, JsonObj], tuple[Mapping[str, Any], set[str]]]

    async def __call__(self, updobj: JsonObj) -> JsonObj:

        inters, out = self._check_fields(self.target, updobj)

        await self._repo.update(**inters)

        return {f"{self.child}": inters, "Errors": {"Unknown Fields": out}}


class DeleteAsset(_TargetAsset):

    async def __call__(self) -> None:

        await self._repo.delete()

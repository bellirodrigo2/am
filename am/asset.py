""""""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from am.interfaces import (
    IdInterface,
    JsonObj,
    NodeInterface,
    ObjectsRules,
    ReadAllOptionsInterface,
    Repository,
    SortOrder,
)


@dataclass(frozen=True, slots=True)
class TargetAsset:

    _repo: Repository
    _rules: ObjectsRules

    target: str
    webid: IdInterface

    def __post_init__(self) -> None:
        self._rules.check_id(self.target, self.webid)


@dataclass(frozen=True, slots=True)
class TargetChildAsset(TargetAsset):

    child: str

    def __post_init__(self) -> None:

        TargetAsset.__post_init__(self)
        self._rules.check_hierarchy(self.target, self.child)


@dataclass(frozen=True, slots=True)
class CreateAsset(TargetChildAsset):

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        obj: NodeInterface = self._rules.make_node(target=self.child, **inpobj)

        new_webid: IdInterface = self._rules.make_id(target=self.child)

        self._repo.create(obj=obj, id=new_webid)

        return {"webid": new_webid}


class ReadOneAsset(TargetAsset):

    def __call__(self, *fields: str) -> JsonObj:

        sel_fields = fields if fields else self._rules.get_fields(self.target)

        return self._repo.read(*sel_fields)


class ReadAllOptions:

    field_filter: Mapping[str, str] | None = None
    field_filter_like: Mapping[str, str] | None = None
    search_full_hierarchy: bool = False
    sort_options: tuple[tuple[str, SortOrder], ...] | None = None
    pag_options: tuple[int, int] | None = None
    selected_fields: Iterable[str] | None = None


class ReadManyAsset(TargetChildAsset):

    def __call__(
        self, options: ReadAllOptionsInterface | None = None
    ) -> Iterable[JsonObj]:

        _options: ReadAllOptionsInterface = options or ReadAllOptions()
        sel_fields: Iterable[str] = _options.selected_fields or self._rules.get_fields(
            target=self.target
        )
        _options.selected_fields = sel_fields
        return self._repo.list(options=options)


class UpdateAsset(TargetChildAsset):
    def __call__(self, updobj: JsonObj) -> JsonObj:
        return {}


class DeleteAsset(TargetAsset):

    def __call__(self) -> None:

        self._repo.delete()

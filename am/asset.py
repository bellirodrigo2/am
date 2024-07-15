""""""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass

from am.interfaces import (
    IdInterface,
    JsonObj,
    ReadAllOptionsInterface,
    Repository,
    SortOrder,
    VisitableInterface,
)


@dataclass(frozen=True, slots=True)
class TargetAsset:

    _repo: Repository
    # _rules: ObjectsRules
    _check_id: Callable[[str, IdInterface], None]

    target: str
    webid: IdInterface

    def __post_init__(self) -> None:
        self._check_id(self.target, self.webid)


@dataclass(frozen=True, slots=True)
class TargetChildAsset(TargetAsset):

    child: str
    _check_hierarchy: Callable[[str, str], None]

    def __post_init__(self) -> None:

        TargetAsset.__post_init__(self)
        self._check_hierarchy(self.target, self.child)


# @dataclass(frozen=True, slots=True)
# class _Asset(TargetChildAsset):

# _obj_class_handler: ObjectHandler


@dataclass(frozen=True, slots=True)
class CreateAsset(TargetChildAsset):

    _cast: Callable[..., VisitableInterface]
    _make_id: Callable[[str], IdInterface]

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        obj: VisitableInterface = self._cast(target=self.child, **inpobj)

        new_webid: IdInterface = self._make_id(self.child)

        self._repo.create(obj=obj, id=new_webid)

        return {"webid": new_webid}


@dataclass(frozen=True, slots=True)
class ReadOneAsset(TargetAsset):

    _split_fields: Callable[..., tuple[set[str], set[str]]]

    def __call__(self, *fields: str) -> JsonObj:

        inters, out = self._split_fields(self.target, *fields)

        obj = self._repo.read(*inters)

        return {f"{self.target}": obj, "Errors": {"Unknown Fields": out}}


@dataclass(frozen=True, slots=True)
class ReadManyAsset(TargetChildAsset):

    _split_fields: Callable[..., tuple[set[str], set[str]]]

    class ReadAllOptions:

        field_filter: Mapping[str, str] | None = None
        field_filter_like: Mapping[str, str] | None = None
        search_full_hierarchy: bool = False
        sort_options: tuple[tuple[str, SortOrder], ...] | None = None
        pag_options: tuple[int, int] | None = None
        selected_fields: tuple[str, ...] = ()

    def __call__(self, options: ReadAllOptionsInterface | None = None) -> JsonObj:

        _options: ReadAllOptionsInterface = options or ReadManyAsset.ReadAllOptions()

        inters, out = self._split_fields(self.target, *_options.selected_fields)

        _options.selected_fields = tuple(inters)
        objs = (self._repo.list(options=options),)

        return {f"{self.child}s": objs, "Errors": {"Unknown Fields": out}}


class UpdateAsset(TargetChildAsset):
    def __call__(self, updobj: JsonObj) -> JsonObj:
        return {}


class DeleteAsset(TargetAsset):

    def __call__(self) -> None:

        self._repo.delete()

""""""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from am.interfaces import (
    IdInterface,
    JsonObj,
    NodeInterface,
    ReadAllOptions,
    Repository,
)
from am.schemas.nodefuncs import make_id


@dataclass(frozen=True, slots=True)
class TargetAsset:

    _repo: Repository
    _check_webid: Callable[[str, IdInterface], None]
    _fields: Callable[[str], Iterable[str]]

    target: str
    webid: IdInterface

    def __post_init__(self) -> None:
        self._check_webid(self.target, self.webid)


@dataclass(frozen=True, slots=True)
class ParentChildAsset(TargetAsset):

    _check_hierarchy: Callable[[str, str], None]
    child: str

    def __post_init__(self) -> None:

        TargetAsset.__post_init__(self)
        self._check_hierarchy(self.target, self.child)


@dataclass(frozen=True, slots=True)
class CreateAsset(ParentChildAsset):

    _make: Callable[..., NodeInterface]

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        obj: NodeInterface = self._make(target=self.child, **inpobj)
        new_webid: IdInterface = make_id(target=self.child)

        self._repo.create(obj=obj, id=new_webid)

        return {"webid": new_webid}


class ReadOneAsset(TargetAsset):

    def __call__(self, *fields: str) -> JsonObj:

        sel_fields = fields if fields else self._fields(self.target)

        return self._repo.read(*sel_fields)


class ReadManyAsset(ParentChildAsset):

    def __call__(self, options: ReadAllOptions | None = None) -> Iterable[JsonObj]:

        # TODO VER AQUI OQUE FAZER SE VIER NONE

        return self._repo.list(options=options)


class UpdateAsset(ParentChildAsset):
    def __call__(self, updobj: JsonObj) -> JsonObj:
        return {}


class DeleteAsset(TargetAsset):

    def __call__(self) -> None:

        self._repo.delete()

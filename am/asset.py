""""""

from collections.abc import Iterable
from dataclasses import dataclass

from am.interfaces import (
    IdInterface,
    JsonObj,
    NodeInterface,
    ObjectsRules,
    ReadAllOptions,
    Repository,
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


class ReadManyAsset(TargetChildAsset):

    def __call__(self, options: ReadAllOptions | None = None) -> Iterable[JsonObj]:

        # TODO VER AQUI OQUE FAZER SE VIER NONE

        return self._repo.list(options=options)


class UpdateAsset(TargetChildAsset):
    def __call__(self, updobj: JsonObj) -> JsonObj:
        return {}


class DeleteAsset(TargetAsset):

    def __call__(self) -> None:

        self._repo.delete()

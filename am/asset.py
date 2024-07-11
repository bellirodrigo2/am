""""""

from collections.abc import Iterable
from dataclasses import dataclass, field

from am.container import Factory
from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import (
    IdInterface,
    JsonObj,
    NodeClassInterface,
    NodeInterface,
    ReadAllOptions,
    Repository,
    VisitorInterface,
)


@dataclass(frozen=True, slots=True)
class TargetAsset:

    _repo: Repository
    _factory: Factory
    _byterep: VisitorInterface
    _target: str
    _target_cls: NodeClassInterface = field(init=False)
    _webid: IdInterface

    def __post_init__(self) -> None:

        object.__setattr__(self, "_target_cls", self._factory.get(self._target))

        def check_webid(target: NodeClassInterface, webid: IdInterface) -> None:
            if self._byterep.visit(target) == webid.prefix:
                return
            raise InconsistentIdTypeError(target=target.__name__, webid=str(webid))

        check_webid(target=self._target_cls, webid=self._webid)


@dataclass(frozen=True, slots=True)
class ParentChildAsset(TargetAsset):

    _child: str
    _child_cls: NodeClassInterface = field(init=False)

    def __post_init__(self) -> None:

        TargetAsset.__post_init__(self)

        object.__setattr__(self, "_child_cls", self._factory.get(self._child))

        def check_hierarchy(
            target: NodeClassInterface, child: NodeClassInterface
        ) -> None:
            if child.base_type() in target.children():
                return
            raise ObjHierarchyError(parent=target.__name__, child=child.__name__)

        check_hierarchy(target=self._target_cls, child=self._child_cls)


@dataclass(frozen=True, slots=True)
class CreateAsset(ParentChildAsset):

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        obj: NodeInterface = self._child_cls(**inpobj)

        webid: IdInterface = self._webid.make(
            input=self._byterep.visit(self._child_cls)
        )
        self._repo.create(obj=obj, id=webid)

        return {"webid": webid}


class ReadOneAsset(TargetAsset):

    def __call__(self, *fields: str) -> JsonObj:

        # TODO SE NAO VIER NADA, LISTA OS FIELDS ?????
        return self._repo.read(*fields)


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

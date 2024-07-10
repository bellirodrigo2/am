""""""

from collections.abc import Iterable
from dataclasses import dataclass, field

from am.container import Factory
from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import (
    DataNodeInterface,
    IdInterface,
    JsonObj,
    NodeClassInterface,
    ReadAllOptions,
    Repository,
)


@dataclass(frozen=True, slots=True)
class TargetAsset:

    _repo: Repository
    _factory: Factory
    _target: str
    _target_cls: NodeClassInterface = field(init=False)
    _webid: IdInterface

    def __post_init__(self) -> None:

        object.__setattr__(self, "_target_cls", self._factory.get(self._target))

        def check_webid(target: NodeClassInterface, webid: IdInterface) -> None:
            if target.byte_rep() == webid.prefix:
                return
            raise InconsistentIdTypeError(target=target.__name__, webid=str(webid))

        check_webid(target=self._target_cls, webid=self._webid)


@dataclass(frozen=True, slots=True)
class ParentChildAsset(TargetAsset):

    _child_cls: NodeClassInterface = field(init=False)
    _child: str

    def __post_init__(self) -> None:

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

        obj: DataNodeInterface = self._child_cls(**inpobj)

        webid: IdInterface = self._webid.make(pref=self._child_cls.byte_rep())

        self._repo.create(obj=obj, id=webid)

        return {"webid": webid}


class ReadOneAsset(TargetAsset):

    def __call__(self, *fields: str) -> JsonObj:

        # sel_fields: Iterable[str] = self._get_valid_fields(*fields)
        return self._repo.read(*fields)


class ReadmanyAsset(ParentChildAsset):

    def __call__(self, options: ReadAllOptions | None) -> Iterable[JsonObj]:

        # TODO VER AQUI OQUE FAZER SE VIER NONE

        return self._repo.list(options=options)


class UpdateAsset(ParentChildAsset):
    def __call__(self, updobj: JsonObj) -> JsonObj:
        return {}


class DeleteAsset(TargetAsset):

    def __call__(self) -> None:

        self._repo.delete()

    # def _fields_list(self) -> Iterable[str]:

    #     # label_fields = list(self._label.get_fields().keys())
    #     return list(self._target_cls.get_fields().keys())

    #     # return set(target_fields + label_fields)

    # def _get_valid_fields(self, *fields: str) -> Iterable[str]:

    #     obj_fields: Iterable[str] = self._fields_list()
    #     if fields:
    #         return set(set(obj_fields) & set(fields))
    #     return obj_fields

    # def _get_valid_field_filters(self, **filters: str) -> Mapping[str, str]:

    #     obj_fields = self._fields_list()
    #     return {k: v for k, v in filters.items() if k in obj_fields}

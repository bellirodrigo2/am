""""""

from collections.abc import Callable, Iterable, Mapping, MutableMapping

from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import (
    IdInterface,
    JsonObj,
    LabelInterface,
    ObjClassInterface,
    ReadAllOptions,
    Repository,
)


class TargetAsset:

    def __init__(
        self,
        repo: Repository,
        target: ObjClassInterface,
        webid: IdInterface,
        # label: type[LabelInterface],
    ) -> None:

        def check_webid(target: ObjClassInterface, webid: IdInterface) -> None:
            if target.byte_rep() == webid.prefix:
                return
            raise InconsistentIdTypeError(target.__name__, str(webid))

        check_webid(target, webid)
        self._repo = repo
        self._target = target
        self._webid = webid
        # self._label = label

    def _fields_list(self) -> set[str]:

        label_fields = list(LabelInterface.__annotations__.keys())
        target_fields = list(self._target.get_fields().keys())

        return set(target_fields + label_fields)

    def _get_valid_fields(self, *fields: str) -> Iterable[str]:

        obj_fields = self._fields_list()
        if fields:
            return set(obj_fields & set(fields))
        return obj_fields

    def _get_valid_field_filters(self, **filters: str) -> Mapping[str, str]:

        obj_fields = self._fields_list()
        return {k: v for k, v in filters.items() if k in obj_fields}


class ParentChildAsset(TargetAsset):

    def __init__(
        self,
        repo: Repository,
        target: ObjClassInterface,
        webid: IdInterface,
        child: ObjClassInterface,
    ) -> None:

        super().__init__(repo=repo, target=target, webid=webid)

        def check_hierarchy(
            target: ObjClassInterface, child: ObjClassInterface
        ) -> None:
            if child.base_type() in target.children():
                return
            raise ObjHierarchyError(target.__name__, child.__name__)

        check_hierarchy(target, child)
        self._child = child


SplitObjFunc = Callable[
    [JsonObj, ObjClassInterface], tuple[MutableMapping, MutableMapping]
]


class CreateAsset(ParentChildAsset):

    def __init__(
        self,
        repo: Repository,
        target: ObjClassInterface,
        webid: IdInterface,
        child: ObjClassInterface,
        split: SplitObjFunc,
    ) -> None:
        super().__init__(repo, target, webid, child)
        self._split = split

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        # must guarantee comply: tuple[0] db labeltab e tuple[1] com objtab
        base, obj = self._split(inpobj, self._child)

        webid = self._webid.make(self._child.byte_rep())

        self._repo.create(base, obj, webid, self._child.is_tree())

        return {"webid": webid}


class ReadOneAsset(TargetAsset):

    def __call__(self, *fields: str) -> JsonObj:

        sel_fields = self._get_valid_fields(*fields)
        return self._repo.read(*sel_fields)


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

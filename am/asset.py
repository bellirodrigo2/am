""""""

from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import (
    CreateRepository,
    DeleteRepository,
    IdFactoryInterface,
    IdInterface,
    JsonObj,
    LabelInterface,
    ListRepository,
    ObjClassInterface,
    ReadAllOptions,
    ReadRepository,
)


def check_webid(target: ObjClassInterface, webid: IdInterface) -> None:
    if target.byte_rep() == webid.prefix:
        return
    raise InconsistentIdTypeError()


def check_hierarchy(target: ObjClassInterface, child: ObjClassInterface) -> None:
    if child.base_type() in target.children():
        return
    raise ObjHierarchyError()


class TargetAsset:

    def __init__(self, target: ObjClassInterface, webid: IdInterface) -> None:

        check_webid(target, webid)

        self._target = target
        self._webid = webid

    def _fields_list(self) -> tuple[str, ...]:
        label_fields = list(LabelInterface.__annotations__.keys())
        target_fields = list(self._target.get_fields().keys())

        return tuple(set(target_fields + label_fields))


class ParentChildAsset(TargetAsset):

    def __init__(
        self,
        target: ObjClassInterface,
        webid: IdInterface,
        child: ObjClassInterface,
    ) -> None:

        check_hierarchy(target, child)
        super().__init__(target=target, webid=webid)
        self._child = child


def split(obj: JsonObj) -> tuple[dict, dict]:
    return {}, {}


class CreateAsset(ParentChildAsset):

    def __init__(
        self,
        target: ObjClassInterface,
        webid: IdInterface,
        repo: CreateRepository,
        child: ObjClassInterface,
        factory_id: IdFactoryInterface,
    ) -> None:
        super().__init__(target, webid, child)
        self._factory_id = factory_id
        self._repo = repo

    def __call__(self, inpobj: JsonObj) -> JsonObj:

        base, obj = split(inpobj)

        webid = self._factory_id(self._child.byte_rep())
        base["webid"] = webid
        obj["webid"] = webid

        self._repo(base, obj)

        return {"webid": webid}


def get_valid_fields(
    obj_fields: tuple[str, ...], selected_fields: tuple[str, ...] | None
) -> tuple[str, ...] | None:
    if selected_fields:
        return tuple(set(list(obj_fields) + list(selected_fields)))
    return None


def get_valid_field_filters(
    obj_fields: tuple[str, ...], field_filter: dict[str, str] | None
) -> dict[str, str] | None:
    if field_filter:
        return {k: v for k, v in field_filter.items() if k in obj_fields}
    return None


class ReadOneAsset(TargetAsset):

    def __init__(
        self, target: ObjClassInterface, webid: IdInterface, repo: ReadRepository
    ) -> None:
        super().__init__(target, webid)
        self._repo = repo

    def __call__(self, selected_fields: tuple[str, ...]) -> JsonObj:

        fields = get_valid_fields(self._fields_list(), selected_fields)
        return self._repo(selected_fields=fields)


class ReadmanyAsset(ParentChildAsset):

    def __init__(
        self,
        target: ObjClassInterface,
        webid: IdInterface,
        child: ObjClassInterface,
        repo: ListRepository,
    ) -> None:
        super().__init__(target, webid, child)
        self._repo = repo

    def __call__(self, options: ReadAllOptions) -> tuple[JsonObj, ...]:

        valid_fields = self._fields_list()

        options.selected_fields = get_valid_fields(
            valid_fields, options.selected_fields
        )
        options.field_filter = get_valid_field_filters(
            valid_fields, options.field_filter
        )
        options.field_filter_like = get_valid_field_filters(
            valid_fields, options.field_filter_like
        )

        search_full = options.search_full_hierarchy
        search_full = search_full if self._target.is_tree() else False

        return self._repo(options=options)


# class UpdateAsset(ParentChildAsset):
# def __call__(self, updobj: UpdateObj) -> JsonObj:
# pass


class DeleteAsset(TargetAsset):

    def __init__(
        self, target: ObjClassInterface, webid: IdInterface, repo: DeleteRepository
    ) -> None:
        super().__init__(target, webid)
        self._repo = repo

    def __call__(self) -> None:

        self._repo()

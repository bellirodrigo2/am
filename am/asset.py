""" Asset Manager Service """

from pydantic import ValidationError

from am.exceptions import (AMValidationError, AssetHierarchyError,
                           WebIdValidationError)
from am.interfaces import AssetDAOInterface, JsonReponse, ReadAllOptions
from am.schemas.schemas import (InputObj, Obj, ObjEnum, WebId,
                                is_valid_obj, is_valid_parent)
from am.schemas.webid import webid_from_string


###############################################################################


def check_hierarchy(parent: ObjEnum, children: ObjEnum):
    if is_valid_parent(parent, children) is False:
        err = f"Object type {parent=} can not has a child of type {children}"
        raise AssetHierarchyError(err)


def filter_response(
    obj: dict, selected_fields: tuple[str, ...] | None = None
) -> JsonReponse:
    return (
        {field: obj[field] for field in selected_fields if field in obj}
        if selected_fields
        else obj
    )


def add_link(filtered: JsonReponse, target: ObjEnum) -> JsonReponse:
    filtered["Links"] = []
    return filtered


class AssetService:
    """"""

    def __init__(
        self,
        dao: AssetDAOInterface,
    ) -> None:
        self.__dao = dao

    def _add_one(self, webid: WebId, obj_type: ObjEnum, obj: Obj) -> WebId:
        return self.__dao.create(webid=webid, obj=obj)

    def _get_one(
        self, webid: WebId, selected_fields: tuple[str, ...] | None = None
    ) -> Obj:
        return self.__dao.read(webid=webid, selected_fields=selected_fields)

    def _get_all(
        self, webid: WebId, child: ObjEnum, options: ReadAllOptions | None
    ) -> tuple[Obj, ...]:
        return self.__dao.list(webid=webid, children=child, options=options)

    def read(
        self,
        webid: WebId | str,
        target: ObjEnum,
        selected_fields: tuple[str, ...] | None = None,
    ) -> JsonReponse:

        try:
            id = webid_from_string(webid) if isinstance(webid, str) else webid
        except ValueError:
            raise WebIdValidationError()

        obj: Obj = self._get_one(webid=id, selected_fields=selected_fields)

        # if obj does not comply with the target pydantic model target Pydantic model,
        # an ValidationError is raised
        try:
            is_valid_obj(target, obj)
        except ValidationError as e:
            raise AMValidationError(e)

        dictobj = obj.model_dump()
        filtered: JsonReponse = (
            filter_response(dictobj, selected_fields) if selected_fields else dictobj
        )
        return add_link(filtered, target)

    def list(
        self,
        webid: WebId | str,
        parent: ObjEnum,
        children: ObjEnum,
        options: ReadAllOptions | None,
    ) -> tuple[JsonReponse, ...]:
        """"""

        try:
            id = webid_from_string(webid) if isinstance(webid, str) else webid
        except ValueError:
            raise WebIdValidationError()

        check_hierarchy(parent, children)

        # **** SE O ID TIVER INFO DE TYPE, ESSE GET NAO PRECISA (um query a menos)
        parent_obj: Obj = self._get_one(id)
        try:
            is_valid_obj(parent, parent_obj)
        except ValidationError as e:
            raise AMValidationError(e)

        # if parent/children is valid, and parent obj is the rigth type,
        # the _get_all() results type should be consistent
        objs: tuple[Obj, ...] = self._get_all(webid=id, child=children, options=options)
        selected_fields = options.selected_fields if options else None
        filtereds: tuple[JsonReponse, ...] = tuple(
            [filter_response(obj.model_dump(), selected_fields) for obj in objs]
        )
        return filtereds

    def create(
        self, webid: WebId | str, parent: ObjEnum, children: ObjEnum, inputobj: InputObj
    ) -> WebId:

        try:
            id = webid_from_string(webid) if isinstance(webid, str) else webid
        except ValueError:
            raise WebIdValidationError()

        check_hierarchy(parent, children)

        try:
            is_valid_obj(children, inputobj)
        except ValidationError as e:
            raise AMValidationError(e)

        obj = Obj(**inputobj.model_dump())

        return self._add_one(webid=id, obj_type=children, obj=obj)


if __name__ == "__main__":

    obj1 = {
        "Name": "cfweqwwq",
        "Descr": "xxxxxxxx",
        "Age": 45,
        "isOK": True,
    }

    selected = ["Name"]
    assert "Name" in filter_response(obj1, tuple(selected))
    assert "Descr" not in filter_response(obj1, tuple(selected))
    assert "Age" not in filter_response(obj1, tuple(selected))
    assert "isOK" not in filter_response(obj1, tuple(selected))
    selected.append("Age")
    assert "Name" in filter_response(obj1, tuple(selected))
    assert "Descr" not in filter_response(obj1, tuple(selected))
    assert "Age" in filter_response(obj1, tuple(selected))
    assert "isOK" not in filter_response(obj1, tuple(selected))
    selected.append("Descr")
    assert "Name" in filter_response(obj1, tuple(selected))
    assert "Descr" in filter_response(obj1, tuple(selected))
    assert "Age" in filter_response(obj1, tuple(selected))
    assert "isOK" not in filter_response(obj1, tuple(selected))
    selected.append("isOK")
    assert "Name" in filter_response(obj1, tuple(selected))
    assert "Descr" in filter_response(obj1, tuple(selected))
    assert "Age" in filter_response(obj1, tuple(selected))
    assert "isOK" in filter_response(obj1, tuple(selected))
    selected.append("NOEXISTENTFIELD")
    assert "Name" in filter_response(obj1, tuple(selected))
    assert "Descr" in filter_response(obj1, tuple(selected))
    assert "Age" in filter_response(obj1, tuple(selected))
    assert "isOK" in filter_response(obj1, tuple(selected))
    assert len(filter_response(obj1)) == 0

from collections.abc import Iterable
from typing import Any

from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import IdInterface
from am.schemas.baseclass import BaseClass
from am.schemas.objects.assetserver import AssetServer
from am.schemas.objects.database import DataBase
from am.schemas.objects.dataserver import DataServer
from am.schemas.objects.item import Item
from am.schemas.objects.keywords import Keywords
from am.schemas.objects.node import Node
from am.schemas.objects.points import Point
from am.schemas.objects.view import View
from am.schemas.webid import WebId

get_class: dict[str, type[BaseClass]] = {
    "assetserver": AssetServer,
    "dataserver": DataServer,
    "database": DataBase,
    "keywords": Keywords,
    "point": Point,
    "view": View,
    "node": Node,
    "item": Item,
}

get_byte_prefix: dict[str, bytes] = {
    "assetserver": b"asse",
    "dataserver": b"dase",
    "database": b"daba",
    "keywords": b"kewo",
    "points": b"pont",
    "view": b"view",
    "node": b"node",
    "item": b"item",
}


def make_id(target: str) -> IdInterface:
    return WebId(_pref=get_byte_prefix[target])


def make_node(target: str, **kwargs: Any) -> BaseClass:

    target_cls: type[BaseClass] = get_class[target]

    return target_cls(**kwargs)


def check_node_hierarchy(parent: str, child: str) -> None:

    parent_cls: type[BaseClass] = get_class[parent]
    child_cls: type[BaseClass] = get_class[child]

    if child_cls.base_type() in parent_cls.children():
        return
    raise ObjHierarchyError(parent=parent, child=child)


def check_webid(target: str, webid: IdInterface) -> None:

    if get_byte_prefix[target] == webid.prefix:
        return
    raise InconsistentIdTypeError(target=target, webid=str(webid))


def get_fields(target: str) -> Iterable[str]:

    target_cls: type[BaseClass] = get_class[target]
    return target_cls.model_fields.keys()

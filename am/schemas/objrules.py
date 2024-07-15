from dataclasses import dataclass
from typing import Any, Container, Generic, TypeVar

from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import IdInterface
from am.schemas import webid
from am.schemas.baseclass import BaseClass
from am.schemas.label import make_input_fields, make_update_fields
from am.schemas.objects import metadata
from am.schemas.objects.assetserver import AssetServer
from am.schemas.objects.collection import Collection
from am.schemas.objects.database import DataBase
from am.schemas.objects.dataserver import DataServer
from am.schemas.objects.enumset import EnumSet
from am.schemas.objects.item import Item
from am.schemas.objects.keyword import Keyword
from am.schemas.objects.node import Node
from am.schemas.objects.point import Point
from am.schemas.objects.templateitem import TemplateItem
from am.schemas.objects.templatenode import TemplateNode
from am.schemas.objects.user import User
from am.schemas.objects.view import View
from am.schemas.webid import WebId

_T = TypeVar("_T")


class _Getter(Generic[_T]):
    def get(self, target: str) -> _T:
        return getattr(self, target)


@dataclass(frozen=True, slots=True)
class _GetClass(_Getter[type[BaseClass]]):
    assetserver = AssetServer
    dataserver = DataServer
    database = DataBase
    user = User
    keyword = Keyword
    enumset = EnumSet
    point = Point
    view = View
    node = Node
    templatenode = TemplateNode
    item = Item
    templateitem = TemplateItem
    collection = Collection
    metadata = metadata.Metadata


@dataclass(frozen=True, slots=True)
class _GetByte(_Getter[bytes]):
    assetserver = b"asse"
    dataserver = b"dase"
    database = b"daba"
    user = b"user"
    keyword = b"kewo"
    enumset = b"enum"
    point = b"poin"
    view = b"view"
    node = b"node"
    templatenode = b"teno"
    item = b"item"
    templateitem = b"teit"
    collection = b"cole"
    metadata = b"meta"


constr = Container[str]


@dataclass(frozen=True, slots=True)
class _ParentConstraint(_Getter[Container[str]]):
    assetserver: constr = ()
    dataserver: constr = ()
    database: constr = "assetserver"
    user: constr = "assetserver"
    enumset: constr = ("database", "user")
    point: constr = ("dataserver",)
    view: constr = ("node", "item", "templatenode", "templateitem")
    node: constr = ("node", "database")
    templatenode: constr = ("templatenode", "database", "user")
    item: constr = ("node", "item")
    templateitem: constr = ("templatenode", "templateitem")
    collection: constr = ("database", "user")
    metadata: constr = ("database", "user")
    keyword: constr = ("node", "item", "templatenode", "templateitem")


class_getter = _GetClass()
byte_getter = _GetByte()
parent_constr_getter = _ParentConstraint()


def _make_id(target: str, id_cls: type[IdInterface] = WebId) -> IdInterface:

    target_byte = byte_getter.get(target)
    return id_cls.make(input=target_byte)


def check_id(target: str, id: IdInterface) -> None:

    target_byte = byte_getter.get(target)
    if target_byte != id.prefix:
        raise InconsistentIdTypeError(target=target, webid=str(id))


def check_hierarchy(target: str, child: str) -> None:

    parent_constr = parent_constr_getter.get(child)
    if target not in parent_constr:
        raise ObjHierarchyError(target, child)


def make_input_object(target: str, **kwargs: Any) -> BaseClass:
    target_cls: type[BaseClass] = class_getter.get(target)

    new_webid = _make_id(target)
    full_kwargs = make_input_fields(webid=str(new_webid), **kwargs)
    # full_kwargs["web_id"] = _make_id(target, id_cls=WebId)

    return target_cls(**full_kwargs)


def _get_fields(target: str) -> set[str]:

    target_cls: type[BaseClass] = class_getter.get(target)

    return set(target_cls.model_fields.keys())


def split_fields(target: str, *fields: str) -> tuple[set[str], set[str]]:

    if not fields:
        return _get_fields(target), set()

    s1 = _get_fields(target)
    s2 = set(fields)

    return s1 & s2, s2 - s1

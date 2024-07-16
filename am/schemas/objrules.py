from dataclasses import dataclass, field
from typing import Any, Container, Generic, TypeVar

from am.exceptions import InconsistentIdTypeError, InvalidIdError, ObjHierarchyError
from am.interfaces import TreeNodeInterface
from am.schemas.baseclass import BaseClass
from am.schemas.id_.errors import InvalidId
from am.schemas.id_.objectid import ObjectId
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
    assetserver: bytes = field(default=b"asse")
    dataserver: bytes = field(default=b"dase")
    database: bytes = field(default=b"daba")
    user: bytes = field(default=b"user")
    keyword: bytes = field(default=b"kewo")
    enumset: bytes = field(default=b"enum")
    point: bytes = field(default=b"poin")
    view: bytes = field(default=b"view")
    node: bytes = field(default=b"node")
    templatenode: bytes = field(default=b"teno")
    item: bytes = field(default=b"item")
    templateitem: bytes = field(default=b"teit")
    collection: bytes = field(default=b"cole")
    metadata: bytes = field(default=b"meta")


constr = Container[str]


@dataclass(frozen=True, slots=True)
class _ParentConstraint(_Getter[Container[str]]):
    assetserver: constr = ()
    dataserver: constr = ()
    database: constr = ("assetserver",)
    user: constr = ("assetserver",)
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

literal_bytes = [getattr(byte_getter, s) for s in byte_getter.__slots__]


@dataclass(frozen=True)
class WebId:
    pref: bytes
    bid: str | None

    def __post_init__(self):

        if self.pref not in literal_bytes:
            raise InvalidIdError(str(self.pref))

        try:
            id = ObjectId(self.bid) or ObjectId()
        except InvalidId:
            raise InvalidIdError(self.bid)  # type: ignore

        object.__setattr__(self, "bid", id)

    def __str__(self) -> str:
        return self.pref.decode(encoding="utf8") + str(self.bid)

    def __bytes__(self) -> bytes:
        return self.pref + self.bid.encode("utf-8")  # type: ignore


def _cast_id(id: str) -> WebId:

    pref = id[:4].encode("utf-8")

    # try:
    oid = id[4:]
    # except InvalidId:
    # raise InvalidIdError(id)

    return WebId(pref=pref, bid=oid)


def _make_new_id(target: str) -> WebId:

    target_byte = byte_getter.get(target)
    return WebId(pref=target_byte, bid=None)


def check_id(target: str, id: str) -> None:

    webid = _cast_id(id=id)
    target_byte = byte_getter.get(target)
    if target_byte != webid.pref:
        raise InconsistentIdTypeError(target=target, webid=str(id))


def check_hierarchy(target: str, child: str) -> None:

    parent_constr = parent_constr_getter.get(child)
    if target not in parent_constr:
        raise ObjHierarchyError(target, child)


def make_input_object(target: str, **kwargs: Any) -> TreeNodeInterface:
    target_cls: type[BaseClass] = class_getter.get(target)

    new_webid = _make_new_id(target)
    full_kwargs = make_input_fields(webid=str(new_webid), **kwargs)

    return target_cls(**full_kwargs)  # type: ignore


def _get_fields(target: str) -> set[str]:

    target_cls: type[BaseClass] = class_getter.get(target)

    return set(target_cls.model_fields.keys())


def split_fields(target: str, *fields: str) -> tuple[set[str], set[str]]:

    if not fields:
        return _get_fields(target), set()

    s1 = _get_fields(target)
    s2 = set(fields)

    return s1 & s2, s2 - s1

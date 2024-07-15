from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Container, Generic, TypeVar

from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import IdInterface
from am.schemas.baseclass import BaseClass
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


def all_subclasses(cls: type) -> Iterable[Any]:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


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


def make_id(target: str, id_cls: type[IdInterface] = WebId) -> IdInterface:

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


def cast_object(target: str, **kwargs: Any) -> BaseClass:
    target_cls: type[BaseClass] = class_getter.get(target)
    return target_cls(**kwargs)


def _get_fields(target: str) -> set[str]:

    target_cls: type[BaseClass] = class_getter.get(target)

    return set(target_cls.model_fields.keys())


def split_fields(target: str, *fields: str) -> tuple[set[str], set[str]]:

    if not fields:
        return _get_fields(target), set()

    s1 = _get_fields(target)
    s2 = set(fields)

    return s1 & s2, s2 - s1


# @dataclass(frozen=True, slots=True)
# class IdHandler:

#     id_cls: type[IdInterface] = field(default=WebId)
#     get_byte: _GetByte = field(default=byte_getter)

#     def make(self, target: str) -> IdInterface:

#         target_byte = self.get_byte.get(target)
#         return self.id_cls.make(input=target_byte)

#     def check(self, target: str, id: IdInterface) -> None:

#         target_byte = self.get_byte.get(target)
#         if target_byte == id.prefix:
#             return
#         raise InconsistentIdTypeError(target=target, webid=str(id))

# @dataclass(frozen=True, slots=True)
# class ObjectClassHandler:

#     get_class: _GetClass = field(default=class_getter)

#     def make(self, target: str, **kwargs: Any) -> BaseClass:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_cls = self.get_class.get(target)
#         return target_cls(**kwargs)

#     def get(self, target: str) -> tuple[str, ...]:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_cls: type[BaseClass] = self.get_class.get(target)

#         return tuple(target_cls.model_fields.keys())


# @dataclass(frozen=True, slots=True)
# class ObjectsRules:
#     __id_cls__: type[IdInterface]

#     get_class: _GetClass = field(default=class_getter)
#     get_byte: _GetByte = field(default=byte_getter)
#     parent_constr: _ParentConstraint = field(default=parent_constr_getter)

#     def make_id(self, target: str) -> IdInterface:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_byte = self.get_byte.get(target)
#         return self.__id_cls__.make(input=target_byte)

#     def check_id(self, target: str, id: IdInterface) -> None:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_byte = self.get_byte.get(target)
#         if target_byte == id.prefix:
#             return
#         raise InconsistentIdTypeError(target=target, webid=str(id))

#     def make_node(self, target: str, **kwargs: Any) -> BaseClass:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_cls = self.get_class.get(target)
#         return target_cls(**kwargs)

#     def check_hierarchy(self, target: str, child: str) -> None:

#         parent_constr = self.parent_constr.get(child)
#         if target in parent_constr:
#             return

#         # target_cls: type[BaseClass] = getattr(self, target)
#         # child_cls: type[BaseClass] = getattr(self, child)
#         # if child_cls.base_type() in target_cls.children():
#         # par_constr: Iterable[str] | None = child_cls.parent_constr()
#         # if par_constr is None or (
#         # target_cls.base_type() in par_constr
#         # or target_cls.__name__.lower() in par_constr
#         # ):
#         # return
#         raise ObjHierarchyError(parent=target, child=child)

#     def get_fields(self, target: str) -> Iterable[str]:

#         # target_cls: type[BaseClass] = getattr(self, target)
#         target_cls: type[BaseClass] = self.get_class.get(target)

#         return target_cls.model_fields.keys()

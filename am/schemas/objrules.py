from collections.abc import Iterable
from dataclasses import dataclass
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


def all_subclasses(cls: type) -> Iterable[Any]:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


@dataclass(frozen=True, slots=True)
class ObjectsRules:
    __id_cls__: type[IdInterface]

    assetserver: type[BaseClass] = AssetServer
    dataserver: type[BaseClass] = DataServer
    database: type[BaseClass] = DataBase
    keywords: type[BaseClass] = Keywords
    point: type[BaseClass] = Point
    view: type[BaseClass] = View
    node: type[BaseClass] = Node
    item: type[BaseClass] = Item

    def make_id(self, target: str) -> IdInterface:

        target_cls: type[BaseClass] = getattr(self, target)
        return self.__id_cls__.make(input=target_cls.byte_rep())

    def check_id(self, target: str, id: IdInterface) -> None:

        target_cls: type[BaseClass] = getattr(self, target)
        if target_cls.byte_rep() == id.prefix:
            return
        raise InconsistentIdTypeError(target=target, webid=str(id))

    def make_node(self, target: str, **kwargs: Any) -> BaseClass:

        target_cls: type[BaseClass] = getattr(self, target)
        return target_cls(**kwargs)

    def check_hierarchy(self, target: str, child: str) -> None:

        target_cls: type[BaseClass] = getattr(self, target)
        child_cls: type[BaseClass] = getattr(self, child)

        if child_cls.base_type() in target_cls.children():
            return
        raise ObjHierarchyError(parent=target, child=child)

    def get_fields(self, target: str) -> Iterable[str]:

        target_cls: type[BaseClass] = getattr(self, target)
        return target_cls.model_fields.keys()

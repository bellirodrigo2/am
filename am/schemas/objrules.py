from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from am.exceptions import InconsistentIdTypeError, InvalidTargetError, ObjHierarchyError
from am.interfaces import IdInterface, TreeNodeInterface
from am.schemas.labelfactory import make_label
from am.schemas.objects.assetserver import AssetServer
from am.schemas.objects.collection import Collection
from am.schemas.objects.database import DataBase
from am.schemas.objects.dataserver import DataServer
from am.schemas.objects.enumset import EnumSet
from am.schemas.objects.item import Item
from am.schemas.objects.keyword import Keyword
from am.schemas.objects.metadata import Metadata
from am.schemas.objects.node import Node
from am.schemas.objects.point import Point
from am.schemas.objects.templateitem import TemplateItem
from am.schemas.objects.templatenode import TemplateNode
from am.schemas.objects.user import User
from am.schemas.objects.view import View
from am.schemas.webid import Id

Rules = tuple[type[TreeNodeInterface], bytes, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class _GetRules:

    assetserver: Rules = field(default=(AssetServer, b"asse", ()))
    dataserver: Rules = field(default=(DataServer, b"dase", ()))
    database: Rules = field(default=(DataBase, b"daba", ("assetserver",)))
    user: Rules = field(default=(User, b"user", ("assetserver",)))
    keyword: Rules = field(
        default=(Keyword, b"kewo", ("node", "item", "templatenode", "templateitem"))
    )
    enumset: Rules = field(default=(EnumSet, b"enum", ("database", "user")))
    point: Rules = field(default=(Point, b"poin", ("dataserver",)))
    view: Rules = field(
        default=(View, b"view", ("node", "item", "templatenode", "templateitem"))
    )
    node: Rules = field(default=(Node, b"node", ("node", "database", "user")))
    templatenode: Rules = field(
        default=(TemplateNode, b"teno", ("templatenode", "database", "user"))
    )
    item: Rules = field(default=(Item, b"item", ("node", "item")))
    templateitem: Rules = field(
        default=(TemplateItem, b"teit", ("templatenode", "templateitem"))
    )
    collection: Rules = field(default=(Collection, b"cole", ("database", "user")))
    metadata: Rules = field(default=(Metadata, b"meta", ("database", "user")))

    def _get(self, target: str) -> Rules:
        return getattr(self, target)

    def get_class(self, target: str) -> type[TreeNodeInterface]:
        return self._get(target)[0]

    def get_byte(self, target: str) -> bytes:
        return self._get(target)[1]

    def get_parent_constr(self, target: str) -> tuple[str, ...]:
        return self._get(target)[2]


rules = _GetRules()

literal_targets = [s for s in rules.__slots__]
literal_bytes = [rules.get_byte(s) for s in literal_targets]


class WebId(Id):

    @classmethod
    def _pref_options(cls) -> Iterable[bytes]:
        return literal_bytes


def _check_target_valid(target: str) -> None:
    if target not in literal_targets:
        raise InvalidTargetError(target)


def _cast_id(id: str) -> IdInterface:

    pref = id[:4].encode("utf-8")
    oid = id[4:]

    return WebId(pref=pref, bid=oid)


def _make_new_id(target: str) -> IdInterface:

    target_byte = rules.get_byte(target)
    return WebId(pref=target_byte)


def check_id(target: str, id: str) -> IdInterface:

    _check_target_valid(target)

    webid = _cast_id(id=id)
    target_byte = rules.get_byte(target)
    if target_byte != webid.pref:
        raise InconsistentIdTypeError(target=target, webid=str(id))
    return webid


def check_hierarchy(target: str, child: str) -> None:

    _check_target_valid(child)
    parent_constr = rules.get_parent_constr(child)
    if target not in parent_constr:
        raise ObjHierarchyError(target, child)


def make_input_object(target: str, **kwargs: Any) -> TreeNodeInterface:

    target_cls: type[TreeNodeInterface] = rules.get_class(target)

    new_webid = _make_new_id(target)
    full_kwargs = make_label(webid=new_webid, **kwargs)

    return target_cls(**full_kwargs)


def _get_fields(target: str) -> set[str]:

    target_cls: type[TreeNodeInterface] = rules.get_class(target)

    return set(target_cls.get_fields())


def split_fields(target: str, *fields: str) -> tuple[set[str], set[str]]:

    tgt_fields = _get_fields(target)

    if not fields:
        return tgt_fields, set()

    s1 = tgt_fields
    s2 = set(fields)

    return s1 & s2, s2 - s1

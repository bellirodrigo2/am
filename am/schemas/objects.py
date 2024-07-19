from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from am.interfaces import TreeNodeInterface
from am.schemas.entry import Entry, make_id
from am.schemas.label import make_label
from am.schemas.models.assetserver import AssetServer
from am.schemas.models.collection import Collection
from am.schemas.models.database import DataBase
from am.schemas.models.dataserver import DataServer
from am.schemas.models.enumset import EnumSet
from am.schemas.models.item import Item
from am.schemas.models.keyword import Keyword
from am.schemas.models.metadata import Metadata
from am.schemas.models.node import Node
from am.schemas.models.point import Point
from am.schemas.models.templateitem import TemplateItem
from am.schemas.models.templatenode import TemplateNode
from am.schemas.models.user import User
from am.schemas.models.view import View

Rules = tuple[type[TreeNodeInterface], tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class _GetRules:

    assetserver: Rules = field(default=(AssetServer, ()))
    dataserver: Rules = field(default=(DataServer, ()))
    database: Rules = field(default=(DataBase, ("assetserver",)))
    user: Rules = field(default=(User, ("assetserver",)))
    keyword: Rules = field(
        default=(Keyword, ("node", "item", "templatenode", "templateitem"))
    )
    enumset: Rules = field(default=(EnumSet, ("database", "user")))
    point: Rules = field(default=(Point, ("dataserver",)))
    view: Rules = field(
        default=(View, ("node", "item", "templatenode", "templateitem"))
    )
    node: Rules = field(default=(Node, ("node", "database", "user")))
    templatenode: Rules = field(
        default=(TemplateNode, ("templatenode", "database", "user"))
    )
    item: Rules = field(default=(Item, ("node", "item")))
    templateitem: Rules = field(
        default=(TemplateItem, ("templatenode", "templateitem"))
    )
    collection: Rules = field(default=(Collection, ("database", "user")))
    metadata: Rules = field(default=(Metadata, ("database", "user")))

    def _get(self, target: str) -> Rules:
        return getattr(self, target)

    def get_class(self, target: str) -> type[TreeNodeInterface]:
        return self._get(target)[0]

    def get_parent_constr(self, target: str) -> tuple[str, ...]:
        return self._get(target)[1]


rules = _GetRules()

literal_targets = [s for s in rules.__slots__]


class AssetEntry(Entry):

    @classmethod
    def _options(cls) -> Iterable[str]:
        return literal_targets

    @classmethod
    def _parents(cls, child: str) -> Iterable[str]:
        return rules.get_parent_constr(child)


def make_input_object(target: str, **kwargs: Any) -> TreeNodeInterface:  # type: ignore

    target_cls: type[TreeNodeInterface] = rules.get_class(target)

    new_webid = make_id()
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

from collections.abc import Container

from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(Label, Visitable):

    @classmethod
    def base_type(cls) -> str:
        return "base"

    @classmethod
    def children(cls) -> Container[str]:
        return []


class BaseServer(BaseClass):

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "serverelement", "root"]


class BaseRoot(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "rootelement", "node"]


class BaseElement(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> Container[str]:
        return []


class ServerElement(BaseElement):
    @classmethod
    def base_type(cls) -> str:
        return "serverelement"


class RootElement(BaseElement):
    @classmethod
    def base_type(cls) -> str:
        return "rootelement"


class TreeElement(BaseElement):
    @classmethod
    def base_type(cls) -> str:
        return "treeelement"


class NodeElement(BaseElement):
    @classmethod
    def base_type(cls) -> str:
        return "nodeelement"


class ItemElement(BaseElement):
    @classmethod
    def base_type(cls) -> str:
        return "itemelement"


class BaseNode(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element", "nodeelement", "treeelement"]


class BaseItem(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item", "element", "itemelement", "treeelement"]


# NodeType = Literal[
#     "server",
#     "root",
#     "element",
#     "serverelement",
#     "rootelement",
#     "treeelement",
#     "nodeelement",
#     "itemelement",
#     "node",
#     "item",
# ]

# GetBaseNode = Callable[[], NodeType]


# @dataclass(slots=True)
# class BaseNodeVisitor(Visitor):
#     assetserver: GetBaseNode = lambda: "server"
#     dataserver: GetBaseNode = lambda: "server"
#     database: GetBaseNode = lambda: "root"
#     keywords: GetBaseNode = lambda: "element"
#     points: GetBaseNode = lambda: "serverelement"
#     view: GetBaseNode = lambda: "nodeelement"
#     node: GetBaseNode = lambda: "node"
#     item: GetBaseNode = lambda: "item"


# GetNodeChildren = Callable[[], Container[NodeType]]


# @dataclass(slots=True)
# class ChildrenNodeVisitor(Visitor):
#     server: GetNodeChildren = lambda: ["root", "serverelement", "element"]
#     root: GetNodeChildren = lambda: ["element", "rootelement", "node"]
#     element: GetNodeChildren = lambda: []
#     serverelement: GetNodeChildren = lambda: []
#     rootelement: GetNodeChildren = lambda: []
#     treeelement: GetNodeChildren = lambda: []
#     nodeelement: GetNodeChildren = lambda: []
#     itemlement: GetNodeChildren = lambda: []
#     node: GetNodeChildren = lambda: [
#         "node",
#         "item",
#         "element",
#         "nodeelement",
#         "treeelement",
#     ]
#     item: GetNodeChildren = lambda: ["item", "element", "itemelement", "treeelement"]

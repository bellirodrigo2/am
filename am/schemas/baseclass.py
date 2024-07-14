from abc import ABC, abstractmethod
from collections.abc import Container

from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(ABC, Label, Visitable):

    @classmethod
    @abstractmethod
    def base_type(cls) -> str: ...

    # return "base"

    @classmethod
    @abstractmethod
    def children(cls) -> Container[str]: ...

    # return []

    @classmethod
    @abstractmethod
    def byte_rep(cls) -> bytes: ...

    # return b"base"


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
        return ["elementfield"]


class ElementField(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "elementfield"

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

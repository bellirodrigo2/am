from abc import ABC, abstractmethod
from collections.abc import Container
from typing import Iterable

from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(ABC, Label, Visitable):

    @classmethod
    @abstractmethod
    def base_type(cls) -> str: ...

    @classmethod
    @abstractmethod
    def children(cls) -> Container[str]: ...

    @classmethod
    @abstractmethod
    def byte_rep(cls) -> bytes: ...

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return None


class BaseServer(BaseClass):

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "root"]


class BaseRoot(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "node"]


class BaseElement(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> Container[str]:
        return ["elementfield"]


class BaseNode(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element"]


class BaseItem(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item", "element"]


class ElementField(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "elementfield"

    @classmethod
    def children(cls) -> Container[str]:
        return []


# class Strict(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "strict"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return []

from abc import ABC, abstractmethod
from collections.abc import Container, Mapping

from pydantic import BaseModel

from am.schemas.comodel import ObjConfig

# from pydantic.fields import FieldInfo


class BaseClass(BaseModel, ABC):

    mode_config = ObjConfig()

    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def children(cls) -> Container[str]:
        pass

    @classmethod
    @abstractmethod
    def byte_rep(cls) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def is_tree(cls) -> bool:
        pass

    @classmethod
    def get_fields(cls) -> Mapping[str, type | None]:
        return {k: v.annotation for k, v in cls.model_fields.items()}


class BaseServer(BaseClass):

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["root"]

    @classmethod
    def is_tree(cls) -> bool:
        return False


class BaseRoot(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "node"]

    @classmethod
    def is_tree(cls) -> bool:
        return False


class BaseElement(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> Container[str]:
        return []

    @classmethod
    def is_tree(cls) -> bool:
        return False


class BaseNode(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element"]

    @classmethod
    def is_tree(cls) -> bool:
        return True


class BaseItem(BaseClass):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item"]

    @classmethod
    def is_tree(cls) -> bool:
        return True

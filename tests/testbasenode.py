from collections.abc import Container

from am.schemas.mapclass import make_map


class Label:

    @classmethod
    def base_type(cls) -> str:
        return "label"

    @classmethod
    def children(cls) -> Container[str]:
        return []

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"labe"


class BaseServer(Label):

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "serverelement", "root"]

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"serv"


class BaseRoot(Label):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "rootelement", "node"]

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"root"


class BaseElement(Label):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> Container[str]:
        return []

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"elem"


class BaseNode(Label):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element", "nodeelement", "treeelement"]

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"node"


class BaseItem(Label):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item", "element", "itemelement", "treeelement"]

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"item"


classes_map = make_map(Label)

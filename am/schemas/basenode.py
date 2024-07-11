from collections.abc import Container, Mapping
from functools import partial

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from am.visitor import Visitable

ObjConfig = partial(
    ConfigDict,
    alias_generator=AliasGenerator(
        alias=to_camel, validation_alias=to_camel, serialization_alias=to_camel
    ),
    populate_by_name=True,
    use_enum_values=True,
    frozen=True,
    str_strip_whitespace=True,
)


class Label(BaseModel, Visitable):

    mode_config = ObjConfig()

    @classmethod
    def base_type(cls) -> str:
        return "label"

    @classmethod
    def children(cls) -> Container[str]:
        return []


class BaseServer(Label):

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "serverelement", "root"]


class BaseRoot(Label):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "rootelement", "node"]


class BaseElement(Label):
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


class BaseNode(Label):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element", "nodeelement", "treeelement"]


class BaseItem(Label):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item", "element", "itemelement", "treeelement"]

from collections.abc import Container, Mapping
from functools import partial

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

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


class BaseClass(BaseModel):

    mode_config = ObjConfig()

    @classmethod
    def base_type(cls) -> str:
        return "base"

    @classmethod
    def children(cls) -> Container[str]:
        return []

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"labe"

    @classmethod
    def get_fields(cls) -> Mapping[str, type | None]:
        return {k: v.annotation for k, v in cls.model_fields.items()}


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

import os
from functools import partial
from typing import Generator, Type

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, ValidationError
from pydantic.alias_generators import to_camel

from am.schemas.config import get_schema_settings
from am.schemas.loader import load_all_plugins
from am.schemas.makeenums import EnumBase, make_enum, name
from am.schemas.webid import WebId, make_webid, webid_from_string

##############################################################################

SPECIAL_CHARS = ["*", "?", ";", "{", "}", "[", "]", "|", "\\", "`", """, """, ":"]
INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add("/")


def make_name(name) -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{name}{i}"
        i += 1


settings = get_schema_settings()

name_gen = make_name(settings.default_name)

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

NameField = partial(
    Field,
    description="Name Field Description",
    min_length=settings.name_min_length,
    max_length=settings.name_max_length,
)

DescriptionField = partial(
    Field,
    description="Description Field Description",
    min_length=settings.description_min_length,
    max_length=settings.description_max_length,
)

WebIdField = partial(
    Field,
    description="WebId Field Description",
)

ClientIdField = partial(
    Field,
    description="ClientId Field Description",
    min_length=settings.clientid_min_length,
    max_length=settings.clientid_max_length,
)

KeywordsField = partial(
    Field,
    description="",
    # por min e max do tmanho das strings
)


class InputObj(BaseModel):

    @classmethod
    def base_type(cls) -> str:
        return "base"

    @classmethod
    def children(cls) -> list[str]:
        return []

    @classmethod
    def cls_name(cls) -> str:
        return name(cls)

    model_config = ObjConfig(extra="allow")  # to allow derived class casting

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    client_id: str | None = ClientIdField(default_factory=make_webid)
    description: str | None = DescriptionField(default=settings.default_description)
    keywords: list[str] | None = KeywordsField(default=[])


class Obj(InputObj):
    webid: WebId = WebIdField(default_factory=make_webid)


class UpdateObj(BaseModel):
    model_config = ObjConfig(extra="allow")

    name: str | None = NameField(default=None)
    description: str | None = DescriptionField(default=None)
    client_id: str | None = ClientIdField(default=None)
    keywords: list[str] | None = KeywordsField(default=None)


##############################################################################
class BaseServer(InputObj):
    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> list[str]:
        return ["root"]

    model_config = ObjConfig(extra="forbid")


class BaseRoot(InputObj):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> list[str]:
        return ["element", "node"]

    model_config = ObjConfig(extra="forbid")


class BaseElement(InputObj):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra="forbid")


class BaseNode(InputObj):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> list[str]:
        return ["node", "item", "element"]

    model_config = ObjConfig(extra="forbid")


class BaseItem(InputObj):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> list[str]:
        return ["item"]

    model_config = ObjConfig(extra="forbid")


##############################################################################


class EnumInputObj(EnumBase):
    @property
    def base_type(self):
        return self._get_class.base_type()

    @property
    def children(self):
        return self._get_class.children()

    # def make(self, obj):
    #     print(obj, self._get_class[self.name])
    #     return self._get_class[self.name](**obj)


load_all_plugins(os.path.dirname(__file__), "plugins")

ObjEnum: Type[EnumInputObj] = make_enum(InputObj, EnumInputObj)


def is_valid_parent(parent: EnumInputObj, child: EnumInputObj):
    return child.base_type in parent.children

def is_valid_obj(target: ObjEnum, obj: InputObj):
    pass
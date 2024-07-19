from collections.abc import Generator, Mapping
from functools import partial
from typing import Any
from uuid import uuid1

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from am.schemas.config import get_schema_settings

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

settings = get_schema_settings()


class Label(BaseModel):

    model_config = ObjConfig(extra="forbid")

    name: str = Field(
        description="Name Field Description",
        min_length=settings.name_min_length,
        max_length=settings.name_max_length,
        # default=None,
    )
    web_id: str = Field(
        description="ClientId Field Description",
        min_length=settings.webid_min_length,
        max_length=settings.webid_max_length,
        # default=None,
    )
    client_id: str = Field(
        description="ClientId Field Description",
        min_length=settings.clientid_min_length,
        max_length=settings.clientid_max_length,
        # default=None,
    )
    description: str = Field(
        description="Description Field Description",
        min_length=settings.description_min_length,
        max_length=settings.description_max_length,
        # default=None,
    )


SPECIAL_CHARS = ["*", "?", ";", "{", "}", "[", "]", "|", "\\", "`", """, """, ":"]
INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add("/")


def make_name(name: str) -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{name}{i}"
        i += 1


settings = get_schema_settings()

name_gen = make_name(settings.default_name)


def make_label(webid: str, **fields: Any) -> Mapping[str, Any]:

    if "name" not in fields:
        fields["name"] = next(name_gen)
    if "client_id" not in fields:
        fields["client_id"] = str(uuid1())
    if "description" not in fields:
        fields["description"] = settings.default_description
    fields["web_id"] = webid
    return fields

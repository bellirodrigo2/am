from collections.abc import Mapping
from functools import partial
from typing import Any

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from am.schemas.config import get_schema_settings
from am.schemas.webid import Id

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

    name: str | None = Field(
        description="Name Field Description",
        min_length=settings.name_min_length,
        max_length=settings.name_max_length,
        # default=None,
    )
    web_id: Id = Field(
        description="ClientId Field Description",
        min_length=settings.webid_min_length,
        max_length=settings.webid_max_length,
        # default=None,
    )
    client_id: str | None = Field(
        description="ClientId Field Description",
        min_length=settings.clientid_min_length,
        max_length=settings.clientid_max_length,
        # default=None,
    )
    description: str | None = Field(
        description="Description Field Description",
        min_length=settings.description_min_length,
        max_length=settings.description_max_length,
        # default=None,
    )


def make_update_fields(**fields: Any) -> Mapping[str, Any]:

    if "name" not in fields:
        fields["name"] = None
    if "client_id" not in fields:
        fields["client_id"] = None
    if "description" not in fields:
        fields["description"] = None
    fields["web_id"] = None
    return fields

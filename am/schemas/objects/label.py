from functools import partial
from typing import Generator

from pydantic import Field

from am.schemas.basenode import BaseClass
from am.schemas.config import get_schema_settings
from am.schemas.id_.objectid import ObjectId

# from am.schemas.webid import WebId

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

ClientIdField = partial(
    Field,
    description="ClientId Field Description",
    min_length=settings.clientid_min_length,
    max_length=settings.clientid_max_length,
)


class InputLabel(BaseClass):

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    client_id: str | None = ClientIdField(default_factory=ObjectId)
    description: str | None = DescriptionField(default=settings.default_description)


class UpdateLabel(BaseClass):

    name: str | None = NameField(default=None)
    description: str | None = DescriptionField(default=None)
    client_id: str | None = ClientIdField(default=None)

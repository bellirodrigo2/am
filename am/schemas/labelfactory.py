from collections.abc import Generator, Mapping
from typing import Any
from uuid import uuid1

from am.interfaces import IdInterface
from am.schemas.config import get_schema_settings

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


def make_label(webid: IdInterface, **fields: Any) -> Mapping[str, Any]:

    if "name" not in fields:
        fields["name"] = next(name_gen)
    if "client_id" not in fields:
        fields["client_id"] = str(uuid1())
    if "description" not in fields:
        fields["description"] = settings.default_description
    fields["web_id"] = webid
    return fields

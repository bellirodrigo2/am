from functools import partial

from pydantic import AliasGenerator, ConfigDict
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

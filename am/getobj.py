""""""

import os
from enum import Enum
from typing import Iterator

from am.interfaces import ObjClassInterface
from am.schemas.baseobjs import BaseClass
from am.schemas.config import get_schema_settings
from am.schemas.loader import load_all_plugins
from am.schemas.makeobj import make_maps

settings = get_schema_settings()
curdir = os.path.dirname(__file__)

load_all_plugins(curdir, settings.objects_folder)


def lower_name(x: str) -> str:
    return x.lower()


def upper_name(x: str) -> str:
    return x.upper()


str_transf = lower_name

baseclass_map: dict[str, type[BaseClass]] = make_maps(BaseClass, str_transf)

# TODO improve this assert here, to guarantee plugins were loaded OK
assert len(baseclass_map) > 0


ObjClassEnum = Enum(
    "ObjClassEnum", {upper_name(x): f"{lower_name(x)}s" for x in baseclass_map.keys()}
)


def get_obj_class(name: str | Enum) -> ObjClassInterface:

    key = name if isinstance(name, str) else name.name
    return baseclass_map[str_transf(key)]


def get_obj_class_iter() -> Iterator[str]:
    return iter(baseclass_map.keys())

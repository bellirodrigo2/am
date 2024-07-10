from collections.abc import Callable, Iterable, Mapping
from typing import Any


def all_subclasses(cls: type, include_base: bool = True) -> Iterable[Any]:
    cls_set = set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )
    if include_base:
        cls_set.add(cls)
    return cls_set


def make_map(
    base_class: type,
    name_transf: Callable[[str], str] | None = None,
    include_base: bool = True,
) -> Mapping[str, type]:

    nested_classes = all_subclasses(base_class, include_base)

    name_transf = name_transf or (lambda x: x)
    return {name_transf(x.__name__): x for x in nested_classes}

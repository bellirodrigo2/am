""""""

from typing import Callable


def get_deriveds(base_class: type):
    return [c for c in base_class.__subclasses__()]


def get_all_deriveds(base_class: type):

    # TODO make it recursive
    deriveds = [get_deriveds(cls) for cls in get_deriveds(base_class)]

    return [item for sublist in deriveds for item in sublist]


str_conv = Callable[[str], str]


def make_maps(base_class: type, name_transf: str_conv | None) -> dict[str, type]:

    nested_classes = get_all_deriveds(base_class)

    return {
        name_transf(x.__name__) if name_transf else x.__name__: x
        for x in nested_classes
    }

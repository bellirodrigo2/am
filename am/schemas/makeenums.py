""" Enums Factory """

from enum import Enum
from typing import Type

###############################################################################


def name(x):
    return x.__name__.lower()


class EnumBase:

    __factory = None

    @classmethod
    def _init_class(cls, classes_list: list):
        cls.__factory = {name(x): x for x in classes_list}

    @property
    def _get_class(self):
        cls = self.__class__
        return cls.__factory[self.name]

    def make(self, obj):
        return self._get_class(**obj)

    def validate(self, obj):
        self._get_class(**obj)


def get_deriveds(base_class: Type):
    return [c for c in base_class.__subclasses__()]


def get_all_deriveds(base_class: Type):

    # fazer isso recursivo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # fazer uma list acumulativa
    deriveds = [get_deriveds(cls) for cls in get_deriveds(base_class)]

    return [item for sublist in deriveds for item in sublist]


def make_enum(base_class: Type, enum_base: Type[EnumBase], module: str = __package__):

    nested_classes = get_all_deriveds(base_class)

    types_map = [(name(x), f"{name(x)}s") for x in nested_classes]

    enum_base._init_class(nested_classes)

    basename = base_class.__name__
    return Enum(
        basename,
        types_map,
        module=module,
        qualname=f"{module}.{basename}",
        type=enum_base,
    )

""" Container """

from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from enum import Enum
from functools import partial
from typing import Any, Callable

################################################################################

NameConv = Callable[[str], str]


def make_map(base_class: type, name_transf: NameConv | None) -> Mapping[str, type]:

    def get_all_deriveds(base_class: type) -> Iterable[type]:

        def get_deriveds(base_class: type) -> Iterable[type]:
            return [c for c in base_class.__subclasses__()]

        # TODO make it recursive
        deriveds = [get_deriveds(cls) for cls in get_deriveds(base_class)]

        return [item for sublist in deriveds for item in sublist]

    nested_classes = get_all_deriveds(base_class)

    name_transf = name_transf or (lambda x: x)
    return {name_transf(x.__name__): x for x in nested_classes}


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
        # cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class Factory(metaclass=Singleton):

    def __init__(self, clss: type, nameconv: NameConv | None) -> None:
        self._classmap: Mapping[str, type] = make_map(clss, nameconv)
        # TODO improve this assert here, to guarantee plugins were loaded OK
        assert len(self._classmap) > 0
        self._enum: Enum | None = None

    def make_enum(self, title: str, nameconv: NameConv, valueconv: NameConv) -> None:
        if self._enum is None:
            Enum(title, {nameconv(x): valueconv(x) for x in self._classmap.keys()})

    @property
    def enum(self) -> Enum | None:
        if self._enum is None:
            self.make_enum(
                self.__class__.__name__, lambda x: x.lower(), lambda x: x.upper()
            )
        return self._enum

    def get(self, clsname: str) -> type:
        return self._classmap[clsname]

    def __getiitem__(self, clsname: str):
        return self._classmap[clsname]

    def __contains__(self, clsname: str):
        return clsname in self._classmap

    def __iter__(self) -> Iterator[tuple[str, type]]:
        return iter(self._classmap.items())


class Container(metaclass=Singleton):

    def __init__(
        self,
        container: MutableMapping[str, tuple[Callable, dict[str, Any]]] | None = None,
    ) -> None:
        self._container = container or {}

    def __getiitem__(self, key: str):
        return self._container[key]

    def __contains__(self, key: str):
        return key in self._container

    def inject(self, key: str, get_dep: Callable, **configs) -> None:
        """"""
        if key in self._container:
            raise Exception(f"Dependency {key=} already exists")

        self._container[key] = (get_dep, configs)

    def provide(self, key: str, **override_configs) -> Callable:
        """"""
        if key not in self._container:
            raise Exception(f"Dependency {key=} does not exists")

        get_dep, configs = self._container[key]
        merged_config = {**configs, **override_configs}
        return partial(get_dep, **merged_config)


if __name__ == "__main__":

    def get_dep1(name: str, url: str, level: int):
        return f"{name}/{url}/{level}"

    container = Container()

    container.inject(
        "dep1", get_dep=get_dep1, name="RBELLI", url="cahier.com", level=10
    )

    depa = container.provide("dep1")
    print(depa())

    depb = container.provide("dep1", name="NAMe2", url="NEWURL.com", level=45)
    print(depb())

    try:
        depc = container.provide("dep1", NOKEY="NAMe2", url="NEWURL.com", level=45)
        print(depc())
    except Exception as e:
        print(e)

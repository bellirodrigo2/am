""" Container """

from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass, field
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
    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
        # cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


@dataclass(frozen=True, slots=True)
class Factory(metaclass=Singleton):
    _classmap: Mapping[str, type]

    def __post_init__(self) -> None:
        assert len(self._classmap) > 0

    def get(self, clsname: str) -> type:
        return self._classmap[clsname]

    def __getiitem__(self, clsname: str):
        return self._classmap[clsname]

    def __contains__(self, clsname: str):
        return clsname in self._classmap

    def __iter__(self) -> Iterator[tuple[str, type]]:
        return iter(self._classmap.items())


@dataclass(frozen=True, slots=True)
class Container(metaclass=Singleton):

    _container: MutableMapping[str, tuple[Callable[..., Any], dict[str, Any]]] = field(
        default_factory=dict
    )

    def __getiitem__(self, key: str):
        return self._container[key]

    def __contains__(self, key: str):
        return key in self._container

    def inject(self, key: str, get_dep: Callable[..., Any], **configs: Any) -> None:
        """"""
        if key in self._container:
            raise Exception(f"Dependency {key=} already exists")

        self._container[key] = (get_dep, configs)

    def provide(self, key: str, **override_configs: Any) -> Callable[..., Any]:
        """"""
        if key not in self._container:
            raise Exception(f"Dependency {key=} does not exists")

        get_dep, configs = self._container[key]
        merged_config = {**configs, **override_configs}
        return partial(get_dep, **merged_config)


if __name__ == "__main__":
    ...

""" Container """

from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable

################################################################################


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

    def __getiitem__(self, clsname: str) -> type:
        return self._classmap[clsname]

    def __contains__(self, clsname: str) -> bool:
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

    def reset(self) -> None:
        self._container.clear()


if __name__ == "__main__":

    class teste: ...

    class derA(teste): ...

    class derB(teste): ...

    class derC(teste): ...

    class derA2(derA): ...

    class derA3(derA): ...

    class derA4(derA): ...

    class derB2(derB): ...

    class derB3(derB): ...

    class derB4(derB): ...

    class derC2(derC): ...

    class derC3(derC): ...

    class derC4(derC): ...

    def all_subclasses(cls: type) -> Iterable[Any]:
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    print(all_subclasses(teste))

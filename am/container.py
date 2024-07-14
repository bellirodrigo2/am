""" Container """

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable


class Singleton(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
        # cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


DependPack = tuple[Callable[..., Any], dict[str, Any]]


@dataclass(frozen=True, slots=True)
class Container(metaclass=Singleton):

    _container: MutableMapping[str, DependPack] = field(default_factory=dict)

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

""" Container """

from functools import partial
from typing import Any, Callable

from am.singleton import Singleton

################################################################################


class Container(metaclass=Singleton):

    def __init__(self) -> None:
        self._container: dict[str, tuple[Callable, dict[str, Any]]]

    # _container: dict[str, tuple[Callable, dict[str, Any]]] = {}

    def __getiitem__(self, key: str):
        return self._container[key]

    def __contains__(self, key):
        return key in self._container

    def inject(self, key: str, get_dep: Callable, **configs) -> None:
        """"""
        if key in self._container:
            raise Exception()

        self._container[key] = (get_dep, configs)

    def provide(self, key: str, **override_configs) -> Callable:
        """"""
        if key not in self._container:
            raise Exception()

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

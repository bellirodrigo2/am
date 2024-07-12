# from pathlib import Path
# from typing import Mapping

import pytest

from am.container import Container

# from am.schemas.loader import load_all_plugins
# from am.schemas.mapclass import make_map
# from tests.objects.baseobj import BaseObj

# dir: str = str(Path(__file__).parent.resolve())
# load_all_plugins(path=dir, tgt_folder="objects", package_name="tests")

# objmap: Mapping[str, type] = make_map(
# base_class=BaseObj, name_transf=None, include_base=True
# )

name = "RBELLI"
url = "cahier.com"
level = 10


@pytest.fixture
def container() -> Container:

    container = Container()
    container.reset()

    def get_dep1(name: str, url: str, level: int):
        return f"{name}/{url}/{level}"

    container.inject("dep1", get_dep=get_dep1, name=name, url=url, level=level)

    return container


# @pytest.fixture
# def factory() -> Factory:
#     return Factory(_classmap=objmap)


# def test_factory_ok(factory: Factory) -> None:
#     """factory get() should raise no exception if class exists"""

#     factory.get(clsname="BaseObj")
#     factory.get(clsname="Hobby")
#     factory.get(clsname="Aged")
#     factory.get(clsname="Sports")


# def test_factory_unknown(factory: Factory) -> None:
#     """factory get() should raise an exception if class do not exists"""

#     with pytest.raises(expected_exception=Exception):
#         factory.get(clsname="NoClass")


def test_container_default_arg_ok(container: Container):

    dep1 = container.provide("dep1")
    dep1_str = dep1()
    assert name in dep1_str
    assert url in dep1_str
    assert str(level) in dep1_str


def test_container_client_arg_ok(container: Container):

    dep2 = container.provide("dep1", name="NAMe2", url="NEWURL.com", level=45)
    dep2_str = dep2()
    assert name not in dep2_str
    assert url not in dep2_str
    assert str(level) not in dep2_str


def test_container_partial_client_arg_ok(container: Container):

    dep2 = container.provide("dep1", name="NAMe2")
    dep2_str = dep2()
    assert name not in dep2_str
    assert url in dep2_str
    assert str(level) in dep2_str


def test_container_client_arg_nok(container: Container):

    with pytest.raises(expected_exception=Exception):
        dep_raise = container.provide(key="dep1", NOKEY="NAMe2")
        dep_raise()

    with pytest.raises(expected_exception=Exception):
        dep_raise = container.provide("dep1", NOKEY="NAMe2", url="NEWURL.com", level=45)
        dep_raise()

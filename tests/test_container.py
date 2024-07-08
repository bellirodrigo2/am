import pytest

from am.container import Container, Factory
from am.schemas.baseobjs import BaseClass


@pytest.fixture
def container():
    return Container()


@pytest.fixture
def factory():
    return Factory(BaseClass)


def test_container(container):

    def get_dep1(name: str, url: str, level: int):
        return f"{name}/{url}/{level}"

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

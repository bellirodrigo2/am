""""""

import json
import os
from typing import Any

import pytest

from am.daos.inmemory.db import bootstrap
from am.daos.inmemory.memorydao import InMemoryDAO

# from am.schemas.schemas import InputObj, Obj, ObjEnum, WebId

###############################################################################


@pytest.fixture
def test_pack() -> tuple[InMemoryDAO, dict[str, dict[str, Any]]]:

    tree = bootstrap()
    dao = InMemoryDAO(get_db=lambda: tree)
    obj_file = os.path.join(os.path.dirname(__file__), "objs.json")
    with open(obj_file) as f:
        objs: dict[str, dict[str, Any]] = json.load(f)
        assert objs is not None
    return (dao, objs)


def setup_function():
    pass


def test_create_some_nodes(test_pack: tuple):
    dao, objs = test_pack

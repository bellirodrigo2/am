""""""
import pytest
from collections import namedtuple

from am.daos.inmemory.db import bootstrap
from am.daos.inmemory.memorydao import InMemoryDAO

from am.schemas.schemas import InputObj, Obj, ObjEnum, WebId

###############################################################################

TestPack = namedtuple('TestPack', 'dao', 'objs')

@pytest.fixture
def make_tree()->TestPack:

    tree = bootstrap()
    dao = InMemoryDAO(get_db= lambda: tree)
    
    objs: dict[str, InputObj] = {
        
    }
    return TestPack(dao=dao, objs=objs)

def setup_function():
    pass

def test_create_some_nodes(make_tree: InMemoryDAO):
    pass    
    
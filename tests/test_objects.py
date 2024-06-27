""""""
import pytest

from cahier.schemas.schemas import ObjEnum, is_valid_parent

###############################################################################


def obj_type(x):
    return x.__class__.__name__.lower()


def test_enums():
    ObjEnum.assetserver
    ObjEnum.database
    ObjEnum.view
    ObjEnum.node
    ObjEnum.item
    with pytest.raises(Exception):
        ObjEnum.ndie


def test_factories_assetserver():
    arg = {'sourceUrl': "http://example.com:8000/"}
    o = ObjEnum.assetserver
    m = o.make(arg)
    assert o.name == "assetserver"
    assert o.value == "assetservers"
    assert o.base_type == "server"
    assert str(m.source_url) == arg["sourceUrl"]


def test_factories_database():
    arg = {'host': "some_db_field"}
    o = ObjEnum.database
    m = o.make(arg)
    assert o.name == "database"
    assert o.value == "databases"
    assert o.base_type == "root"
    assert m.host == arg['host']


def test_factories_view():
    arg = {'viewStr': "some_view_string"}
    o = ObjEnum.view
    m = o.make(arg)
    assert o.name == "view"
    assert o.value == "views"
    assert o.base_type == "element"
    assert m.view_str == arg["viewStr"]


def test_factories_node():
    arg = {'template':"templated_NOD1E"}
    o = ObjEnum.node
    m = o.make(arg)
    assert o.name == "node"
    assert o.value == "nodes"
    assert o.base_type == "node"
    assert m.template == arg["template"]


def test_factories_item():
    arg = {'type':int}
    o = ObjEnum.item
    m = o.make(arg)
    assert o.name == "item"
    assert o.value == "items"
    assert o.base_type == "item"
    assert m.type == arg["type"]


def test_factories_assetserver_hierarchy():
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.database)
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.view) is False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.node) is False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.item) is False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.assetserver) is False


def test_factories_database_hierarchy():
    assert is_valid_parent(ObjEnum.database, ObjEnum.assetserver) is False
    assert is_valid_parent(ObjEnum.database, ObjEnum.database) is False
    assert is_valid_parent(ObjEnum.database, ObjEnum.view)
    assert is_valid_parent(ObjEnum.database, ObjEnum.node)
    assert is_valid_parent(ObjEnum.database, ObjEnum.item) is False


def test_factories_view_hierarchy():
    assert is_valid_parent(ObjEnum.view, ObjEnum.assetserver) is False
    assert is_valid_parent(ObjEnum.view, ObjEnum.database) is False
    assert is_valid_parent(ObjEnum.view, ObjEnum.view) is False
    assert is_valid_parent(ObjEnum.view, ObjEnum.node) is False
    assert is_valid_parent(ObjEnum.view, ObjEnum.item) is False


def test_factories_node_hierarchy():
    assert is_valid_parent(ObjEnum.node, ObjEnum.assetserver) is False
    assert is_valid_parent(ObjEnum.node, ObjEnum.database) is False
    assert is_valid_parent(ObjEnum.node, ObjEnum.view)
    assert is_valid_parent(ObjEnum.node, ObjEnum.node)
    assert is_valid_parent(ObjEnum.node, ObjEnum.item)


def test_factories_item_hierarchy():
    assert is_valid_parent(ObjEnum.item, ObjEnum.assetserver) is False
    assert is_valid_parent(ObjEnum.item, ObjEnum.database) is False
    assert is_valid_parent(ObjEnum.item, ObjEnum.view) is False
    assert is_valid_parent(ObjEnum.item, ObjEnum.node) is False
    assert is_valid_parent(ObjEnum.item, ObjEnum.item)

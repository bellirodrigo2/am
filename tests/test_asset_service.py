""""""

import json
import os
from unittest.mock import MagicMock

import pytest

from am.asset import AssetService, WebIdValidationError
from am.interfaces import AssetInterface
from am.schemas.schemas import ObjEnum, WebId

###############################################################################


obj_file = os.path.join(os.path.dirname(__file__), "objs.json")
with open(obj_file) as f:
    objs: dict[str, dict] = json.load(f)
    assert objs is not None


oks = {
    ObjEnum.assetserver: objs["assetservers"][0],
    ObjEnum.database: objs["databases"][0],
    ObjEnum.view: objs["views"][0],
    ObjEnum.node: objs["nodes"][0],
    ObjEnum.item: objs["items"][0],
    ObjEnum.proc: objs["procs"][0],
}

mock_repo = MagicMock()
mock_repo.read.side_effect = oks.values()

mock_break_repo = MagicMock()
mock_break_repo.read.side_effect = list(reversed(oks.values()))


def get_objs_list():
    return [
        objs["databases"],
        objs["nodes"],
        objs["procs"],
        objs["views"],
        objs["nodes"],
        objs["items"],
        objs["procs"],
        objs["views"],
        objs["items"],
    ]


mock_list = MagicMock()
mock_list.list.side_effect = get_objs_list()


@pytest.fixture
def mock_asset_service() -> AssetInterface:
    return AssetService(dao=mock_repo)


@pytest.fixture
def mock_broken_asset_service() -> AssetInterface:
    return AssetService(dao=mock_break_repo)


def setup_function():
    mock_repo.reset_mock(side_effect=True)
    mock_break_repo.reset_mock()


@pytest.mark.parametrize("target", oks.keys())
def test_getone_wrongwebid(target, mock_asset_service: AssetInterface):

    id = "1c8acc4a9fbd4aa"

    with pytest.raises(WebIdValidationError):
        mock_asset_service.read(webid=id, target=target)


@pytest.mark.parametrize("target", oks.keys())
def test_getone_ok(target, mock_asset_service: AssetInterface):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"

    o = mock_asset_service.read(webid=id, target=target)

    assert o is not None
    mock_repo.read.assert_called_with(webid=WebId(id), selected_fields=None)
    mock_repo.list.assert_not_called()


@pytest.mark.parametrize("target", oks.keys())
def test_getone_wrong_obj(target: ObjEnum, mock_broken_asset_service: AssetInterface):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"

    with pytest.raises(Exception):
        mock_broken_asset_service.read(webid=id, target=target)


@pytest.mark.parametrize("target", oks.keys())
def test_list_wrongwebid(target, mock_asset_service: AssetInterface):

    id = "1c8acc4a9fbd4aa"

    with pytest.raises(WebIdValidationError):
        mock_asset_service.list(
            webid=id, parent=target, children=ObjEnum.node, options=None
        )


def test_list_ok(mock_asset_service: AssetInterface):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    aser = ObjEnum.assetserver
    db = ObjEnum.database
    proc = ObjEnum.proc
    view = ObjEnum.view
    node = ObjEnum.node
    item = ObjEnum.item

    # precisa entender pq esta passando, mesmo com o fixture errado

    mock_asset_service.list(webid=id, parent=aser, children=db, options=None)
    mock_asset_service.list(webid=id, parent=db, children=node, options=None)
    mock_asset_service.list(webid=id, parent=db, children=proc, options=None)
    mock_asset_service.list(webid=id, parent=db, children=view, options=None)
    mock_asset_service.list(webid=id, parent=node, children=node, options=None)
    mock_asset_service.list(webid=id, parent=node, children=item, options=None)
    mock_asset_service.list(webid=id, parent=node, children=proc, options=None)
    mock_asset_service.list(webid=id, parent=node, children=view, options=None)
    mock_asset_service.list(webid=id, parent=item, children=item, options=None)

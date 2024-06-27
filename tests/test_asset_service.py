""""""
import pytest
from unittest.mock import MagicMock

from icecream import ic

from cahier.interfaces.assetservice import AssetInterface, ReadAllOptions
from cahier.schemas.schemas import ObjEnum, WebId
from cahier.services.asset import AssetService

###############################################################################

oks = {
    ObjEnum.assetserver: {"name" : 'USER', "sourceUrl" : 'http://example.com:8000/'},
    ObjEnum.database :{"name" : 'USER', "client_id" : 'thisisclientid', 'host':'dbURLhere'}, #databases
    ObjEnum.view :{"name" : 'USER', "description" : 'descriptionofthisdb', 'viewStr': 'stringVIEW'}, #views
    ObjEnum.node :{"name" : 'USER', "keywords" : ['foo', 'bar'], "template" : 'NodeTemplate'}, #nodes
    ObjEnum.item :{"name" : 'USER', 'type': bool}, #items
    ObjEnum.proc: {"name" : 'USER', "procStr" : 'whatever'}, #proc
    
}

mock_repo = MagicMock()
mock_repo.read.side_effect = oks.values()

mock_break_repo = MagicMock()
mock_break_repo.read.side_effect = list(reversed(oks.values()))

@pytest.fixture
def mock_asset_service()->AssetInterface:
    return AssetService(get_dao=lambda : mock_repo)

@pytest.fixture
def mock_broken_asset_service()->AssetInterface:
    return AssetService(get_dao=lambda : mock_break_repo)

def setup_function():
    mock_repo.reset_mock(side_effect=True)
    mock_break_repo.reset_mock()

@pytest.mark.parametrize("target", oks.keys())
def test_getone_ok(target, mock_asset_service: AssetInterface):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    
    o = mock_asset_service.read(webid=id, target=target)
    mock_repo.read.assert_called_with(webid=id, selected_fields=None)
    mock_repo.list.assert_not_called()

@pytest.mark.parametrize("target", oks.keys())
def test_getone_wrong_obj(target: ObjEnum, mock_broken_asset_service: AssetInterface):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    
    with pytest.raises(Exception):
        mock_broken_asset_service.read(webid=id, target=target)

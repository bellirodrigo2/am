""""""

from unittest.mock import MagicMock

import pytest

from am.asset import TargetAsset, TargetChildAsset
from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import Repository
from am.schemas.objrules import ObjectsRules
from am.schemas.webid import WebId

rules = ObjectsRules(__id_cls__=WebId)


@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a")),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a")),
        ("view", WebId.make(input="view668540fb5ac420d8fc35320a")),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_ok(target: str, webid: WebId, repo: Repository):
    TargetAsset(
        _repo=repo,
        _rules=rules,
        target=target,
        webid=webid,
    )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("database", WebId.make(input="elem668540fb5ac420d8fc35320a")),
        ("view", WebId.make(input="base668540fb5ac420d8fc35320a")),
        ("node", WebId.make(input="root668540fb5ac420d8fc35320a")),
        ("item", WebId.make(input="node668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_nok(target: str, webid: WebId, repo: Repository):

    with pytest.raises(expected_exception=InconsistentIdTypeError):
        TargetAsset(
            _repo=repo,
            _rules=rules,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "database"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "keywords"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "node"),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a"), "item"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "view"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "enumset"),
    ],
)
def test_parent_asset_ok(target: str, webid: WebId, repo: Repository, child: str):
    TargetChildAsset(
        _repo=repo,
        _rules=rules,
        target=target,
        webid=webid,
        child=child,
    )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "item"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "assetserver"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "database"),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a"), "node"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "view"),
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "enumset"),
    ],
)
def test_parent_asset_nok(target: str, webid: WebId, repo: Repository, child: str):

    with pytest.raises(expected_exception=ObjHierarchyError):
        TargetChildAsset(
            _repo=repo,
            _rules=rules,
            target=target,
            webid=webid,
            child=child,
        )

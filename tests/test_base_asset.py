""""""

from unittest.mock import MagicMock

import pytest

from am.asset import TargetAsset, TargetChildAsset
from am.exceptions import InconsistentIdTypeError, ObjHierarchyError
from am.interfaces import Repository
from am.schemas.objrules import check_hierarchy, check_id
from am.schemas.webid import WebId


@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a")),
        ("dataserver", WebId.make(input="dase668540fb5ac420d8fc35320a")),
        ("enumset", WebId.make(input="enum668540fb5ac420d8fc35320a")),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a")),
        ("keyword", WebId.make(input="kewo668540fb5ac420d8fc35320a")),
        ("view", WebId.make(input="view668540fb5ac420d8fc35320a")),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("templatenode", WebId.make(input="teno668540fb5ac420d8fc35320a")),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_ok(target: str, webid: WebId, repo: Repository):
    TargetAsset(
        _repo=repo,
        _check_id=check_id,
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
        ("templatenode", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("enumset", WebId.make(input="daba668540fb5ac420d8fc35320a")),
        ("point", WebId.make(input="asse668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_nok(target: str, webid: WebId, repo: Repository):

    with pytest.raises(expected_exception=InconsistentIdTypeError):
        TargetAsset(
            _repo=repo,
            _check_id=check_id,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "database"),
        ("dataserver", WebId.make(input="dase668540fb5ac420d8fc35320a"), "point"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "node"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "node"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "item"),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a"), "item"),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a"), "view"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "view"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "enumset"),
    ],
)
def test_parent_asset_ok(target: str, webid: WebId, repo: Repository, child: str):
    TargetChildAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        target=target,
        webid=webid,
        child=child,
    )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "item"),
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "point"),
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "node"),
        ("dataserver", WebId.make(input="dase668540fb5ac420d8fc35320a"), "database"),
        ("dataserver", WebId.make(input="dase668540fb5ac420d8fc35320a"), "view"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "assetserver"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "point"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "keyword"),
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
            _check_id=check_id,
            _check_hierarchy=check_hierarchy,
            target=target,
            webid=webid,
            child=child,
        )

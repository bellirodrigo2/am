""""""

from unittest.mock import MagicMock

import pytest

from am.asset import _TargetAsset, _TargetChildAsset  # type: ignore
from am.exceptions import InconsistentIdTypeError, InvalidIdError, ObjHierarchyError
from am.interfaces import Repository
from am.schemas.objrules import check_hierarchy, check_id


@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "asse668540fb5ac420d8fc35320a"),
        ("dataserver", "dase668540fb5ac420d8fc35320a"),
        ("enumset", "enum668540fb5ac420d8fc35320a"),
        ("database", "daba668540fb5ac420d8fc35320a"),
        ("keyword", "kewo668540fb5ac420d8fc35320a"),
        ("view", "view668540fb5ac420d8fc35320a"),
        ("node", "node668540fb5ac420d8fc35320a"),
        ("templatenode", "teno668540fb5ac420d8fc35320a"),
        ("item", "item668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_ok(target: str, webid: str, repo: Repository):
    _TargetAsset(
        _repo=repo,
        _check_id=check_id,
        target=target,
        webid=webid,
    )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "asse668540fb5xxxxac420d8fc35320a"),
        ("dataserver", "dase668540fb5axxxxxc420d8fc35320a"),
        ("enumset", "enum668320a"),
        ("database", "daba668540fb58fc35320a"),
        ("keyword", "kewo6Aac420d8fc35320a"),
        ("view", "view66820a"),
        ("node", "node6685XX"),
        ("templatenode", "teno66850a"),
        ("item", "item668540fb5ac42FFFFFFFFFFFFFFF0d8fc35320a"),
    ],
)
def test_target_asset_invalidid_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=InvalidIdError):
        _TargetAsset(
            _repo=repo,
            _check_id=check_id,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "node668540fb5ac420d8fc35320a"),
        ("database", "elem668540fb5ac420d8fc35320a"),
        ("view", "base668540fb5ac420d8fc35320a"),
        ("node", "root668540fb5ac420d8fc35320a"),
        ("item", "node668540fb5ac420d8fc35320a"),
        ("templatenode", "node668540fb5ac420d8fc35320a"),
        ("enumset", "daba668540fb5ac420d8fc35320a"),
        ("point", "asse668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_inconsistentid_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=InconsistentIdTypeError):
        _TargetAsset(
            _repo=repo,
            _check_id=check_id,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "asse668540fb5ac420d8fc35320a", "database"),
        ("dataserver", "dase668540fb5ac420d8fc35320a", "point"),
        ("database", "daba668540fb5ac420d8fc35320a", "node"),
        ("node", "node668540fb5ac420d8fc35320a", "node"),
        ("node", "node668540fb5ac420d8fc35320a", "item"),
        ("item", "item668540fb5ac420d8fc35320a", "item"),
        ("item", "item668540fb5ac420d8fc35320a", "view"),
        ("node", "node668540fb5ac420d8fc35320a", "view"),
        ("database", "daba668540fb5ac420d8fc35320a", "enumset"),
    ],
)
def test_parent_asset_ok(target: str, webid: str, repo: Repository, child: str):
    _TargetChildAsset(
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
        ("assetserver", "asse668540fb5ac420d8fc35320a", "item"),
        ("assetserver", "asse668540fb5ac420d8fc35320a", "point"),
        ("assetserver", "asse668540fb5ac420d8fc35320a", "node"),
        ("dataserver", "dase668540fb5ac420d8fc35320a", "database"),
        ("dataserver", "dase668540fb5ac420d8fc35320a", "view"),
        ("database", "daba668540fb5ac420d8fc35320a", "assetserver"),
        ("database", "daba668540fb5ac420d8fc35320a", "point"),
        ("database", "daba668540fb5ac420d8fc35320a", "keyword"),
        ("node", "node668540fb5ac420d8fc35320a", "database"),
        ("item", "item668540fb5ac420d8fc35320a", "node"),
        ("database", "daba668540fb5ac420d8fc35320a", "view"),
        ("assetserver", "asse668540fb5ac420d8fc35320a", "enumset"),
    ],
)
def test_parent_asset_nok(target: str, webid: str, repo: Repository, child: str):

    with pytest.raises(expected_exception=ObjHierarchyError):
        _TargetChildAsset(
            _repo=repo,
            _check_id=check_id,
            _check_hierarchy=check_hierarchy,
            target=target,
            webid=webid,
            child=child,
        )

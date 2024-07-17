""""""

from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from am.asset import _TargetAsset, _TargetChildAsset  # type: ignore
from am.exceptions import (
    InconsistentIdTypeError,
    InvalidIdError,
    InvalidTargetError,
    ObjHierarchyError,
)
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
        ("notarget", "daba668540fb5ac420d8fc35320a"),
        ("nochild", "daba668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_invalid_target_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=InvalidTargetError):
        _TargetAsset(
            _repo=repo,
            _check_id=check_id,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("database", "base668540fb5ac420d8fc35320a"),
        ("keyword", "root668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_invalid_pref_nok(target: str, webid: str, repo: Repository):

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
        ("assetserver", "asse668540fb5xxxxac420d8fc35320a"),
        ("item", "item668540fb5ac42FFFFFFFFFFFFFFF0d8fc35320a"),
        ("view", "view66820a"),
        ("node", "node6685XX"),
    ],
)
def test_target_asset_invalid_bid_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=ValidationError):
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
        ("database", "asse668540fb5ac420d8fc35320a"),
        ("view", "item668540fb5ac420d8fc35320a"),
        ("node", "dase668540fb5ac420d8fc35320a"),
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
        ("assetserver", "asse668540fb5ac420d8fc35320a", "nochild"),
        ("dataserver", "dase668540fb5ac420d8fc35320a", "noexist"),
        ("database", "daba668540fb5ac420d8fc35320a", "foobar"),
    ],
)
def test_parent_asset_invalid_child_nok(
    target: str, webid: str, repo: Repository, child: str
):

    with pytest.raises(expected_exception=InvalidTargetError):
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

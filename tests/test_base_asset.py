""""""

from unittest.mock import MagicMock

import pytest

from am.asset import _TargetAsset, _TargetChildAsset  # type: ignore
from am.exceptions import InvalidIdError, InvalidTargetError
from am.interfaces import Repository
from am.schemas.objects import AssetEntry


@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "668540fb5ac420d8fc35320a"),
        ("dataserver", "668540fb5ac420d8fc35320a"),
        ("enumset", "668540fb5ac420d8fc35320a"),
        ("database", "668540fb5ac420d8fc35320a"),
        ("keyword", "668540fb5ac420d8fc35320a"),
        ("view", "668540fb5ac420d8fc35320a"),
        ("node", "668540fb5ac420d8fc35320a"),
        ("templatenode", "668540fb5ac420d8fc35320a"),
        ("item", "668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_ok(target: str, webid: str, repo: Repository):
    _TargetAsset(
        _repo=repo,
        _validator=AssetEntry,
        target=target,
        webid=webid,
    )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("notarget", "668540fb5ac420d8fc35320a"),
        ("nochild", "668540fb5ac420d8fc35320a"),
    ],
)
def test_target_asset_invalid_target_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=InvalidTargetError):
        _TargetAsset(
            _repo=repo,
            _validator=AssetEntry,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "668540fb5xxxxac420d8fc35320a"),
        ("item", "668540fb5ac42FFFFFFFFFFFFFFF0d8fc35320a"),
        ("view", "66820a"),
        ("node", "6685XX"),
    ],
)
def test_target_asset_invalid_bid_nok(target: str, webid: str, repo: Repository):

    with pytest.raises(expected_exception=InvalidIdError):
        _TargetAsset(
            _repo=repo,
            _validator=AssetEntry,
            target=target,
            webid=webid,
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "668540fb5ac420d8fc35320a", "database"),
        ("dataserver", "668540fb5ac420d8fc35320a", "point"),
        ("database", "668540fb5ac420d8fc35320a", "node"),
        ("node", "668540fb5ac420d8fc35320a", "node"),
        ("node", "668540fb5ac420d8fc35320a", "item"),
        ("item", "668540fb5ac420d8fc35320a", "item"),
        ("item", "668540fb5ac420d8fc35320a", "view"),
        ("node", "668540fb5ac420d8fc35320a", "view"),
        ("database", "668540fb5ac420d8fc35320a", "enumset"),
    ],
)
def test_parent_asset_ok(target: str, webid: str, repo: Repository, child: str):
    _TargetChildAsset(
        _repo=repo,
        _validator=AssetEntry,
        target=target,
        webid=webid,
        child=child,
    )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "668540fb5ac420d8fc35320a", "nochild"),
        ("dataserver", "668540fb5ac420d8fc35320a", "noexist"),
        ("database", "668540fb5ac420d8fc35320a", "foobar"),
    ],
)
def test_parent_asset_invalid_child_nok(
    target: str, webid: str, repo: Repository, child: str
):

    with pytest.raises(expected_exception=InvalidTargetError):
        _TargetChildAsset(
            _repo=repo,
            _validator=AssetEntry,
            target=target,
            webid=webid,
            child=child,
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "668540fb5ac420d8fc35320a", "item"),
        ("assetserver", "668540fb5ac420d8fc35320a", "point"),
        ("assetserver", "668540fb5ac420d8fc35320a", "node"),
        ("dataserver", "668540fb5ac420d8fc35320a", "database"),
        ("dataserver", "668540fb5ac420d8fc35320a", "view"),
        ("database", "668540fb5ac420d8fc35320a", "assetserver"),
        ("database", "668540fb5ac420d8fc35320a", "point"),
        ("database", "668540fb5ac420d8fc35320a", "keyword"),
        ("node", "668540fb5ac420d8fc35320a", "database"),
        ("item", "668540fb5ac420d8fc35320a", "node"),
        ("database", "668540fb5ac420d8fc35320a", "view"),
        ("assetserver", "668540fb5ac420d8fc35320a", "enumset"),
    ],
)
def test_parent_asset_nok(target: str, webid: str, repo: Repository, child: str):

    with pytest.raises(expected_exception=InvalidTargetError):
        _TargetChildAsset(
            _repo=repo,
            _validator=AssetEntry,
            target=target,
            webid=webid,
            child=child,
        )

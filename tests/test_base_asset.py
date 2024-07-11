""""""

from unittest.mock import MagicMock

import pytest

from am.asset import (
    InconsistentIdTypeError,
    ObjHierarchyError,
    ParentChildAsset,
    TargetAsset,
)
from am.container import Factory
from am.interfaces import Repository
from am.schemas.webid import WebId

from .testbasenode import ByteRepVisitorTest, classes_map

###############################################################################


factory = Factory(classes_map)
visitor = ByteRepVisitorTest()


# testing TargetAsset
@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid",
    [
        ("BaseServer", WebId.make(input="serv668540fb5ac420d8fc35320a")),
        ("BaseRoot", WebId.make(input="root668540fb5ac420d8fc35320a")),
        ("BaseElement", WebId.make(input="elem668540fb5ac420d8fc35320a")),
        ("BaseNode", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("BaseItem", WebId.make(input="item668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_ok(target: str, webid: WebId, repo: Repository):
    TargetAsset(
        _repo=repo, _factory=factory, _target=target, _webid=webid, _byterep=visitor
    )


@pytest.mark.parametrize(
    "target, webid",
    [
        ("BaseServer", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("BaseRoot", WebId.make(input="elem668540fb5ac420d8fc35320a")),
        ("BaseElement", WebId.make(input="base668540fb5ac420d8fc35320a")),
        ("BaseNode", WebId.make(input="root668540fb5ac420d8fc35320a")),
        ("BaseItem", WebId.make(input="node668540fb5ac420d8fc35320a")),
    ],
)
def test_target_asset_nok(target: str, webid: WebId, repo: Repository):

    with pytest.raises(expected_exception=InconsistentIdTypeError):
        TargetAsset(
            _repo=repo, _factory=factory, _target=target, _webid=webid, _byterep=visitor
        )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("BaseServer", WebId.make(input="serv668540fb5ac420d8fc35320a"), "BaseRoot"),
        ("BaseRoot", WebId.make(input="root668540fb5ac420d8fc35320a"), "BaseElement"),
        ("BaseNode", WebId.make(input="node668540fb5ac420d8fc35320a"), "BaseNode"),
        ("BaseItem", WebId.make(input="item668540fb5ac420d8fc35320a"), "BaseItem"),
    ],
)
def test_parent_asset_ok(target: str, webid: WebId, repo: Repository, child: str):
    ParentChildAsset(
        _repo=repo,
        _factory=factory,
        _target=target,
        _webid=webid,
        _child=child,
        _byterep=visitor,
    )


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("BaseServer", WebId.make(input="serv668540fb5ac420d8fc35320a"), "BaseItem"),
        ("BaseRoot", WebId.make(input="root668540fb5ac420d8fc35320a"), "BaseServer"),
        ("BaseNode", WebId.make(input="node668540fb5ac420d8fc35320a"), "BaseRoot"),
        ("BaseItem", WebId.make(input="item668540fb5ac420d8fc35320a"), "BaseNode"),
    ],
)
def test_parent_asset_nok(target: str, webid: WebId, repo: Repository, child: str):

    with pytest.raises(expected_exception=ObjHierarchyError):
        ParentChildAsset(
            _repo=repo,
            _factory=factory,
            _byterep=visitor,
            _target=target,
            _webid=webid,
            _child=child,
        )

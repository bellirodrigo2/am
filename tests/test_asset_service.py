""""""

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from am.asset import CreateAsset, ReadManyAsset, ReadOneAsset
from am.interfaces import Repository
from am.schemas.nodefuncs import (
    check_node_hierarchy,
    check_webid,
    get_fields,
    make_node,
)
from am.schemas.webid import WebId

obj_file: Path = Path.cwd() / "tests/objs.json"
with open(file=obj_file) as f:
    inputs = json.load(fp=f)
    assert inputs is not None


# testing TargetAsset
@pytest.fixture
def repo() -> Repository:
    return MagicMock()


@pytest.mark.parametrize(
    "target, webid, child, objs",
    [
        (
            "assetserver",
            WebId.make(input="asse668540fb5ac420d8fc35320a"),
            "database",
            inputs["databases"],
        ),
        (
            "node",
            WebId.make(input="node668540fb5ac420d8fc35320a"),
            "view",
            inputs["views"],
        ),
        (
            "node",
            WebId.make(input="node668540fb5ac420d8fc35320a"),
            "node",
            inputs["nodes"],
        ),
        (
            "item",
            WebId.make(input="item668540fb5ac420d8fc35320a"),
            "item",
            inputs["items"],
        ),
    ],
)
def test_create_asset_ok(
    target: str,
    webid: WebId,
    repo: Repository,
    child: str,
    objs: Iterable[Mapping[str, Any]],
):
    create = CreateAsset(
        _repo=repo,
        target=target,
        webid=webid,
        child=child,
        _check_webid=check_webid,
        _fields=get_fields,
        _check_hierarchy=check_node_hierarchy,
        _make=make_node,
    )
    for obj in objs:
        repo.reset_mock()  # type: ignore
        res: Mapping[str, Any] = create(obj)
        repo.create.assert_called_once()  # type: ignore
        assert "webid" in res

        # obj_type = visitor.visit(factory.get(child))
        # assert res["webid"].prefix == obj_type


@pytest.mark.parametrize(
    "target, webid, child",
    [
        (
            "assetserver",
            WebId.make(input="asse668540fb5ac420d8fc35320a"),
            "database",
        ),
        (
            "database",
            WebId.make(input="daba668540fb5ac420d8fc35320a"),
            "node",
        ),
        (
            "node",
            WebId.make(input="node668540fb5ac420d8fc35320a"),
            "node",
        ),
        (
            "item",
            WebId.make(input="item668540fb5ac420d8fc35320a"),
            "item",
        ),
    ],
)
def test_create_asset_nok(
    target: str,
    webid: WebId,
    repo: Repository,
    child: str,
):
    create = CreateAsset(
        _repo=repo,
        target=target,
        webid=webid,
        child=child,
        _check_webid=check_webid,
        _fields=get_fields,
        _check_hierarchy=check_node_hierarchy,
        _make=make_node,
    )
    for obj in inputs["assetservers"]:
        with pytest.raises(expected_exception=ValidationError):
            create(obj)


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a")),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a")),
        ("keywords", WebId.make(input="kewo668540fb5ac420d8fc35320a")),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a")),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a")),
    ],
)
def test_readone_asset_ok(target: str, webid: WebId, repo: Repository):
    readone = ReadOneAsset(
        _repo=repo,
        target=target,
        webid=webid,
        _check_webid=check_webid,
        _fields=get_fields,
    )
    repo.reset_mock()  # type: ignore
    readone()
    repo.read.assert_called_once()  # type: ignore


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", WebId.make(input="asse668540fb5ac420d8fc35320a"), "database"),
        ("database", WebId.make(input="daba668540fb5ac420d8fc35320a"), "node"),
        ("node", WebId.make(input="node668540fb5ac420d8fc35320a"), "node"),
        ("item", WebId.make(input="item668540fb5ac420d8fc35320a"), "item"),
    ],
)
def test_readmany_asset_ok(target: str, webid: WebId, repo: Repository, child: str):
    readmany = ReadManyAsset(
        _repo=repo,
        target=target,
        webid=webid,
        child=child,
        _check_webid=check_webid,
        _fields=get_fields,
        _check_hierarchy=check_node_hierarchy,
    )

    repo.reset_mock()  # type: ignore
    readmany()
    repo.list.assert_called_once()  # type: ignore

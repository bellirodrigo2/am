""""""

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from am.asset import CreateAsset, ReadManyAsset, ReadOneAsset
from am.interfaces import Repository
from am.schemas.objrules import (
    check_hierarchy,
    check_id,
    make_input_object,
    split_fields,
)

obj_file: Path = Path.cwd() / "tests/objs.json"
with open(file=obj_file) as f:
    inputs = json.load(fp=f)
    assert inputs is not None


@pytest.fixture
def repo() -> Repository:
    return AsyncMock()


@pytest.mark.parametrize(
    "target, webid, child, objs",
    [
        (
            "assetserver",
            "asse668540fb5ac420d8fc35320a",
            "database",
            inputs["databases"],
        ),
        (
            "node",
            "node668540fb5ac420d8fc35320a",
            "view",
            inputs["views"],
        ),
        (
            "node",
            "node668540fb5ac420d8fc35320a",
            "node",
            inputs["nodes"],
        ),
        (
            "item",
            "item668540fb5ac420d8fc35320a",
            "item",
            inputs["items"],
        ),
    ],
)
async def test_create_asset_ok(
    target: str,
    webid: str,
    repo: Repository,
    child: str,
    objs: Iterable[Mapping[str, Any]],
):
    create = CreateAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        _cast=make_input_object,
        # _make_id=make_id,
        target=target,
        webid=webid,
        child=child,
    )
    for obj in objs:
        repo.reset_mock()  # type: ignore
        await create(obj)
        repo.create.assert_called_once()  # type: ignore


async def test_create_asset_empty(
    repo: Repository,
):
    create = CreateAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        _cast=make_input_object,
        target="node",
        webid="node668540fb5ac420d8fc35320a",
        child="node",
    )
    res1: Mapping[str, Any] = await create({})
    repo.create.assert_called_once()  # type: ignore
    res2: Mapping[str, Any] = await create({})
    res3: Mapping[str, Any] = await create({})
    assert (
        res1["node"].name != res2["node"].name
        and res2["node"].name != res3["node"].name
        and res1["node"].name != res3["node"].name
    )
    assert (
        res1["node"].web_id != res2["node"].web_id
        and res2["node"].web_id != res3["node"].web_id
        and res1["node"].web_id != res3["node"].web_id
    )
    assert (
        res1["node"].client_id != res2["node"].client_id
        and res2["node"].client_id != res3["node"].client_id
        and res1["node"].client_id != res3["node"].client_id
    )


async def test_create_asset_wrong_field(
    repo: Repository,
):
    create = CreateAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        _cast=make_input_object,
        # _make_id=make_id,
        target="node",
        webid="node668540fb5ac420d8fc35320a",
        child="node",
    )
    with pytest.raises(expected_exception=ValidationError):
        await create({"NoExistentKey": "foobar"})


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "asse668540fb5ac420d8fc35320a", "database"),
        ("database", "daba668540fb5ac420d8fc35320a", "node"),
        ("node", "node668540fb5ac420d8fc35320a", "node"),
        ("item", "item668540fb5ac420d8fc35320a", "item"),
    ],
)
async def test_create_asset_nok(
    target: str,
    webid: str,
    repo: Repository,
    child: str,
):
    create = CreateAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        _cast=make_input_object,
        target=target,
        webid=webid,
        child=child,
    )
    for obj in inputs["assetservers"]:
        with pytest.raises(expected_exception=ValidationError):
            await create(obj)


@pytest.mark.parametrize(
    "target, webid",
    [
        ("assetserver", "asse668540fb5ac420d8fc35320a"),
        ("database", "daba668540fb5ac420d8fc35320a"),
        ("keyword", "kewo668540fb5ac420d8fc35320a"),
        ("node", "node668540fb5ac420d8fc35320a"),
        ("item", "item668540fb5ac420d8fc35320a"),
    ],
)
async def test_readone_asset_ok(target: str, webid: str, repo: Repository):
    readone = ReadOneAsset(
        _repo=repo,
        _check_id=check_id,
        _split_fields=split_fields,
        target=target,
        webid=webid,
    )
    repo.reset_mock()  # type: ignore
    await readone()
    repo.read.assert_called_once()  # type: ignore


@pytest.mark.parametrize(
    "target, webid, child",
    [
        ("assetserver", "asse668540fb5ac420d8fc35320a", "database"),
        ("database", "daba668540fb5ac420d8fc35320a", "node"),
        ("node", "node668540fb5ac420d8fc35320a", "node"),
        ("item", "item668540fb5ac420d8fc35320a", "item"),
    ],
)
async def test_readmany_asset_ok(target: str, webid: str, repo: Repository, child: str):
    readmany = ReadManyAsset(
        _repo=repo,
        _check_id=check_id,
        _check_hierarchy=check_hierarchy,
        _split_fields=split_fields,
        target=target,
        webid=webid,
        child=child,
    )

    repo.reset_mock()  # type: ignore
    await readmany()
    repo.list.assert_called_once()  # type: ignore

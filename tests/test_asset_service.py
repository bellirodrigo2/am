""""""

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from am.asset import CreateAsset
from am.container import Factory
from am.interfaces import Repository
from am.schemas.webid import WebId
from tests.basenodetest import ByteRepVisitorTest, classes_map

###############################################################################


obj_file: Path = Path.cwd() / "tests/objs.json"
with open(file=obj_file) as f:
    inputs = json.load(fp=f)
    assert inputs is not None


factory = Factory(_classmap=classes_map)
visitor = ByteRepVisitorTest()


# testing TargetAsset
@pytest.fixture
def repo() -> Repository:
    return MagicMock()
    # mock_repo.get_one_by_webid.side_effect = oks.values()


# def setup_function():
# mock_repo.reset_mock(side_effect=True)


@pytest.mark.parametrize(
    "target, webid, child, objs",
    [
        (
            "BaseServer",
            WebId.make(input="serv668540fb5ac420d8fc35320a"),
            "BaseRoot",
            inputs["databases"],
        ),
        (
            "BaseRoot",
            WebId.make(input="root668540fb5ac420d8fc35320a"),
            "BaseElement",
            inputs["views"],
        ),
        (
            "BaseNode",
            WebId.make(input="node668540fb5ac420d8fc35320a"),
            "BaseNode",
            inputs["nodes"],
        ),
        (
            "BaseItem",
            WebId.make(input="item668540fb5ac420d8fc35320a"),
            "BaseItem",
            inputs["items"],
        ),
    ],
)
def test_parent_asset_ok(
    target: str,
    webid: WebId,
    repo: Repository,
    child: str,
    objs: Iterable[Mapping[str, Any]],
):
    create = CreateAsset(
        _repo=repo,
        _factory=factory,
        _target=target,
        _webid=webid,
        _child=child,
        _byterep=visitor,
    )
    for obj in objs:
        repo.reset_mock()  # type: ignore
        res: Mapping[str, Any] = create(obj)
        repo.create.assert_called_once()  # type: ignore
        assert "webid" in res

        obj_type = visitor.visit(factory.get(child))
        assert res["webid"].prefix == obj_type

    for obj in inputs["assetservers"]:
        with pytest.raises(expected_exception=ValidationError):
            create(obj)

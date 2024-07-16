""""""

import pytest

from am.exceptions import InvalidIdError
from am.schemas.id_.errors import InvalidId
from am.schemas.id_.objectid import ObjectId
from am.schemas.objrules import WebId, _cast_id, _make_new_id  # type: ignore

strid = "node668540fb5ac420d8fc35320a"
prefid = b"node"
binid = b"nodef\x85@\xfbZ\xc4 \xd8\xfc52\n"


def test_ok_from_4bytes_constructor() -> None:
    """Make webid from 4 bytes pref should be OK"""

    pref = b"node"
    webid: WebId = WebId(pref=pref, bid=None)

    assert webid.pref == pref


def test_ok_from_4bytes() -> None:
    """Make webid from 4 bytes pref should be OK"""

    pref = "node"
    webid: WebId = _make_new_id(target=pref)

    assert webid.pref == pref.encode("utf-8")


def test_ok_from_str() -> None:
    """Make webid from str pref should be OK"""

    input = "node668540fb5ac420d8fc35320a"
    webid: WebId = _cast_id(input)

    assert str(webid) == input


def test_bad_from_short_str() -> None:
    """Make webid from short str should be OK"""

    input = "node668540fb5ac"

    with pytest.raises(expected_exception=Exception):
        _cast_id(input)


def test_bad_from_long_str() -> None:
    """Make webid from long str should be OK"""

    input = "node668540fb5ac420d8fc35320aFOOBAR"

    with pytest.raises(expected_exception=Exception):
        _cast_id(input)


def test_bad_from_15bytes() -> None:
    """Make webid from 15 bytes should not be OK"""

    input: bytes = b"node" + b"12345678901"

    with pytest.raises(expected_exception=InvalidIdError):
        _cast_id(str(input))


def test_bad_from_17bytes() -> None:
    """Make webid from 17 bytes should not be OK"""

    input: bytes = b"node" + b"1234567890123"

    with pytest.raises(expected_exception=InvalidIdError):
        _cast_id(str(input))

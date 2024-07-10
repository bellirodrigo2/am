""""""

import pytest

from am.schemas.id_.objectid import ObjectId
from am.schemas.webid import WebId

strid = "node668540fb5ac420d8fc35320a"
prefid = b"node"
binid = b"nodef\x85@\xfbZ\xc4 \xd8\xfc52\n"


def test_ok_from_4bytes() -> None:
    """Make webid from 4 bytes pref should be OK"""

    pref = b"node"
    webid: WebId = WebId.make(input=pref)

    assert webid.prefix == pref


def test_ok_from_16bytes() -> None:
    """Make webid from 16 bytes (pref+ObjectId) pref should be OK"""

    input: bytes = b"node" + ObjectId().binary
    webid: WebId = WebId.make(input=input)

    assert bytes(webid) == input


def test_ok_from_str() -> None:
    """Make webid from str pref should be OK"""

    input = "node668540fb5ac420d8fc35320a"
    webid: WebId = WebId.make(input=input)

    assert str(webid) == input


def test_bad_from_short_str() -> None:
    """Make webid from short str should be OK"""

    input = "node668540fb5ac"

    with pytest.raises(expected_exception=Exception):
        WebId.make(input=input)


def test_bad_from_long_str() -> None:
    """Make webid from long str should be OK"""

    input = "node668540fb5ac420d8fc35320aFOOBAR"

    with pytest.raises(expected_exception=Exception):
        WebId.make(input=input)


def test_bad_from_15bytes() -> None:
    """Make webid from 15 bytes should not be OK"""

    input: bytes = b"node" + b"12345678901"

    with pytest.raises(expected_exception=Exception):
        WebId.make(input=input)


def test_bad_from_17bytes() -> None:
    """Make webid from 17 bytes should not be OK"""

    input: bytes = b"node" + b"1234567890123"

    with pytest.raises(expected_exception=Exception):
        WebId.make(input=input)


def test_bad_from_no_byte_or_str_input() -> None:
    """Make webid from a non bytes/str input should not be OK"""

    input = 4

    with pytest.raises(expected_exception=Exception):
        WebId.make(input=input)  # type: ignore

""""""

import pytest
from pydantic import ValidationError

from am.exceptions import InvalidIdError
from am.interfaces import IdInterface
from am.schemas.objrules import WebId, _cast_id, _make_new_id  # type: ignore


def test_ok_from_4bytes_constructor() -> None:
    """Make webid from 4 bytes pref should be OK"""

    pref = b"node"
    webid: IdInterface = WebId(pref=pref)

    assert webid.pref == pref


def test_ok_from_4bytes() -> None:
    """Make webid from 4 bytes pref should be OK"""

    pref = "node"
    webid: IdInterface = _make_new_id(target=pref)

    assert webid.pref == pref.encode("utf-8")


def test_ok_from_str() -> None:
    """Make webid from str pref should be OK"""

    input = "node668540fb5ac420d8fc35320a"
    webid: IdInterface = _cast_id(input)

    assert str(webid) == input


def test_bad_prefix_str() -> None:
    """Make webid from str"""

    pref = b"noke"

    with pytest.raises(expected_exception=InvalidIdError):
        WebId(pref=pref)


def test_bad_space_str() -> None:
    """Make webid from str"""

    input = "node668540f 5ac420d8fc35320a"

    with pytest.raises(expected_exception=InvalidIdError):
        _cast_id(input)


def test_bad_special_str() -> None:
    """Make webid from str"""

    input = "node668540f?5ac420d8fc35320a"

    with pytest.raises(expected_exception=InvalidIdError):
        _cast_id(input)


def test_bad_from_short_str() -> None:
    """Make webid from short str should be OK"""

    input = "node668540fb5ac"

    with pytest.raises(expected_exception=ValidationError):
        _cast_id(input)


def test_bad_from_long_str() -> None:
    """Make webid from long str should be OK"""

    input = "node668540fb5ac420d8fc35320aFOOBAR"

    with pytest.raises(expected_exception=ValidationError):
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

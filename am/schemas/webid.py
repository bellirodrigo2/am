from dataclasses import dataclass
from typing import Self

from am.schemas.id_.objectid import ObjectId


def webid_from_str(id: str) -> tuple[bytes, ObjectId]:
    pref = id[:4].encode("utf-8")
    bid = ObjectId(id[4:])
    return pref, bid


def webid_from_bytes(id: bytes) -> tuple[bytes, ObjectId]:
    binarylen = len(id)
    if binarylen == 16:
        pref = id[:4]
        bid = ObjectId(id[4:])
    elif binarylen == 4:
        pref = id
        bid = ObjectId()
    else:
        raise Exception()
    return pref, bid


@dataclass(frozen=True)
class WebId:
    _pref: bytes
    _bid: ObjectId

    @classmethod
    def make(cls, input: bytes | str) -> Self:
        if isinstance(input, bytes):
            pref, bid = webid_from_bytes(input)
        elif isinstance(input, str):  # type: ignore
            pref, bid = webid_from_str(input)
        else:
            raise Exception(f"Input type is not valid {type(input)=}")
        return cls(pref, bid)

    def __str__(self) -> str:
        return self._pref.decode(encoding="utf8") + str(self._bid)

    def __bytes__(self) -> bytes:
        return self._pref + self._bid.binary

    @property
    def prefix(self) -> bytes:
        return self._pref


if __name__ == "__main__":
    ...

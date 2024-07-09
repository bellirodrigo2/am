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
    def make(cls, pref: bytes) -> Self:
        binarylen = len(pref)
        if binarylen == 16:
            pref = pref[:4]
            bid = ObjectId(pref[4:])
        elif binarylen == 4:
            bid = ObjectId()
        else:
            raise Exception()
        return cls(pref, bid)

    def __str__(self) -> str:
        return self._pref.decode("utf8") + str(self._bid)

    def __bytes__(self) -> bytes:
        return self._pref + self._bid.binary

    @property
    def prefix(self) -> bytes:
        return self._pref


if __name__ == "__main__":

    strid = "node668540fb5ac420d8fc35320a"
    prefid = b"node"
    binid = b"nodef\x85@\xfbZ\xc4 \xd8\xfc52\n"

    # web_str = WebId(strid)
    # assert str(web_str) == strid
    # assert bytes(web_str) == binid
    # # assert web_str.validat_pref("node")
    # # assert web_str.validat_pref(b"node")

    # web_pref = WebId(prefid)
    # # assert str(web_pref) == strid
    # # assert bytes(web_pref) == binid
    # # assert web_pref.validat_pref("node")
    # # assert web_pref.validat_pref(b"node")

    # web_bin = WebId(binid)
    # assert str(web_bin) == strid
    # assert bytes(web_bin) == binid
    # # assert web_bin.validat_pref("node")
    # # assert web_bin.validat_pref(b"node")

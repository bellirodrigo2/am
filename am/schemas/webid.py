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


class WebId:

    def __init__(self, id: str | bytes) -> None:

        if isinstance(id, str):
            pref, bid = webid_from_str(id)
        elif isinstance(id, bytes):
            pref, bid = webid_from_bytes(id)
        self.__pref = pref
        self.__bid = bid

    def __str__(self) -> str:
        return self.__pref.decode("utf8") + str(self.__bid)

    def __bytes__(self) -> bytes:
        return self.__pref + self.__bid.binary

    @property
    def prefix(self):
        return self.__pref


if __name__ == "__main__":

    strid = "node668540fb5ac420d8fc35320a"
    prefid = b"node"
    binid = b"nodef\x85@\xfbZ\xc4 \xd8\xfc52\n"

    web_str = WebId(strid)
    assert str(web_str) == strid
    assert bytes(web_str) == binid
    assert web_str.validat_pref("node")
    assert web_str.validat_pref(b"node")

    web_pref = WebId(prefid)
    # assert str(web_pref) == strid
    # assert bytes(web_pref) == binid
    assert web_pref.validat_pref("node")
    assert web_pref.validat_pref(b"node")

    web_bin = WebId(binid)
    assert str(web_bin) == strid
    assert bytes(web_bin) == binid
    assert web_bin.validat_pref("node")
    assert web_bin.validat_pref(b"node")

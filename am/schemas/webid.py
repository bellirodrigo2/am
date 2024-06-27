"""Cahier Object WebId type."""

# from typing import Annotated
from uuid import UUID, uuid1

# from am.schemas.id_.objectid import ObjectId

# from pydantic import ValidationError


###############################################################################

WebId = UUID


def make_webid() -> WebId:
    return uuid1()


def webid_from_string(webid: str) -> WebId:
    return UUID(webid, version=1)


# class hasWebId:
#     web_id: Annotated[
#         WebId,
#         Field(
#             alias="WebId",
#             serialization_alias="WebId",
#             frozen=True,
#             default_factory=make_webid,
#         ),
#     ]
if __name__ == "__main__":

    print("ok")
    # id1 = ObjectId()
    # id2 = ObjectId()

    # print(id1)
    # sid = str(id1)
    # print(len(str.encode(sid)))
    # print(len(bytes.fromhex(sid)))

"""Cahier Object WebId type."""

# from typing import Annotated
from uuid import UUID, uuid1

from cahier.schemas.id_.objectid import ObjectId

# from pydantic import Field


###############################################################################

WebId = UUID


def make_webid() -> WebId:
    return uuid1()


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
    id1 = ObjectId()
    id2 = ObjectId()

    print(id1)
    sid = str(id1)
    print(len(str.encode(sid)))
    print(len(bytes.fromhex(sid)))

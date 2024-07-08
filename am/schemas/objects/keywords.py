""" Asset Keywords Object """

from pydantic import Field

from am.schemas.basenode import BaseServer

###############################################################################


class Keywords(BaseServer):
    @classmethod
    def byte_rep(cls) -> bytes:
        return b"kewo"

    keywords: list[str] = Field()

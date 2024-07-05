""" Database Object """

from pydantic import Field

from am.schemas.baseobjs import BaseRoot

###############################################################################


class DataBase(BaseRoot):
    @classmethod
    def byte_rep(cls) -> bytes:
        return b"dbas"

    host: str = Field()

""" Database Object """

from pydantic import Field

from am.schemas.basenode import BaseRoot

###############################################################################


class DataBase(BaseRoot):
    # @classmethod
    # def byte_rep(cls) -> bytes:
    # return b"dbas"

    host: str = Field()

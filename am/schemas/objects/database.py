""" Database Object """

from pydantic import Field

from am.schemas.baseclass import BaseRoot


class DataBase(BaseRoot):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"daba"

    host: str = Field()

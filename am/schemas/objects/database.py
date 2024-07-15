""" Database Object """

from typing import Iterable

from pydantic import Field

from am.schemas.baseclass import BaseRoot


class DataBase(BaseRoot):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"daba"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["assetserver"]

    host: str = Field()

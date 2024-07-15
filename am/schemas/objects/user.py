""" User Object """

from typing import Iterable

from pydantic import Field

from am.schemas.baseclass import BaseRoot


class User(BaseRoot):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"user"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["assetserver"]

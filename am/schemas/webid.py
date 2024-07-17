from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from am.exceptions import InvalidIdError
from am.schemas.id_.errors import InvalidId
from am.schemas.id_.objectid import ObjectId


class Id(BaseModel, ABC):

    @classmethod
    @abstractmethod
    def _pref_options(cls) -> Iterable[bytes]: ...

    pref: bytes = Field(min_length=4, max_length=4, frozen=True)
    bid: str = Field(
        min_length=24, max_length=24, default_factory=ObjectId, frozen=True
    )

    @field_validator("pref")
    @classmethod
    def prefix_validator(cls, v: bytes) -> bytes:
        if v not in cls._pref_options():
            raise InvalidIdError(f"{v!r} not in {cls._pref_options()}")
        return v

    @field_validator("bid")
    @classmethod
    def bid_validator(cls, v: str) -> str:
        try:
            ObjectId(v)
        except InvalidId:
            raise InvalidIdError(f"{v} if not a valid bid")
        return v

    def __str__(self) -> str:
        return self.pref.decode(encoding="utf8") + str(self.bid)

    def __bytes__(self) -> bytes:
        return self.pref + self.bid.encode("utf-8")  # type: ignore

    def pref_as_int(self, byteorder: Literal["little", "big"] = "little") -> int:
        return int.from_bytes(self.pref, byteorder=byteorder)

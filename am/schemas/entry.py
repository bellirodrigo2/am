from abc import ABC, abstractmethod
from collections.abc import Iterable

from pydantic import BaseModel, ValidationInfo, field_validator

from am.exceptions import InvalidIdError, InvalidTargetError
from am.schemas.id_.errors import InvalidId
from am.schemas.id_.objectid import ObjectId


def make_id() -> str:
    return str(ObjectId())


class Entry(BaseModel, ABC):

    target: str
    webid: str
    child: str | None = None

    @classmethod
    @abstractmethod
    def _options(cls) -> Iterable[str]: ...

    @classmethod
    @abstractmethod
    def _parents(cls, child: str) -> Iterable[str]: ...

    @field_validator("target")
    @classmethod
    def target_validator(cls, v: str) -> str:
        if v not in cls._options():
            raise InvalidTargetError(f"Target {v!r} not in {cls._options()}")
        return v

    @field_validator("webid")
    @classmethod
    def webid_validator(cls, v: str) -> str:

        try:
            ObjectId(v)
        except InvalidId:
            raise InvalidIdError(id=v)
        return v

    @field_validator("child")
    @classmethod
    def child_validator(cls, v: str | None, info: ValidationInfo) -> str | None:

        if not v:
            return v
        if v not in cls._options():
            raise InvalidTargetError(f"Child {v} not in {cls._options()}")

        target = info.data["target"]
        parents = cls._parents(v)
        if target not in parents:
            raise InvalidTargetError(f"Target {target} can not be a parent of {v}")

        return v

from collections.abc import Iterable

from am.schemas.baseclass import BaseElement


class EnumSet(BaseElement):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"enum"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["database"]

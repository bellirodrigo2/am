""" Metadata Object """

from collections.abc import Iterable

from am.schemas.baseclass import BaseElement


class Metadata(BaseElement):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"cole"

    @classmethod
    def parent_constr(cls) -> Iterable[str] | None:
        return ["database", "user"]

from collections.abc import Iterable

from am.interfaces import (
    IdInterface,
    JsonObj,
    ReadAllOptionsInterface,
    VisitableInterface,
)


class SQLRepository:

    def create(self, obj: VisitableInterface, id: IdInterface) -> None: ...

    def read(self, *fields: str) -> JsonObj: ...

    def list(self, options: ReadAllOptionsInterface | None) -> Iterable[JsonObj]: ...

    def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj: ...

    def delete(self) -> JsonObj: ...

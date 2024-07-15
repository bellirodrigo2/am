""" Asset Manager Interfaces"""

from collections.abc import Iterable, Mapping
from enum import Enum
from typing import Any, Protocol, Self


class IdInterface(Protocol):

    @classmethod
    def make(cls, input: bytes | str) -> Self: ...

    @property
    def prefix(self) -> bytes: ...

    def __str__(self) -> str: ...

    def __bytes__(self) -> bytes: ...


JsonObj = Mapping[str, Any]


class VisitableInterface(Protocol):

    @property
    def visitor_rep(self) -> str: ...

    def accept(self, visitor: Any) -> None: ...


class VisitorInterface(Protocol):
    def visit(self, element: VisitableInterface) -> Any: ...  # type: ignore


class ObjectsRules(Protocol):
    def make_id(self, target: str) -> IdInterface: ...
    def make_node(self, target: str, **kwargs: Any) -> VisitableInterface: ...
    def check_hierarchy(self, target: str, child: str) -> None: ...
    def check_id(self, target: str, id: IdInterface) -> None: ...
    def get_fields(self, target: str) -> tuple[str, ...]: ...


# class _Getter(Protocol):
# def get(self, target: str) -> Any: ...


class _Maker(Protocol):
    def make(self, target: str, **kwargs: Any) -> Any: ...


class _Checker(Protocol):
    def check(self, target: str, against: Any) -> None: ...


class IdHandlerInterface(_Maker, _Checker, Protocol): ...


# class ObjectHandler(_Maker, _Getter, Protocol): ...


class SortOrder(Enum):
    Asc = "asc"
    Desc = "desc"


start = int
max = int
field = str


class ReadAllOptionsInterface(Protocol):

    field_filter: Mapping[field, str] | None
    field_filter_like: Mapping[field, str] | None
    search_full_hierarchy: bool
    sort_options: tuple[tuple[field, SortOrder], ...] | None
    pag_options: tuple[start, max] | None
    selected_fields: tuple[field, ...]


class CreateAssetInterface(Protocol):
    def __call__(self, inpobj: JsonObj) -> JsonObj: ...


class UpdateAssetInterface(Protocol):
    def __call__(self, updobj: JsonObj) -> JsonObj: ...


class ReadOneAssetInterface(Protocol):
    def __call__(self, *fields: str) -> JsonObj: ...


class ReadManyAssetInterface(Protocol):
    def __call__(self, sel_fields: ReadAllOptionsInterface | None) -> JsonObj: ...


class DeleteAssetInterface(Protocol):
    def __call__(self) -> JsonObj:
        ...

        # ficou boa a aula a partir das 9:12 pm
        # O OUTPUT TEM QUE SER UM READONLY... MAPPED OBJECT... E NAO UMA ENTITY
        # DESCRIçÂO D
        # OS TESTES?/// DEVE CRIAR UMA CONTA COMO......

        # ASSISTIR AS 21:30.... sobre repository x database
        # OUVIR 21:58 sobre dao x repository
        # join dentro do repositpry


###############################################################################


class Repository(Protocol):

    def create(self, obj: VisitableInterface, id: IdInterface) -> None: ...

    def read(self, *fields: str) -> JsonObj: ...

    def list(self, options: ReadAllOptionsInterface | None) -> Iterable[JsonObj]: ...

    def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj: ...

    def delete(self) -> JsonObj: ...


if __name__ == "__main__":
    ...

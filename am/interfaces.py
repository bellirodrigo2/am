""" Asset Manager Interfaces"""

from collections.abc import Container, Iterable, Mapping
from enum import Enum
from typing import Any, Callable, Protocol, Self


class IdInterface(Protocol):

    @classmethod
    def make(cls, pref: bytes) -> Self: ...

    prefix: bytes

    def __str__(self) -> str: ...

    def __bytes__(self) -> bytes: ...


class LabelInterface(Protocol):

    name: str
    description: str
    client_id: str


class ObjInterface(Protocol):

    @classmethod
    def base_type(cls) -> str: ...

    @classmethod
    def children(cls) -> Container[str]: ...

    @classmethod
    def byte_rep(cls) -> bytes: ...

    @classmethod
    def is_tree(cls) -> bool: ...

    @classmethod
    def get_fields(cls) -> Mapping[str, type | None]: ...


ObjClassInterface = type[ObjInterface]

ObjFactoryInterface2 = Callable[[str], ObjClassInterface]


class SortOrder(Enum):
    Asc = "asc"
    Desc = "desc"


class ReadAllOptions(Protocol):

    field_filter: Mapping[str, str] | None
    field_filter_like: Mapping[str, str] | None
    search_full_hierarchy: bool | None
    sort_field: str | None
    sort_order: SortOrder | None
    start_index: int | None
    max_count: int | None
    selected_fields: Iterable[str] | None


JsonObj = Mapping[str, Any]

###############################################################################


class CreateAssetInterface(Protocol):
    def __call__(self, inpobj: JsonObj) -> JsonObj: ...


class UpdateAssetInterface(Protocol):
    def __call__(self, updobj: JsonObj) -> JsonObj: ...


class ReadOneAssetInterface(Protocol):
    def __call__(self, *fields: str) -> JsonObj: ...


class ReadmanyAssetInterface(Protocol):
    def __call__(self, sel_fields: ReadAllOptions | None) -> JsonObj: ...


class DeleteAssetInterface(Protocol):
    def __call__(self) -> JsonObj:
        ...

        # ficou boa a aula a partir das 9:12 pm
        # O OUTPUT TEM QUE SER UM READONLY... MAPPED OBJECT... E NAO UMA ENTITY
        # DESCRIçÂO DOS TESTES?/// DEVE CRIAR UMA CONTA COMO......

        # ASSISTIR AS 21:30.... sobre repository x database
        # OUVIR 21:58 sobre dao x repository
        # join dentro do repositpry


###############################################################################


class Repository(Protocol):

    def create(
        self, base: JsonObj, obj: JsonObj, id: IdInterface, istree: bool
    ) -> None: ...

    def read(self, *fields: str) -> JsonObj: ...

    def list(self, options: ReadAllOptions | None) -> Iterable[JsonObj]: ...

    def update(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj: ...

    def delete(self) -> JsonObj: ...


if __name__ == "__main__":
    ...

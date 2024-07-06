""" Asset Manager Interfaces"""

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
    def children(cls) -> list[str]: ...

    @classmethod
    def byte_rep(cls) -> bytes: ...

    @classmethod
    def is_tree(cls) -> bool: ...

    @classmethod
    def get_fields(cls) -> dict[str, type | None]: ...


ObjClassInterface = type[ObjInterface]

ObjFactoryInterface2 = Callable[[str], ObjClassInterface]


class SortOrder(Enum):
    Asc = "asc"
    Desc = "desc"


class ReadAllOptions(Protocol):

    field_filter: dict[str, str] | None
    field_filter_like: dict[str, str] | None
    search_full_hierarchy: bool | None
    sort_field: str | None
    sort_order: SortOrder | None
    start_index: int | None
    max_count: int | None
    selected_fields: tuple[str, ...] | None


JsonObj = dict[str, Any]

###############################################################################


class CreateAssetInterface(Protocol):
    def __call__(self, inpobj: JsonObj) -> JsonObj: ...


class UpdateAssetInterface(Protocol):
    def __call__(self, updobj: JsonObj) -> JsonObj: ...


class ReadOneAssetInterface(Protocol):
    def __call__(self, sel_fields: tuple[str, ...]) -> JsonObj: ...


class ReadmanyAssetInterface(Protocol):
    def __call__(self, sel_fields: ReadAllOptions) -> JsonObj: ...


class DeleteAssetInterface(Protocol):
    def __call__(self) -> JsonObj:
        ...

        # ficou boa a aula a partir das 9:12 pm
        # O OUTPUT TEM QUE SER UM READONLY.... MAPPED OBJECT... E NAO UMA ENTITY
        # DESCRIçÂO DOS TESTES?/// DEVE CRIAR UMA CONTA COMO......

        # ASSISTIR AS 21:30.... sobre repository x database
        # OUVIR 21:58 sobre dao x repository
        # join dentro do repositpry


###############################################################################


class CreateRepository(Protocol):
    def __call__(self, base: JsonObj, obj: JsonObj) -> None: ...


class ReadRepository(Protocol):
    def __call__(self, selected_fields: tuple[str, ...] | None) -> JsonObj: ...


class ListRepository(Protocol):
    def __call__(self, options: ReadAllOptions | None) -> tuple[JsonObj, ...]: ...


class UpdateRepository(Protocol):
    def __call__(self, base: JsonObj, obj_spec: JsonObj) -> JsonObj: ...


class DeleteRepository(Protocol):
    def __call__(self) -> JsonObj: ...


if __name__ == "__main__":
    ...

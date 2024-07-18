""" Asset Manager Interfaces"""

from collections.abc import Iterable, Mapping, MutableMapping
from enum import Enum
from typing import Any, Literal, Protocol

JsonObj = Mapping[str, Any]


class VisitableInterface(Protocol):

    @property
    def visitor_rep(self) -> str: ...

    def accept(self, visitor: Any) -> None: ...


class VisitorInterface(Protocol):
    def visit(self, element: VisitableInterface) -> Any: ...  # type: ignore


class IdInterface(Protocol):

    @property
    def pref(self) -> bytes: ...
    @property
    def bid(self) -> str: ...

    def __str__(self) -> str: ...
    def __bytes__(self) -> bytes: ...
    def pref_as_int(self, byteorder: Literal["little", "big"]) -> int: ...


class TreeNodeInterface(VisitableInterface, Protocol):

    @property
    def web_id(self) -> IdInterface: ...

    def model_dump(self) -> MutableMapping[str, Any]: ...

    @classmethod
    def get_fields(cls) -> Iterable[str]: ...


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
    async def __call__(self, inpobj: JsonObj) -> JsonObj: ...


class UpdateAssetInterface(Protocol):
    async def __call__(self, updobj: JsonObj) -> JsonObj: ...


class ReadOneAssetInterface(Protocol):
    async def __call__(self, *fields: str) -> JsonObj: ...


class ReadManyAssetInterface(Protocol):
    async def __call__(self, sel_fields: ReadAllOptionsInterface | None) -> JsonObj: ...


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

    async def create(
        self,
        obj: TreeNodeInterface,
        parent: IdInterface,
    ) -> None: ...

    async def read(self, target_id: IdInterface, *fields: str) -> JsonObj: ...

    # async def list(
    #     self, options: ReadAllOptionsInterface | None
    # ) -> Iterable[JsonObj]: ...

    # async def update(self, **fields: Any) -> JsonObj: ...

    # async def delete(self) -> JsonObj: ...


if __name__ == "__main__":
    ...

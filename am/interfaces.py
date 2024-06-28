""" Asset Manager Interfaces"""

from enum import Enum
from typing import Any, Protocol

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from am.schemas.schemas import InputObj, Obj, ObjEnum, WebId

###############################################################################


class SortOrder(Enum):
    Asc = "asc"
    Desc = "desc"


class ReadAllOptions(BaseModel):
    """"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            alias=to_camel, validation_alias=to_camel, serialization_alias=to_camel
        ),
        populate_by_name=True,
        use_enum_values=True,
        frozen=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    field_filter: tuple[str, ...] | None = Field(default=None)
    field_filter_like: tuple[str, ...] | None = Field(default=None)
    search_full_hierarchy: bool | None = Field(default=None)
    sort_field: str | None = Field(default=None)
    sort_order: SortOrder | None = Field(default=None)
    start_index: int | None = Field(default=None)
    max_count: int | None = Field(default=None)
    selected_fields: tuple[str, ...] | None = Field(default=None)


JsonReponse = dict[str, Any]

###############################################################################


class AssetInterface(Protocol):

    def read(
        self,
        webid: WebId | str,
        target: ObjEnum,
        selected_fields: tuple[str, ...] | None = None,
    ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        webid: WebId | str,
        parent: ObjEnum,
        children: ObjEnum,
        options: ReadAllOptions | None,
    ) -> tuple[JsonReponse, ...]:
        """"""
        pass

    def create(
        self, webid: WebId | str, parent: ObjEnum, children: ObjEnum, inputobj: InputObj
    ) -> WebId:
        """"""
        pass


###############################################################################


class AssetDAOInterface(Protocol):

    def read(self, webid: WebId | str) -> Obj:
        """"""
        pass

    def list(self, webid: WebId | str, children: ObjEnum) -> tuple[Obj, ...]:
        """"""
        pass

    def create(self, webid: WebId | str, obj_type: ObjEnum, obj: Obj) -> WebId:
        """"""
        pass


if __name__ == "__main__":
    pass

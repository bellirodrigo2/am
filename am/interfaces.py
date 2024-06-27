""" Asset Manager Interfaces"""

from enum import Enum
from typing import Any, Protocol

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from am.schemas.schemas import InputObj, Obj, ObjEnum, WebId

################################################################################


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

################################################################################


class AssetInterface(Protocol):

    def read(
        self, target: ObjEnum, webid: WebId, selected_fields: tuple[str] | None = None
    ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> tuple[JsonReponse]:
        """"""
        pass

    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: InputObj
    ) -> WebId:
        """"""
        pass


################################################################################


class AssetDAOInterface(Protocol):

    def read(
        self, webid: WebId, selected_fields: tuple[str] | None = None
    ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> tuple[JsonReponse]:
        """"""
        pass

    def create(self, webid: WebId, obj: Obj) -> WebId:
        """"""
        pass


if __name__ == "__main__":
    pass

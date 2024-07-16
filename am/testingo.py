from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class _ParentConstraint:
    assetserver: str
    dataserver: int
    database: str
    user: bool

    def get(self, target: str) -> Any:
        return getattr(self, target)


p = _ParentConstraint(assetserver="foo", dataserver=4, database="bar", user=True)
print(p.get("user"))
# print(p.get("noKey"))
vals = [getattr(p, s) for s in p.__slots__]
print(vals)
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
for s in p.__slots__:
    print(s)

# class Base(DeclarativeBase): ...


# def byte_rep(b: bytes) -> int:
#     return int.from_bytes(b, byteorder="little")


# class Label(Base):
#     __tablename__ = "label"

#     name: Mapped[str] = mapped_column(primary_key=True)
#     type: Mapped[int]


# print(type(Label))
# print(b"node".decode("utf-8"))
# print(b"item".decode("utf-8"))
# print(b"daba".decode("utf-8"))
# print(b"asse".decode("utf-8"))
# print(b"teno".decode("utf-8"))

# from dataclasses import dataclass


# @dataclass(frozen=True, slots=True)
# class GetClass:
#     assetserver: type = int
#     dataserver: type = str

#     def __get__(self, instance, owner) -> None:  # type: ignore
#         print(instance, owner)  # type: ignore


# class Teste:
#     getcls_asset_server = GetClass()


# g = Teste()
# g.getclass

# from typing import Any, get_args, get_origin

# from pydantic import AnyUrl, BaseModel, ConfigDict, Field
# from pydantic.fields import FieldInfo


# class First(BaseModel):

#     # model_config = ConfigDict(extra="forbid")

#     arg: str | None = None


# class Teste(BaseModel):
#     name: str | None = Field(default="RBELL")
#     age: int = Field(default=4)
#     vis: First = Field(default_factory=First)
#     arg: AnyUrl


# def get_field(info: type[Any]) -> tuple[type, bool]:
#     args = get_args(info)
#     lenargs = len(args)
#     if lenargs == 0:
#         return (info, False)
#     if lenargs == 2:
#         if args[0] == type(None):
#             return (args[1], True)
#         if args[1] == type(None):
#             return (args[0], True)
#     raise Exception(f"Type {type(info)} does not follow the required format")


# # for name, field in Teste.model_fields.items():
# #     print(name, get_field(field.annotation))  # type: ignore


# class Second(First):
#     arg2: str


# f = Second(arg="foobar", arg2="whatelse", arg3="foobae")

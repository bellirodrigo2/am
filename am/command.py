from collections.abc import Awaitable, Hashable, Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol, get_args, get_origin


class Method(Enum):

    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()
    HEAD = auto()
    OPTIONS = auto()
    TRACE = auto()
    CONNECT = auto()


class Command(Protocol):

    method: Method
    host: str  # URL
    path: Hashable
    query_param: Iterable[tuple[str, str]]
    header: Mapping[str, Any]
    body: Mapping[str, Any]

    async def do(self) -> Awaitable[Any]: ...
    async def undo(self) -> Awaitable[Any]: ...


@dataclass(frozen=True)
class one:
    a: str = field(default="foo")
    b: type = field(default=int)


@dataclass(frozen=True)
class two:
    a: str = field(default="bar")
    b: type = field(default=str)


@dataclass(frozen=True)
class three:
    a: str = field(default="foo")
    b: type = field(default=int)


class mt: ...


m = mt()
o = one()
tw = two()
th = three()


print("m ", hash(m))
print("o", hash(o))
print("tw", hash(tw))
print("th", hash(th))


assert hash(th) == hash(o)
assert hash(("foo", int)) == hash(o)
print(tuple(vars(o).values()))

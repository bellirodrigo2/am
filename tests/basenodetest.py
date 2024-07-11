from collections.abc import Container
from dataclasses import dataclass

from pydantic import AnyUrl, BaseModel

from am.schemas.mapclass import make_map
from am.visitor import GetByteRep, Visitable, Visitor


@dataclass(frozen=True, slots=True)
class ByteRepVisitorTest(Visitor):
    label: GetByteRep = lambda x: b"labe"
    baseserver: GetByteRep = lambda x: b"serv"
    baseroot: GetByteRep = lambda x: b"root"
    baseelement: GetByteRep = lambda x: b"elem"
    basenode: GetByteRep = lambda x: b"node"
    baseitem: GetByteRep = lambda x: b"item"


class Label(BaseModel, Visitable):
    name: str
    client_id: str
    description: str

    @classmethod
    def base_type(cls) -> str:
        return "label"

    @classmethod
    def children(cls) -> Container[str]:
        return []


class BaseServer(Label):

    source_url: AnyUrl

    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "serverelement", "root"]


class BaseRoot(Label):

    host: str

    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def children(cls) -> Container[str]:
        return ["element", "rootelement", "node"]


class BaseElement(Label):

    view_str: str
    proc_str: str

    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def children(cls) -> Container[str]:
        return []


class BaseNode(Label):

    template: str

    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def children(cls) -> Container[str]:
        return ["node", "item", "element", "nodeelement", "treeelement"]


class BaseItem(Label):

    type: str

    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def children(cls) -> Container[str]:
        return ["item", "element", "itemelement", "treeelement"]


classes_map = make_map(Label)

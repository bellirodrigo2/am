""" In Memory DAO """

from collections import namedtuple
from typing import Callable

from treelib import Node, Tree

from am.schemas.schemas import Obj, ObjEnum, WebId

###############################################################################

DataNode = namedtuple("DataNode", ["objtype", "obj"])


class InMemoryDAO:
    def __init__(self, get_db: Callable[[], Tree]) -> None:
        self.get_db = get_db

    def read(self, webid: WebId | str) -> Obj:
        """"""
        tree = self.get_db()
        node: Node | None = tree.get_node(webid)
        if node:
            return node.data.obj
        raise Exception()

    def list(self, webid: WebId | str, children: ObjEnum) -> tuple[Obj, ...]:
        """"""
        tree = self.get_db()
        treenodes: list[Node] | None = tree.children(webid)
        if treenodes is None:
            raise Exception()
        nodes = [node.data for node in treenodes]
        return tuple([data.obj for data in nodes if data.objtype == children])

    def create(self, webid: WebId | str, obj_type: ObjEnum, obj: Obj) -> WebId:
        """"""

        tree = self.get_db()
        tree.create_node(
            tag=obj.name,
            identifier=obj.webid,
            parent=webid,
            data=DataNode(objtype=obj_type, obj=obj),
        )
        return obj.webid

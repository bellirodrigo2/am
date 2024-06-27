""" In Memory DAO """

from typing import Callable

from treelib import Tree

from cahier.interfaces.assetdao import ReadAllOptions, JsonReponse
from cahier.schemas.schemas import InputObj, Obj, ObjEnum, WebId

################################################################################

def filter_children(node , children: ObjEnum):
    
    objs_list: list[Obj] = [n.data for n in node.children]
    return [o for o in objs_list if o.cls_name() == children.name]

class InMemoryDAO:

    def __init__(self, get_db: Callable[[], Tree]) -> None:
        self.get_db = get_db
    def read(self, 
            webid: WebId, 
            selected_fields: tuple[str] | None = None
            ) -> JsonReponse:
        """"""
        
        tree = self.get_db()
        print('****************************', tree)
        
        node = tree.get_node(webid)
        if node:
            return node.data
        raise Exception()

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> list[JsonReponse] | JsonReponse:
        """"""
        
        tree = self.get_db()
        node = tree.get_node(webid)
        if node:
            return filter_children(node, children)  # ... filtrar os types de children
        raise Exception()

    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: InputObj
    ) -> None:
        """"""

        tree = self.get_db()
        obj_ = Obj(obj)
        tree.create_node(tag=obj_.name, identifier=obj_.webid, data=obj_)

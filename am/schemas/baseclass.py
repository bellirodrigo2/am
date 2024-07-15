from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(Label, Visitable): ...


#     @classmethod
#     @abstractmethod
#     def base_type(cls) -> str: ...

#     @classmethod
#     @abstractmethod
#     def children(cls) -> Container[str]: ...

#     @classmethod
#     @abstractmethod
#     def byte_rep(cls) -> bytes: ...

#     @classmethod
#     def parent_constr(cls) -> Iterable[str] | None:
#         return None


# class BaseServer(BaseClass):

#     @classmethod
#     def base_type(cls) -> str:
#         return "server"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return ["element", "root"]


# class BaseRoot(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "root"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return ["element", "basenode"]


# class BaseElement(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "element"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return ["elementfield"]


# class BaseNode(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "basenode"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return ["basenode", "baseitem", "element"]


# class BaseItem(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "baseitem"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return ["baseitem", "element"]


# class ElementField(BaseClass):
#     @classmethod
#     def base_type(cls) -> str:
#         return "elementfield"

#     @classmethod
#     def children(cls) -> Container[str]:
#         return []


# # class Strict(BaseClass):
# #     @classmethod
# #     def base_type(cls) -> str:
# #         return "strict"

# #     @classmethod
# #     def children(cls) -> Container[str]:
# #         return []

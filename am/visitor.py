from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from am.interfaces import VisitableInterface, VisitorInterface


class Visitable:

    @property
    def visitor_rep(self) -> str:
        return self.__class__.__name__.lower()

    def accept(self, visitor: VisitorInterface) -> None:

        visitor.visit(self)


@dataclass(frozen=True, slots=True)
class VisitableString(Visitable):
    key: str

    @property
    def visitor_rep(self) -> str:
        return self.key


class NonImplementedVisitMethod(Exception): ...


class Visitor:

    def visit(self, element: VisitableInterface) -> Any:

        rep = element.visitor_rep
        try:
            fn = getattr(self, rep)
        except AttributeError:
            raise NonImplementedVisitMethod(f"Visit Method not implemented for {rep=}")

        return fn(element)


class VisitorDefault(ABC):

    @abstractmethod
    def __run_default__(self, element: VisitableInterface) -> Any: ...

    def visit(self, element: VisitableInterface) -> Any:

        rep = element.visitor_rep

        try:
            fn = getattr(self, rep)
        except AttributeError:
            raise NonImplementedVisitMethod(
                f"Visit Method not implemented for {rep}, on Visitor {self.__class__.__name__}"
            )

        return fn(element) if fn is not None else self.__run_default__(element=element)

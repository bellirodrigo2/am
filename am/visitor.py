from dataclasses import dataclass
from typing import Any

from am.interfaces import VisitableInterface, VisitorInterface


class Visitable:

    @property
    def visitor_rep(self) -> str:
        return self.__class__.__name__.lower()

    def accept(self, visitor: VisitorInterface) -> None:

        visitor.visit(self)


class NonImplementedVisitMethod(Exception):
    pass


class Visitor:

    def visit(self, element: VisitableInterface) -> Any:

        rep = element.visitor_rep
        try:
            fn = getattr(self, rep)
        except AttributeError:
            err = f"Visit Method not implemented for {rep=}"
            raise NonImplementedVisitMethod(err)

        return fn(element)

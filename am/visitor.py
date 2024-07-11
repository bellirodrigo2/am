from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from am.interfaces import VisitableInterface, VisitorInterface


class Visitable:

    @classmethod
    def visitor_rep(cls) -> str:
        return cls.__name__.lower()

    def accept(self, visitor: VisitorInterface) -> None:

        visitor.visit(self)


class NonImplementedVisitMethod(Exception): ...


class Visitor:

    def visit(self, element: VisitableInterface | type[VisitableInterface]) -> Any:

        rep = (
            element.visitor_rep()
            if isinstance(element, type)
            else element.__class__.visitor_rep()
        )
        try:
            fn = getattr(self, rep)
        except AttributeError:
            raise NonImplementedVisitMethod(f"Visit Method not implemented for {rep=}")

        return fn(element)


GetByteRep = Callable[[Any], bytes]


@dataclass()
class ByteRepVisitor(Visitor):
    assetserver: GetByteRep = lambda x: b"asse"
    dataserver: GetByteRep = lambda x: b"dase"
    database: GetByteRep = lambda x: b"daba"
    keywords: GetByteRep = lambda x: b"kewo"
    points: GetByteRep = lambda x: b"pont"
    view: GetByteRep = lambda x: b"view"
    node: GetByteRep = lambda x: b"node"
    item: GetByteRep = lambda x: b"item"


if __name__ == "__main__":

    @dataclass(slots=True)
    class Person(Visitable):
        name: str
        age: int

    @dataclass(slots=True)
    class Car(Visitable):
        brand: str
        power: int

    def print_person(x: Person) -> None:
        print(x.name, x.age)

    def print_car(x: Car) -> None:
        print(x.brand, x.power)

    @dataclass(slots=True)
    class VisitorPrint(Visitor):
        person: Callable[[Person], None] = print_person
        car: Callable[[Car], None] = print_car

    pa = Person(name="John", age=42)
    pb = Person(name="Jack", age=26)

    ca = Car(brand="BMW", power=2000)
    cb = Car(brand="Fiat", power=1000)

    visitor = VisitorPrint()
    visitor.visit(pa)
    visitor.visit(pb)
    visitor.visit(ca)
    visitor.visit(cb)

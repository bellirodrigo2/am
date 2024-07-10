from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from am.interfaces import VisitorInterface


class Visitable:

    @property
    def visitor_rep(self) -> str:
        return self.__class__.__name__.lower()

    def accept(self, visitor: VisitorInterface) -> None:

        visitor.visit(self)


class Visitor:

    def visit(self, element: Visitable) -> Any:

        fn = getattr(self, element.visitor_rep)
        return fn(element)


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

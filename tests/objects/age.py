from dataclasses import dataclass

from .baseobj import BaseObj


@dataclass
class Aged(BaseObj):
    age: int

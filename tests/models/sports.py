from dataclasses import dataclass

from .baseobj import BaseObj


@dataclass
class Sports(BaseObj):
    sports: list[str]

from dataclasses import dataclass

from .baseobj import BaseObj


@dataclass
class Hobby(BaseObj):
    hobby: str

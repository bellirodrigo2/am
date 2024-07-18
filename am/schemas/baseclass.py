from collections.abc import Iterable, Mapping
from typing import Any

from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(Label, Visitable):

    @classmethod
    def get_fields(cls) -> Iterable[str]:
        return cls.model_fields.keys()

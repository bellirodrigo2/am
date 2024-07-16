from typing import Any, Mapping

from am.schemas.label import Label
from am.visitor import Visitable


class BaseClass(Label, Visitable):

    def dump(self) -> Mapping[str, Any]:
        return self.model_dump()

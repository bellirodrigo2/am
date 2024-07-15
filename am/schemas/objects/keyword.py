""" Asset Keywords Object """

from pydantic import Field

from am.schemas.baseclass import BaseClass


class Keyword(BaseClass):

    keywords: list[str] = Field()

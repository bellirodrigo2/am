""" Database Object """

from typing import Iterable

from pydantic import Field

from am.schemas.baseclass import BaseClass


class DataBase(BaseClass):

    host: str = Field()

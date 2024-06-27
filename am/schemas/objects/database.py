""" Database Object """

from typing import Annotated

from cahier.schemas.schemas import BaseRoot
from pydantic import Field

###############################################################################


class DataBase(BaseRoot):

    host: str = (Field(),)

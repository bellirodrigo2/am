""" Database Object """

from pydantic import Field

from am.schemas.schemas import BaseRoot

###############################################################################


class DataBase(BaseRoot):

    host: str = (Field(),)

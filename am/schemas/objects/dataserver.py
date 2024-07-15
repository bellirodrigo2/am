""" TimeSeries Data Server Object """

from pydantic import AnyUrl, Field

from am.schemas.baseclass import BaseClass


class DataServer(BaseClass):

    source_url: AnyUrl = Field()
    version: int = Field()

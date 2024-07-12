""" TimeSeries Data Server Object """

from pydantic import AnyUrl, Field

from am.schemas.baseclass import BaseRoot


class DataServer(BaseRoot):

    source_url: AnyUrl = Field()
    version: int = Field()

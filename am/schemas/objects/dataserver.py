""" TimeSeries Data Server Object """

from pydantic import AnyUrl, Field

from am.schemas.baseclass import BaseServer


class DataServer(BaseServer):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"dase"

    source_url: AnyUrl = Field()
    version: int = Field()

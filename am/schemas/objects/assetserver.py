""" Asset Server Object """

from pydantic import AnyUrl, Field

from am.schemas.baseclass import BaseServer


class AssetServer(BaseServer):

    @classmethod
    def byte_rep(cls) -> bytes:
        return b"asse"

    source_url: AnyUrl = Field()

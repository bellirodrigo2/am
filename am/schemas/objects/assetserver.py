""" Asset Server Object """

from pydantic import AnyUrl, Field

from am.schemas.basenode import BaseServer


class AssetServer(BaseServer):
    @classmethod
    def byte_rep(cls) -> bytes:
        return b"serv"

    source_url: AnyUrl = Field()

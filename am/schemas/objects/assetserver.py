""" Asset Server Object """

from pydantic import AnyUrl, Field

from am.schemas.schemas import BaseServer

###############################################################################


class AssetServer(BaseServer):
    source_url: AnyUrl = Field()

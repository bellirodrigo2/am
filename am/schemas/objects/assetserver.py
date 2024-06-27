""" Asset Server Object """

from cahier.schemas.schemas import BaseServer
from pydantic import AnyUrl, Field

###############################################################################


class AssetServer(BaseServer):
    source_url: AnyUrl = (Field(),)

""" Asset Server Object """

from pydantic import AnyUrl, Field

from am.schemas.baseclass import BaseClass


class AssetServer(BaseClass):

    source_url: AnyUrl = Field()

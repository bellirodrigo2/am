""" Template Node Object """

from pydantic import Field

from am.schemas.baseclass import BaseClass


class TemplateNode(BaseClass):

    extensible: bool = Field(default=True)

""""""

from base_table import Base
from sqlalchemy import create_engine


def bootstrap(url: str, echo: bool = False):
    engine = create_engine(url, echo=echo)

    Base.metadata.create_all(engine)
    return engine

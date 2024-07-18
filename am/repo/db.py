""""""

from sqlalchemy import create_engine

from am.repo.base_table import Base


def bootstrap(url: str, echo: bool = False):
    engine = create_engine(url, echo=echo)

    Base.metadata.create_all(engine)
    return engine

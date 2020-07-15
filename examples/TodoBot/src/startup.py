from pathlib import Path

import vkquick as vq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@vq.Signal("startup")
def startup():
    """
    Handler to signal `startup`
    """
    engine = create_engine(
        f"sqlite:///{Path('src') / 'db.sqlite3'}",
        echo=False
    )
    session = sessionmaker(bind=engine)()

    vq.current.engine = engine
    vq.current.session = session

    # Migrate tables
    from . import _tables

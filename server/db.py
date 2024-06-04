from collections.abc import Generator

from sqlmodel import Session, create_engine

import server.models.database.classroom_db_model  # noqa
from server.config import CONFIG

engine = create_engine(f"{CONFIG.db_uri}/{CONFIG.db_database}")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

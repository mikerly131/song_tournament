"""
Give the app some persistence with a SQLite DB, don't need async for now.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.db_models import Base
from contextlib import contextmanager


engine = create_engine("sqlite+pysqlite:///./bracket_voter_simple.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

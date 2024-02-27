"""
Give the app some persistence with a SQLite DB, don't need async for now.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.db_models import Base
from contextlib import contextmanager

# Setup engine to create connection to DB, connect_args only needed for sqlite dbs otherwise remove it
engine = create_engine("sqlite+pysqlite:///./bracket_voter_simple.db", connect_args={"check_same_thread": False})

# Since all models are in db_models and it has the Base model, don't need to import them before this step
Base.metadata.create_all(engine)

# Use sessionmaker to be a db connection session factory for serving sessions
Session = sessionmaker(bind=engine)

# Function that will be called to get a session connection for DB and ensure it gets closed/cleaned up
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

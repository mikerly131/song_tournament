"""
Give the app some persistence with a DB, don't need async for now.

Heavily noted to help beginners get some insight
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.db_models import Base
from contextlib import contextmanager

# Setup engine to create connection to DB, connect_args only needed for sqlite dbs otherwise remove it
# Create tables in the DB from Base - all classes(tables) defined in db_models including Base, so only importing Base
# Factory for sessions - sessionmaker uses engine to make a Session object
# A Session will connect to engine(db), create transaction on connection, holds all objects for transaction
engine = create_engine("sqlite+pysqlite:///./bracket_voter_simple.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Get a session for each request (that needs one) to transact with DB
# Use it for life of request, and then close out the session (released)
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

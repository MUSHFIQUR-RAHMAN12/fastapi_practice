from contextlib import contextmanager

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel,Session
import os
from fastapi import Depends
from typing import Annotated
load_dotenv()
username=os.getenv("DB_USERNAME")
password=os.getenv("DB_PASSWORD")

db_url=f"mysql+mysqlconnector://{username}:{password}@localhost:3306/fastapi_practice"

engine=create_engine(db_url, echo=True)


def create_tables():
    #SQLModel.metadata.drop_all(engine)   # deletes all tables
    SQLModel.metadata.create_all(engine) # recreates fresh
@contextmanager
def get_session_context():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_session():
    with get_session_context() as session:
        yield session

sessiondependency = Annotated[Session, Depends(get_session)]
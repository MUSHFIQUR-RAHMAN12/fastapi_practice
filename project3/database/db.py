from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
import os
load_dotenv()
username=os.getenv("DB_USERNAME")
password=os.getenv("DB_PASSWORD")

db_url=f"mysql+mysqlconnector://{username}:{password}@localhost:3306/fastapi_practice"

engine=create_engine(db_url, echo=True)


def create_tables():
    SQLModel.metadata.drop_all(engine)   # deletes all tables
    SQLModel.metadata.create_all(engine) # recreates fresh
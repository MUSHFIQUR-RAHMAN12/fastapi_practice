from fastapi import FastAPI
from models.mytodo import MyTodo
from database.db import create_tables
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()
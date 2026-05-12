from fastapi import FastAPI,Depends, Query,status,Path,HTTPException
from sqlmodel import Session, select
from models.mytodo import MyTodo
from database.db import create_tables,get_session,sessiondependency
from requestmodel.todoreq import todoreq
from typing import Annotated
from responsemodel.todores import Todores,Todofinalres



app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/todos/create",response_model=Todofinalres,status_code=status.HTTP_201_CREATED)
async def create_todo(todoreq: todoreq, session: sessiondependency):
    todo = MyTodo.model_validate(todoreq)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return {"msg": "Todo created successfully hahaha", "todo": todo}


@app.get("/todos/getall",response_model=list[Todores])
def get_all(session: sessiondependency):
    query=select(MyTodo)
    todos=session.exec(query).all()
    return todos


@app.get("/todos/getbyid/{id}",response_model=Todores)
def get_todo_by_id(session: sessiondependency,id:int=Path(ge=1)):
    todo=session.get(MyTodo,id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {id} not found")
    return todo


@app.get("/todos/getbypriority",response_model=list[Todores])
def get_todo_by_priority(session: sessiondependency,priority:int=Query(ge=1,le=5)):
    query=select(MyTodo).where(MyTodo.priority==priority)
    todos=session.exec(query).all()
    return todos
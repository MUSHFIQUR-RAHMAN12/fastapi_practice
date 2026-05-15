from fastapi import APIRouter,Depends, Query,status,Path,HTTPException
from sqlmodel import Session, select
from models.mytodo import MyTodo
from database.db import create_tables,get_session,sessiondependency
from requestmodel.todoreq import todoreq
from typing import Annotated
from responsemodel.todores import Todores,Todofinalres



router = APIRouter()



@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/todos/create",response_model=Todofinalres,status_code=status.HTTP_201_CREATED)
async def create_todo(todoreq: todoreq, session: sessiondependency):
    todo = MyTodo.model_validate(todoreq)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return {"msg": "Todo created successfully hahaha", "todo": todo}


@router.get("/todos/getall",response_model=list[Todores])
def get_all(session: sessiondependency):
    query=select(MyTodo)
    todos=session.exec(query).all()
    return todos


@router.get("/todos/getbyid/{id}",response_model=Todores)
def get_todo_by_id(session: sessiondependency,id:int=Path(ge=1)):
    todo=session.get(MyTodo,id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {id} not found")
    return todo


@router.get("/todos/getbypriority",response_model=list[Todores])
def get_todo_by_priority(session: sessiondependency,priority:int=Query(ge=1,le=5)):
    query=select(MyTodo).where(MyTodo.priority==priority)
    todos=session.exec(query).all()
    return todos

@router.put("/todos/update/{id}",response_model=Todofinalres)
def update_todo(session: sessiondependency,id:int=Path(ge=1),todoreq:todoreq=None):
    todo=session.get(MyTodo,id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {id} not found")
    todo.title=todoreq.title
    todo.description=todoreq.description
    todo.priority=todoreq.priority
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return {"msg": "Todo updated successfully", "todo": todo}

@router.delete("/todos/delete/{id}")
def delete_todo(session: sessiondependency,id:int=Path(ge=1)):
    todo=session.get(MyTodo,id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {id} not found")
    session.delete(todo)
    session.commit()
    return {"msg": "Todo deleted successfully"}
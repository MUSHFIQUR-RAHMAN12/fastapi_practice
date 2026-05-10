from fastapi import FastAPI,Body,Query,Path
from todomodel import Todo
from datetime import datetime
from todorequest import Todorequest

app = FastAPI()


Todos=[
    Todo(id=1, title="Buy groceries", description="Milk, Bread, Eggs", completed=False, priority=1),
    Todo(id=2, title="Read a book", description="The Great Gatsby", completed=False, priority=2),
    Todo(id=3, title="Exercise", description="Go for a run", completed=False, priority=3),
    Todo(id=4, title="Call mom", description="Check in with family", completed=False, priority=4)]

@app.get("/todos/wow")
async def get_todos():
    return Todos

@app.post("/todos/creation")
async def create_todo(todo: Todorequest):
    t=Todo(**todo.dict())
    Todos.append(get_todo_id(t))
    return t

def get_todo_id(todo):
    if len(Todos)==0:
        todo.id=1
    else:
        todo.id=Todos[-1].id+1
    return todo


@app.put("/todos/update")
async def todo_update(todo: Todorequest):
    t =Todo(**todo.dict())
    for i in range(len(Todos)):
        if Todos[i].id==t.id:
            Todos[i]=t
            return t    
        
@app.delete("/todos/delete/{id}")
async def delete_todo(id:int=Path(ge=1)):
    for i in range(len(Todos)):
        if Todos[i].id==id:
            del Todos[i]
            return {"message": "Todo deleted successfully"}
    return {"message": "Todo not found"}



@app.get("/todos/{id}")
async def get_todo_by_id(id:int=Path(ge=1)):
    for i in range(len(Todos)):
        if Todos[i].id==id:
            return Todos[i]
    return {"message": "Todo not found"}

@app.get("/todos/priority/",status_code=200)
async def get_todo_by_priority(priority:int=Query(ge=1, le=5)):
    result=[]
    for i in range(len(Todos)):
        if Todos[i].priority==priority:
            result.append(Todos[i])
    return result   
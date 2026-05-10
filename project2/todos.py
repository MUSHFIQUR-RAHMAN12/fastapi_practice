from fastapi import FastAPI,Body,Query,Path,HTTPException as htt,status
from todomodel import Todo
from datetime import datetime
from todorequest import Todorequest
from todoresponse import Todoresponse

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="A simple API for managing todo items"
)


Todos=[
    Todo(id=1, title="Buy groceries", description="Milk, Bread, Eggs", completed=False, priority=1),
    Todo(id=2, title="Read a book", description="The Great Gatsby", completed=False, priority=2),
    Todo(id=3, title="Exercise", description="Go for a run", completed=False, priority=3),
    Todo(id=4, title="Call mom", description="Check in with family", completed=False, priority=4)]

@app.get("/todos/wow",response_model=list[Todoresponse],status_code=status.HTTP_200_OK)
async def get_todos():
    return Todos

@app.post("/todos/creation",response_model=Todoresponse,status_code=status.HTTP_201_CREATED)
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


@app.put("/todos/update",response_model=Todoresponse,status_code=status.HTTP_201_CREATED)
async def todo_update(todo: Todorequest):
    t =Todo(**todo.dict())
    not_found=True
    for i in range(len(Todos)):
        if Todos[i].id==t.id:
            Todos[i]=t
            not_found=False
            return t    
    if not_found:
        raise htt(status_code=404, detail="Todo not found")
    
@app.delete("/todos/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id:int=Path(ge=1)):
    not_found=True
    for i in range(len(Todos)):
        if Todos[i].id==id:
            del Todos[i]
            return {"message": "Todo deleted successfully"}
    raise htt(status_code=404, detail="Todo not found")


@app.get("/todos/{id}",response_model=Todoresponse,status_code=status.HTTP_200_OK)
async def get_todo_by_id(id:int=Path(ge=1)):
    for i in range(len(Todos)):
        if Todos[i].id==id:
            return Todos[i]
    raise htt(status_code=404, detail="Todo not found")

@app.get("/todos/priority/",response_model=list[Todoresponse],status_code=200)
async def get_todo_by_priority(priority:int=Query(ge=1, le=5)):
    result=[]
    for i in range(len(Todos)):
        if Todos[i].priority==priority:
            result.append(Todos[i])
    return result   
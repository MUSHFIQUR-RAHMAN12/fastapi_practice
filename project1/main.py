from fastapi import FastAPI,Body

app= FastAPI()

todos= [{"title": "task1", "description": "this is task1", "iscomplete": False},
        
        {"title": "task2", "description": "this is task2","iscomplete": False},
        {"title": "task3", "description": "this is task3","iscomplete": False},
        {"title": "task4", "description": "this is task4","iscomplete": False}]

@app.get("")
def hello_world():
    return {"message": "Hello World"}


@app.get("/todos/all")
def get_all_todos():
    return todos

@app.post("/todos/create")
def create_todo(new_todo=Body()):
    todos.append(new_todo)
    return {"message": "Todo created successfully", "todo": new_todo}

@app.put("/todos/update/{todo_id}")
def update_todo(todo_id: int, updated_todo=Body()):
    if 0 <= todo_id < len(todos):
        todos[todo_id] = updated_todo
        return {"message": "Todo updated successfully", "todo": updated_todo}
    else:
        return {"message": "Todo not found"}, 404
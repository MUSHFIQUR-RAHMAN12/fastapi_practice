from fastapi import FastAPI,Body

app= FastAPI()

todos= [{"title": "task1", "description": "this is task1", "iscomplete": False},
        
        {"title": "task2", "description": "this is task2","iscomplete": True},
        {"title": "task3", "description": "this is task3","iscomplete": False},
        {"title": "task4", "description": "this is task4","iscomplete": True}]

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
    


@app.delete("/todos/delete/{todo_id}")
def delete_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        deleted_todo = todos.pop(todo_id)
        return {"message": "Todo deleted successfully", "todo": deleted_todo}
    else:
        return {"message": "Todo not found"}, 404
    

@app.get("/todos/iscomplete/")
def is_todo_complete(todo_id: int):
    if 0 <= todo_id < len(todos):
        return todos[todo_id]["iscomplete"]
    else:
        return {"message": "Todo not found"}, 404
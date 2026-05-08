from fastapi import FastAPI

app= FastAPI()

todos= [{"title": "task1", "description": "this is task1", "iscomplete": False},
        
        {"title": "task2", "description": "this is task2","iscomplete": False},
        {"title": "task3", "description": "this is task3","iscomplete": False},
        {"title": "task4", "description": "this is task4","iscomplete": False}]

@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/todos/all")
def get_all_todos():
    return todos
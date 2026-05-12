from sqlmodel import SQLModel, Field
from datetime import datetime
from models.todobase import TodoBase

class MyTodo(TodoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    created_at: datetime = Field(default=datetime.now(), nullable=False)
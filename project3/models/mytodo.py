from sqlmodel import SQLModel, Field
from datetime import datetime

class MyTodo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=2, max_length=50,nullable=False)
    description: str = Field(min_length=2, max_length=100,nullable=True)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
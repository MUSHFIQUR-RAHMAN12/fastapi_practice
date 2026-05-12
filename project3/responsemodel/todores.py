from models.todobase import TodoBase
from pydantic import BaseModel, Field

class Todores(TodoBase):
    id:int

class Todofinalres(BaseModel):
    msg:str = Field(default="Todo created successfully", nullable=False)
    todo: Todores
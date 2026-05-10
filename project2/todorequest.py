from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
class Todorequest(BaseModel):
    id: Optional[int]=Field(ge=1,description="The unique identifier of the todo item",default=None)
    title: str = Field(min_length=2, max_length=15)
    description: str = Field(min_length=2, max_length=50)
    completed: Optional[bool]=Field(default=False)
    priority: int = Field(ge=1, le=5)

    model_config = {"json_schema_extra": {
        "example": {
            "title": "Buy any groceries",
            "description": "Milk, Bread, Eggs",
            "completed": False,
            "priority": 1
        }
    }}
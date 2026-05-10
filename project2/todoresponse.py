from pydantic import BaseModel

class Todoresponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: int
    
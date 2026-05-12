from sqlmodel import SQLModel, Field



class TodoBase(SQLModel):
    title: str = Field(min_length=2, max_length=50, nullable=False)
    description: str = Field(min_length=2, max_length=100, nullable=True)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)
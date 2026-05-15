from sqlmodel import Field
from models.userbase import UserBase
from datetime import datetime

class User(UserBase,  table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
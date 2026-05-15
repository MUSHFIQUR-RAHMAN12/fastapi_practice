from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str = Field(nullable=False,min_length=3,max_length=50,unique=True)
    email: str = Field(max_length=255, nullable=False, unique=True)
    

class UserCredential(SQLModel):
    password: str = Field(max_length=255, nullable=False)


class UserCreate(UserBase,UserCredential):
    pass
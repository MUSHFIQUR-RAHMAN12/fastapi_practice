from fastapi import APIRouter,Depends,status,HTTPException
from database.db import sessiondependency
from models.user import User
from responsemodel.userres import UserResponse
from requestmodel.userreq import UserRequest
from sqlmodel import select
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#encode password
def get_password_hash(password):
    return pwd_context.hash(password)


router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def register(usereq:UserRequest,session:sessiondependency):


    data = usereq.model_dump()

    data["hashed_password"] = get_password_hash(data.pop("password"))

    user = User(**data)

    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user.hashed_password = get_password_hash(usereq.password)
    session.add(user)
    session.commit()  
    session.refresh(user)
    return user  


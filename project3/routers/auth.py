from fastapi import APIRouter,Depends,status,HTTPException
from database.db import sessiondependency
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from models.user import User
from responsemodel.userres import UserResponse
from requestmodel.userreq import UserRequest
from sqlmodel import select
from datetime import datetime, timedelta
from utility import check_user_credentials,get_password_hash,create_jwt_token







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

@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],session:sessiondependency):
    email=form_data.username
    password=form_data.password

    # validate user credentials
    authorized_user = await check_user_credentials(email,password,session)
    if not authorized_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    #jwttoken generation logic here
    data={"sub": authorized_user.email,
          "user_id": authorized_user.id,
          "username": authorized_user.username}
    token_dict = await create_jwt_token(data, timedelta(minutes=30))

    return token_dict
from database.db import sessiondependency
from models.user import User
from sqlmodel import select
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#encode password
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password)->bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


async def check_user_credentials(email:str,password:str,session:sessiondependency):
    #return and get user by email

    db_user=session.exec(select(User).where(User.email == email)).first()
    
    #if user is not present in db return false
    if not db_user:
        return False
    #validate password using hash password and return true if valid otherwise false
    if not verify_password(password, db_user.hashed_password):
        return False

    #if email and pssword is valid return user
    return db_user

async def create_jwt_token(data: dict, expires_delta: timedelta):
    #jwt token generation logic here
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, jwt_secret_key, algorithm=jwt_algorithm)
    return {"access_token": access_token, "token_type": "bearer"}


def decoded_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
async def validate_jwt_token(token: Annotated[str, Depends(oauth2_bearer)]):
    payload=decoded_token(token)
    email=payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

auth_user_dependency = Annotated[dict, Depends(validate_jwt_token)]
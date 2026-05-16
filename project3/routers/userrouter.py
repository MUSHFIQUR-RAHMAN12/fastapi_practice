from fastapi import APIRouter, HTTPException, status
from database.db import sessiondependency
from requestmodel.passchanreq import PassChanReq
from utility import auth_user_dependency
from models.user import User
from utility import verify_password, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.put("/change-password")
async def change_password(requser: auth_user_dependency, user_passreq: PassChanReq, session: sessiondependency):
    if not requser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    db_user = session.get(User, requser.get("user_id"))
    db_password = db_user.hashed_password
    asSame= verify_password(hash_password=db_password, plain_password=user_passreq.current_password)
    if not asSame:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    
    db_user.hashed_password = get_password_hash(user_passreq.new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "Password changed successfully"}
    
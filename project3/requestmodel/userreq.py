from models.userbase import UserCreate
from pydantic import ConfigDict
class UserRequest(UserCreate):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "mushfiq",
                "email": "mushfiq@gmail.com",
                "password": "12345678"
            }
        }
    )
    pass 
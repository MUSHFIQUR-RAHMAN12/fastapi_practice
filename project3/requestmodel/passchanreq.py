from pydantic import  BaseModel
class PassChanReq(BaseModel):
    current_password:str
    new_password:str
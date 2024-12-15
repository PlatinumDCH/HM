from pydantic import BaseModel, EmailStr,Field

class ResetPassword(BaseModel):
    email: EmailStr

class ConfirmPassword(BaseModel):
    token:str
    new_password:str = Field (min_length=6, max_length=10)
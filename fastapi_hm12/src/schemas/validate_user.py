from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username:str = Field(min_length=3, max_length=40)
    email: EmailStr
    password:str = Field(min_length=6, max_length=8)

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        form_attributes: True

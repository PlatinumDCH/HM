from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserSchema(BaseModel):
    username:str = Field(min_length=3, max_length=40)
    email: EmailStr
    password:str = Field(min_length=6, max_length=8)

class NewUserSchema(UserSchema):
    avatar: str|None = None

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    model_config = ConfigDict(from_attributes=True)
    

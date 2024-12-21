from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from datetime import date

from src.config import logger

PhoneNumber.phone_format = 'E164' #alternativ: 'INTERNATIONAL', 'NATIONAL'

class ContactCreateSchema(BaseModel):
    first_name: str            = Field(min_length=1, max_length=50)
    last_name: str             = Field(min_length=1, max_length=50)
    email: EmailStr
    note: Optional[str]        = Field(default=None, max_length=250)
    phone_number: PhoneNumber
    date_birthday:date


    @field_validator('first_name', 'last_name')
    def no_leading_trailing_whitespace(cls, variable:str)->str:
        """проверка,отсутствие пробелов в начале и конце строки"""
        if variable != variable.strip():
            raise ValueError('Must not contain leading or trailing whitespace')
        return variable

    @field_validator('date_birthday')
    def validate_age(cls, value:date)->date:
        """проверка, день рождения не больше тукещего дня"""
        today = date.today()
        if value > today:
            logger.info(f'Data of bitsh is in the future')
            raise ValueError('Date of birth cannot be in the future')
        return  value


class ContactResponse(ContactCreateSchema):
    id:int
    model_config = ConfigDict(from_attributes=True)
        

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from datetime import date, timedelta
from pydantic_extra_types.phone_numbers import PhoneNumber


PhoneNumber.phone_format = 'E164' #'INTERNATIONAL', 'NATIONAL'

class ContactCreateSchema(BaseModel):
    first_name: str     = Field(min_length=1, max_length=50)
    last_name: str      = Field(min_length=1, max_length=50)
    email: EmailStr     = Field(min_length=8, max_length=25)
    note: str|None      = None
    phone_number: PhoneNumber
    date_birthday:date


    @field_validator('first_name', 'last_name')
    def no_leading_trailing_whitespace(cls, variable:str):
        if variable != variable.strip():
            raise ValueError('Must not contain leading or trailing whitespace')
        return variable

    @field_validator('date_birthday')
    def validate_age(cls, value):
        min_valid_age_date = date.today() - timedelta(days=365 * 80)
        min_adult_age_date = date.today() - timedelta(days= 365 * 18)

        if not (min_valid_age_date <= value <= min_adult_age_date):
            raise ValueError('Age must be between 18 and 80 years from today')
        return  value

    class Config:
        from_attributes = True

class ContactSchema(ContactCreateSchema):
    id:int

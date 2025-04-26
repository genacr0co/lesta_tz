import re
from pydantic import BaseModel, field_validator

class ValidatePhone(BaseModel):
    phone: str
    
    @field_validator("phone")
    def phone_number_must_be_valid(cls, v):
        if not re.match(r"^\+[0-9]{1,15}$", v):
            raise ValueError("Invalid phone number format")
        return v

class ValidateName(BaseModel):
    name: str

    @field_validator("name")
    def name_length_must_not_exceed_50(cls, v):
        if len(v) > 100:
            raise ValueError("Name length must not exceed 50 characters")
        return v
    

class ValidateUserName(BaseModel):
    username: str

    @field_validator("username")
    def name_length_must_not_exceed_50(cls, v):
        if len(v) > 50:
            raise ValueError("Name length must not exceed 50 characters")
        return v

class ValidateMiddleName(BaseModel):
    middleName: str

    @field_validator("middleName")
    def name_length_must_not_exceed_50(cls, v):
        if len(v) > 50:
            raise ValueError("middleName length must not exceed 50 characters")
        return v

class ValidateEmail(BaseModel):
    email: str

    @field_validator("email")
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email address")
        return v

class ValidateSex(BaseModel):
    sex: int

    @field_validator("sex")
    def rating_must_be_within_range(cls, v):
        if v == 0 or v == 1:
            return v
        else:
            raise ValueError("Sex must be equal to 0 - male or 1 - female")
        
class ValidateRating(BaseModel):
    rating: int
    
    @field_validator("rating")
    def rating_must_be_within_range(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v
    

class RegistragtionValidation(ValidatePhone,ValidateName, BaseModel):
    pass